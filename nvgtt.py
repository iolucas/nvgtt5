from bs4 import BeautifulSoup

#import wikipedia

#from nltk import word_tokenize

import wikipydia

import re

import sys

#Module to render graphics
#import matplotlib.pyplot as plt

#User default dict because it generates a default value according to the datatype not found
from collections import defaultdict

from nltk.tokenize import word_tokenize

import nltk.draw.dispersion as disp


def saveAndExit(htmlData):
    """Debug function to save html data to a file and exit script."""

    f = open('teste2.html', 'w')
    f.write(htmlData.encode('utf-8'))
    f.close()
    sys.exit(0)


def clearSectionAndBelow(html, sectionId):
    """Function to remove the target section and content below it in a wikipedia article."""

    clearNode = html.find(id=sectionId)

    if clearNode:

        #Create list of nodes to be removed
        #Check if they are valid nodes by the name property
        decomposeQueue = [siblingNode for siblingNode in clearNode.parent.next_siblings if siblingNode.name != None]
        decomposeQueue.append(clearNode.parent)

        #Remove all nodes on the list
        for nodeToDelete in decomposeQueue:
            nodeToDelete.decompose()




#---- main() ----#


pageData = wikipydia.getPage(sys.argv[1])
soup = pageData['full']

# for p in soup.findAll('p'):
#     print p.text.encode('utf-8')
#     print '\n'


# sys.exit(0)


#USER 1+ LOG OF FREQUENCY AS MEASUREMENT

#Use something like the kalman filters to estimate the orders of important things

### Treat Data ###

#Clear table of contents if any
for node in soup.findAll(id='toc'):
    node.decompose()

#Clear top info table if any
for node in soup.findAll(class_='ambox'):
    node.decompose()

#Clear info box if any
for node in soup.findAll(class_='infobox'):
    node.decompose()

#Clear verticalbox if any
for node in soup.findAll(class_='vertical-navbox'):
    node.decompose()


#Clear everything below some of the sections below
# clearSections = ['References', 'See_also']

# for section in clearSections:
#     clearSectionAndBelow(soup, section)


# for i, section in enumerate(pageData['sections']):
#     print "SECTION " + str(i) + "\n"
#     print '\n'.join([tag.text for tag in section]).encode('utf-8')
#     print "\n\n"

#print re.findall('\\bMCU \(Micro Controller Unit\)', soup.text, re.IGNORECASE)

def getPresenceVector(texts, targetWords):
    wordDict = dict()

    #Iterate thru all target words
    for word in targetWords:
        wordDict[word] = []
        #Iterate thru all texts 
        for text in texts:
            #Match words inside its boundaries (non-alphanumeric chars)
            matches = re.findall('[^a-zA-Z0-9_]' + re.escape(word) + '[^a-zA-Z0-9_]', text, re.IGNORECASE)
            #matches = re.findall('\\b' + re.escape(word) + '\\b', text, re.IGNORECASE)
            #matches = re.findall('\\b' + word + '\\b', text, re.IGNORECASE)
            wordDict[word].append(len(matches))
            
    return wordDict

#For know just return a 2^n weight where n is the arraylength - index
def getImportanceVector(texts):
    textsLen = len(texts)
    return [2**(textsLen - n - 1) for n in xrange(textsLen)]

#Function to cross importance vector to generate an importance weight to the current presence vector
def getVectorWeight(targetVector, importanceVector):
    #raise an error if the target vector length is diferent from the importance vector length
    if len(targetVector) != len(importanceVector):
        raise "ERROR: Vectors length do not match. " + len(targetVector) + " " + len(importanceVector)

    valSum = 0
    for i, val in enumerate(targetVector):
        if val > 0:
            valSum += importanceVector[i]
    
    return valSum

#Get the wikilinks texts and build a set of target word
#Avoid links with : that means special links for wikipedia
#Clear parentheses in text cause it is not handled proper by text boundaries \b
#targetWords = set([re.sub(r" \(.*\)", "", link.text.lower()) for link in soup.findAll('a') if link['href'][0:6] == '/wiki/' and not ':' in link['href']])
targetWords = set([link.text.lower() for link in soup.findAll('a') if link['href'][0:6] == '/wiki/' and not ':' in link['href']])
#check why the "for" word is appearing on python
#test without removing parentheses

sectionsSoup = pageData['sections']

# for section in sectionsSoup:
#     print ''.join([tag.text for tag in section]).encode('utf-8')
#     print "\n\n"

# sys.exit(0)

# for word in targetWords:
#     print word
#     print "\n"

#Gen section texts based on article sections
sectionTexts = []
for section in sectionsSoup:
    sectionTexts.append(''.join([tag.text for tag in section]))

presVects = []

#Improve later with better importance algorithm and using vectors of meanings based on other articles links text
importVector = getImportanceVector(sectionTexts)

#MAYBE COUNT THE NUMBER OF TIMES A WORD APPEAR IN THE TEXT FOR ADITIONAL WEIGHT
#NOW MUST THINK ABOUT THE INTERFACE AND WHERE WILL BE THE START POINT TO MEASURE THE HWO FAR

for vec in getPresenceVector(sectionTexts, targetWords).items():
    vecWeight = getVectorWeight(vec[1], importVector)

    presVects.append((vec[0], vec[1], vecWeight))
    

def getVectVal(vect):
    return vect[2]

presVects.sort(key=getVectVal, reverse=True)

for vect in presVects:
    print vect[0].encode('utf-8'), vect[1], vect[2]