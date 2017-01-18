import wikipydia

import re


def getLinksScore(pageName):
    #Download page structured by sections
    pageData = wikipydia.getPage(pageName)
    soup = pageData['full']

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


    #Get the wikilinks texts and build a set of target word
    #Avoid links with : that means special links for wikipedia
    #Clear parentheses in text cause it is not handled proper by text boundaries \b
    #targetWords = set([re.sub(r" \(.*\)", "", link.text.lower()) for link in soup.findAll('a') if link['href'][0:6] == '/wiki/' and not ':' in link['href']])
    targetLinks = set([(link['href'][6:], link.text.lower()) for link in soup.findAll('a') if link['href'][0:6] == '/wiki/' and not ':' in link['href'] and not '(disambiguation)' in link['href']])
    #check why the "for" word is appearing on python
    #test without removing parentheses


    #create and populate a hyper link dict
    hlDict = dict()
    for link, text in targetLinks:
        hlDict[text] = link

    sectionsSoup = pageData['sections']

    #Gen section texts based on article sections
    sectionTexts = []
    for section in sectionsSoup:
        sectionTexts.append(''.join([tag.text for tag in section]))

    presVects = []

    #Improve later with better importance algorithm and using vectors of meanings based on other articles links text
    importVector = getImportanceVector(sectionTexts)

    #MAYBE COUNT THE NUMBER OF TIMES A WORD APPEAR IN THE TEXT FOR ADITIONAL WEIGHT
    #NOW MUST THINK ABOUT THE INTERFACE AND WHERE WILL BE THE START POINT TO MEASURE THE HWO FAR

    for vec in getPresenceVector(sectionTexts, targetLinks).items():
        vecWeight = getVectorWeight(vec[1], importVector)
        presVects.append((vec[0],hlDict[vec[0]], vec[1], vecWeight))


    return presVects


def getPresenceVector(texts, targetLinks):
    wordDict = dict()

    #Iterate thru all target words
    for link in targetLinks:
        word = link[1] #Get link text
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





#Test stuff
if __name__ == "__main__":
    import sys

    def getVectVal(vect):
        """Function to return the sort value of the target vector"""
        return vect[3]


    presVects = getLinksScore(sys.argv[1])

    presVects.sort(key=getVectVal, reverse=True)

    for vect in presVects:
        print vect[0].encode('utf-8'), vect[1], vect[2], vect[3]



