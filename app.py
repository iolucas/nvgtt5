from bs4 import BeautifulSoup

import wikipedia

#from nltk import word_tokenize

import wikipydia

import re

import sys

#User default dict because it generates a default value according to the datatype not found
from collections import defaultdict



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


pageData = wikipydia.getPage("MQTT")

offset = int(pageData['sections'][0]['byteoffset'])

print pageData['html'].encode('utf-8')

sys.exit(0)

pageData = wikipedia.page(sys.argv[1])

#Create a new tree with html data from wikipedia
#Since this snippet of html is not fully structured (there is no html or body tags) we need to specify the parser
soup = BeautifulSoup(pageData.html(), "html.parser")


### Treat Data ###

#Clear table of contents if any
for node in soup.findAll(id='toc'):
    node.decompose()

#Clear top info table if any
for node in soup.findAll(class_='ambox'):
    node.decompose()

#Clear everything below some of the sections below
clearSections = ['References', 'See_also']

for section in clearSections:
    clearSectionAndBelow(soup, section)


#saveAndExit(soup.prettify())

#Remove vertical all vertical table content (NOT WORKING yet)
# for table in soup.findAll("table", {"class": "vertical-navbox"}):
#     table.extract()

#Get the wikilinks texts and build a set of target word
targetWords = set([link.text.lower() for link in soup.findAll('a') if link['href'][0:6] == '/wiki/'])

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
#for w in targetWords:
    print w
    #print (w[0],float(w[1])/wordOccurList[0][1])
    #print (w[0],float(w[1])/sumValues)


# #Tokenize page content
# words = word_tokenize(soup.text)



# for w in words:
#     if w in targetWords:
#         wordsOccur[w] += 1







# for elem in  wordsOccur.items().sort(key=getKey):
#     print elem

#print soup.text.replace(u'\u2013', '-')






