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

#Remove vertical all vertical table content (NOT WORKING yet)
# for table in soup.findAll("table", {"class": "vertical-navbox"}):
#     table.extract()

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
            #print re.escape(re.escape(word))
            matches = re.findall('\\b' + re.escape(word) + '\\b', text, re.IGNORECASE)
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

sectionTexts = []
for section in sectionsSoup:
    sectionTexts.append(''.join([tag.text for tag in section]).encode('utf-8'))

presVects = []

#Improve later with better importance algorithm and using vectors of meanings based on other articles links text
importVector = getImportanceVector(sectionTexts)

for vec in getPresenceVector(sectionTexts, targetWords).items():
    vecWeight = getVectorWeight(vec[1], importVector)

    presVects.append((vec[0], vec[1], vecWeight))

    # valSum = 0
    # for i, val in enumerate(vec[1]):
    #     if val > 0:
    #         valSum += 2**(len(vec[1]) - i)
    # presVects.append((vec[0], vec[1], valSum))
    

def getVectVal(vect):
    return vect[2]

presVects.sort(key=getVectVal, reverse=True)

for vect in presVects:
    print vect

sys.exit(0)


wordDict = dict()

# NOT WORKING, MUST FIX IT
# CREATE GENERAL METHOD TO HANDLE ANY KIND OF TEXT SPLIT,
# IT WILL RECEIVE A LIST OF THE WORDS TO FOUND AND A LIST OF TEXT SNIPETS
#  THEN WE CAN SPLIT THE DOCUMENT THE WAY WE WANT (SECTIONS, PHRASES, WORDS, ETC)

 #must check word with regular expression \b \\b , not with IN operator





for i, sec in enumerate(sectionsSoup):
    for w in targetWords:
        #Init current word on the dict
        if not w in wordDict:
            wordDict[w] = list()

        wordDict[w].append(0)

        for tag in sec:
            if w in tag.text:
                wordDict[w][len(wordDict[w])-1] = 1
                break


#numberOfSections = len(sectionsSoup)

# teams_list = ["S" + str(i) for i in range(len(sectionsSoup))]

# row_format ="{:>15}" * (len(teams_list) + 1)
# print row_format.format("", *teams_list)

rankDict = dict()

for w in wordDict:
    rankDict[w] = sum(wordDict[w])

#Function to return the sort anchor
def getKey(elem):
    return elem[1]


#NOT WORKING, MUST FIX IT
wordOccurList = sorted(rankDict.items(),key=getKey, reverse=True)

for w in list(wordOccurList):
    print w

sys.exit(0)










#Dict to store words occurrences (default value is 0)
wordsOccur = defaultdict(int)

#Check occurrences ot the target words on the article text and compute number of matches
for tWord in targetWords:
    if tWord == "":
        continue
    try:
        #User regex to match
        #User \b at the start and end to specify word bondaries
        matches = re.findall('\\b' + re.escape(tWord) + '\\b', soup.text, re.IGNORECASE)
        #matches = re.findall(tWord, soup.text, re.IGNORECASE)
        wordsOccur[tWord] = len(matches)
    except:
        pass

#Function to return the sort anchor
def getKey(elem):
    return elem[1]



wordOccurList = sorted(wordsOccur.items(),key=getKey, reverse=True)

sumValues = 0
#Sum all words occurrences
for w in list(wordOccurList):
    sumValues += w[1]

#print result
for w in list(wordOccurList):
    #disp.dispersion_plot(word_tokenize(soup.text), [w[0]])
#for w in targetWords:
    print w
    #print (w[0],float(w[1])/wordOccurList[0][1])
    #print (w[0],float(w[1])/sumValues)


print sumValues



sys.exit(0)

#pageData = wikipedia.page(sys.argv[1])

#Create a new tree with html data from wikipedia
#Since this snippet of html is not fully structured (there is no html or body tags) we need to specify the parser
#soup = BeautifulSoup(pageData.html(), "html.parser")









#saveAndExit(soup.prettify())





# #Tokenize page content
# words = word_tokenize(soup.text)



# for w in words:
#     if w in targetWords:
#         wordsOccur[w] += 1







# for elem in  wordsOccur.items().sort(key=getKey):
#     print elem

#print soup.text.replace(u'\u2013', '-')






