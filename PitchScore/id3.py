# Python ID3 algorithm
#    translated from Luger/Stubblefield's lisp version
# Author:  Richard Salter
  
### Usage:
# Build tree using buildTreeFromExamples(examples, classifierName)
# or buildTreeFromData(datlist, namelist)
# For example, with shuttle.py use buildTreeFromExamples(examples, "landing")
# and with congress.py use buildTreeFromData(cdata, cnames)
#
# To classify incoming data use classify(instance, tree), classifyDat(instance, names, tree) or classifyAll(instances, names, tree)

import math, random

# Data Structures

# Property
# Property node used in tree
# name:  property name
# test:  function of 1 argument, returning property value
# values:  list of all possible values returned by test

class Property:
    def __init__(self, name, test, values):
        self.__name = name
        self.__test = test
        self.__values = values
    def name(self):
        return self.__name
    def test(self):
        return self.__test
    def values(self):
        return self.__values

# ExampleFrame:
# Training data set
# instances:   A list of objects of known classification
# properties:  A list of properties of objects in the domain
# classifier:  A property that classifies objects in the instances
#              The values of the classifier will be the leaves of the tree
# size:        Function that returns number of objects in instances
# information: The information content of the instances

class ExampleFrame:
    def __init__(self, instances=[], properties=[], classifier=None, info=None):
        self.__instances = instances
        self.__properties = properties
        self.__classifier = classifier
        self.__info = info
    def instances(self):
        return self.__instances
    def properties(self):
        return self.__properties
    def classifier(self):
        return self.__classifier
    def info(self):
        return self.__info
    def pushInstance(self, x):
        self.__instances = [x]+self.__instances
    def setProperties(self, x):
        self.__properties = x
    def setClassifier(self, x):
        self.__classifier = x
    def setInfo(self, x):
        self.__info = x
    def size(self):
        return len(self.__instances)
    def propSize(self):
        return len(self.__properties)

# Partition
# A partition of the example frame across the values of a property
# test-name:  name of the property used to partition the examples
# test:       test function for that property
# components: dictionary of property-value/example-frame pairs defining the partition
# infoGain:   information gain across all components of the partition

class Partition:
    def __init__(self, testName, test, components, infoGain):
        self.__testName = testName
        self.__test = test
        self.__components = components
        self.__infoGain = infoGain
    def testName(self):
        return self.__testName
    def test(self):
        return self.__test
    def components(self):
        return self.__components
    def infoGain(self):
        return self.__infoGain

# Decision Tree is empty super class for Interior and Leaf

class DecisionTree:
    pass

# Interior
# interior node of the decision tree
# test-name:  name of property used to select a branch
# test:       test function for that property
# branches:   dictionary of property-value/decision-tree pairs

class Interior(DecisionTree):
    def __init__(self, testName, test, branches):
        self.__testName = testName
        self.__test = test
        self.__branches = branches
    def testName(self):
        return self.__testName
    def test(self):
        return self.__test
    def branches(self):
        return self.__branches
    def show(self):
        def showchildren(self):
            ans = dict()
            for key in self.__branches.keys():
                ans[key] = self.__branches[key].show()
            return ans
        return {self.__testName: showchildren(self)}

# Leaf
# leaf node of the decision tree
# value:  a property value of classifier property

class Leaf(DecisionTree):
    def __init__(self, value):
        self.__value = value
    def value(self):
        return self.__value
    def show(self):
        return self.__value

########################
# Functions to construct a decision tree using the ID3 algorithm
# buildTree creates a tree from a training frame:
# (this corresponds to the pseudocode "induce_tree" in the lecture notes)
#   if the training frame is empty create a leaf with no classification
#   if all properties are used create a leaf with remaining classes (may be ambiguous)
#   if all instances are of the same class (info == 0), create a leaf with that class
#   otherwise choose a test for the root of this subtree and recursively build subtrees

def buildTree(trainingFrame):
    if trainingFrame.size() == 0:
        return Leaf("unable to classify; no examples")
    if trainingFrame.propSize() == 0:
        return Leaf(listClasses(trainingFrame))
    if trainingFrame.info() == 0:
        return Leaf(trainingFrame.classifier().test()(trainingFrame.instances()[0]))
    else:
        part = choosePartition(genPartitions(trainingFrame))
        def branchMaker(pc):
            ans = dict()
            for x in pc:
                ans[x] = buildTree(pc[x])
            return ans
        return Interior(part.testName(), part.test(), branchMaker(part.components()))

# genPartitions generates all different partitions of an example frame

def genPartitions(trainingFrame):
    return list(map(lambda x: split(trainingFrame, x), trainingFrame.properties()))

# split takes an example frame and property
# It partitions the example frame on that property
# and returns an instance of a partition structure,
# where partition-components is property-value/ExampleFrame dictionary
# It also computes the information gain and other statistics
# for each component of the partition

def split(rootFrame, property):
    parts = dict()
    for x in property.values():
        parts[x] = ExampleFrame()
    for instance in rootFrame.instances():
        partsList = parts[property.test()(instance)]
        partsList.pushInstance(instance)
    for x in parts:
        frame = parts[x]
        props = rootFrame.properties().copy()
        props.remove(property)
        frame.setProperties(props)
        frame.setClassifier(rootFrame.classifier())
        frame.setInfo(computeInformation(frame.instances(), frame.classifier()))
    return Partition(property.name(), property.test(), parts, computeInfoGain(rootFrame, parts))

# choosePartition takes a list of candidate partitions and chooses 
# The one with the highest information gain

def choosePartition(candidates):
    best = candidates[0]
    for c in candidates[1:]:
        if c.infoGain() > best.infoGain():
            best = c
    return best

# listClasses lists all the classes in the instances of a training frame

def listClasses(trainingFrame):
    classifier = trainingFrame.classifier().test()
    classesPresent = []
    for cl in trainingFrame.classifier().values():
        if cl in list(map(classifier, trainingFrame.instances())):
            classesPresent = [cl] + classesPresent
    return classesPresent

# computeInfoGain computes the information gain of a partition
# by subtracting the weighted average of the information 
# in the children from the information in 
# the original set of instances.

def computeInfoGain(root, parts):
    size = root.size()
    l = []
    return root.info() - sum(list(map(lambda x: parts[x].info() * (parts[x].size()/size), parts.keys())))

# computeInformation computes the information content of a list of examples using a classifier.

def computeInformation(examples, classifier):
    classCount = dict()
    for x in classifier.values():
        classCount[x] = 0
    size = 0
    for instance in examples:
        size += 1
        classCount[classifier.test()(instance)] += 1
    return sum(list(map(lambda x: 0
                        if classCount[x] == 0
                        else -(classCount[x]/size)*math.log2(classCount[x]/size),
                        classCount.keys())))

# buildTreeFromData builds a decision tree from a numerical instance list and name list
# assuming the first property is the classifier

def buildTreeFromData(datlist, namelist):
    return buildTreeFromExamples(buildDb(datlist, namelist), namelist[0][0])

# buildTreeFromExamples first calls buildTrainingFrame on examples to create
# the training frame, then calls buildTree to build the tree

def buildTreeFromExamples(examples, classifierName):
    return buildTree(buildTrainingFrame(examples, classifierName))

# buildDb builds an example list out of a list of numerical instances and
# a name list and builds a database (a list of examples)

def buildDb(dat, names):
    return list(map(lambda x: pairLine(x, names), dat))

# pairLine takes a numerical instance (list of numerical data)
# and a name list and creates an example

def pairLine(datline, names):
    ans = dict()
    def pairUp(ans):
        def pairUp1(dat, names):
            ans[names[0]] = getBucket(dat, names[1:])
        return pairUp1
    list(map(pairUp(ans), datline, names))
    return ans


def getBucket(dat, bucketList):
    if type(bucketList[0])==tuple:
        for i in range(len(bucketList)):
            t = bucketList[i]
            if dat >= t[1] and (i == len(bucketList)-1 or dat < bucketList[i+1][1]):
                return t[0]
    else:
        return bucketList[dat-1]

# buildTrainingFrame builds an ExampleFrame with the given classifier from the list of examples

def buildTrainingFrame(examples, classifierName):
    def possibles(examples, getter):
        l = list(map(getter, examples))
        return list(set(l))
    props = list(examples[0].keys())
    getters = list(map(lambda prop: lambda x: x[prop], props))
    allProperties = list(map(lambda prop, getter: Property(prop, getter, possibles(examples, getter)),
                             props, getters))
    for prop in allProperties:
        if classifierName == prop.name():
            classifier = prop
            allProperties.remove(prop)
            properties = allProperties
            break;
    return ExampleFrame(examples, properties, classifier, computeInformation(examples, classifier))

# classify returns the classifier property value obtained from the tree
# by parsing instance
# instance is a property name/property value dictionary

def classify(instance, tree):
    if type(tree) == Leaf:
        return tree.value()
    key = tree.test()(instance)
    if key in tree.branches().keys():
        subtree = tree.branches()[key]
        return classify(instance, subtree)
    return "unable to classify"

# classifyDat assumes instance is numerical (a list of numbers) corresponding to the
# property names and values in names (where the first name in names is the classifier)

def classifyDat(instance, names, tree):
    return classify(pairLine(instance, names[1:]), tree)

# classifyAll takes a list of numerical instances and classifies them

def classifyAll(instances, names, tree):
    return list(map(lambda z: classifyDat(z, names, tree), instances))


# test_gen generates random data based on the training data.

def test_gen(train, n, f):
    ranges = rangefinder(train)
    l = len(ranges)
    ans = []
    for i in range(n):
        line = []
        for j in range(1, l):
            line.append(f(ranges[j][0], ranges[j][1]))
        ans.append(line)
    return ans

def test_gen_float(train, n):
    return test_gen(train, n, random.uniform)

def test_gen_int(train, n):
        return test_gen(train, n, random.randint)

# rangefinder returns a list of tuples, each representing the interval on which
# the corresponding property lies

def rangefinder(train):
    return list(map(lambda i: (min(map(lambda x: x[i], train)), max(map(lambda x: x[i], train))), range(len(train[0]))))
