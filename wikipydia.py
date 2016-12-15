import requests

from bs4 import BeautifulSoup

def getPage(page, lang="en"):
    """Function to retrieve a wikipedia page in html form, with its sections"""

    # https://en.wikipedia.org/w/api.php?action=parse&redirects&page=fluid_mechanics

    wikipediaApiUrl = "https://" + lang + ".wikipedia.org/w/api.php"

    pageParams = {
        'action': 'parse', 
        'redirects': True,
        'page': page,
        'format': 'json',
        'prop':'text|displaytitle'
    }

    pageData = requests.get(wikipediaApiUrl, pageParams).json()

    if not 'parse' in pageData:
        raise "Error while getting page " + page


    docHtml = BeautifulSoup(pageData['parse']['text']['*'], 'html.parser')

    #Split document by its sections
    docSections = __splitIntoSections__(docHtml)


    for i, section in enumerate(docSections):
        print "SECTION " + str(i) + "\n"
        print '\n'.join([tag.text for tag in section]).encode('utf-8')
        print "\n\n"

    structPageData = {
        'full': docHtml,
        'sections': docSections
    }

    return structPageData


def __splitIntoSections__(htmlObj):
    """Function to split html document in sections (use h2 tags as divisors)"""

    #Init var to store sections
    sectionObjs = [[]]

    for tag in htmlObj.children:
        #Start new section in case the tag is h2
        if tag.name == 'h2':
            sectionObjs.append([])

        #If it is a valid tag (invalid tags has no 'name' property)
        if tag.name != None:
            sectionObjs[len(sectionObjs) - 1].append(tag)

    return sectionObjs

    #PREVIOUS VERSION BASED ON SECTION IDS
    # for sectionId in sectionsIds:
    #     sectionNode = htmlObj.find(id=sectionId)

    #     if sectionNode != None:
    #         #Create objects to store section tags (since the title is inside a h2 tag, we need the parent tag)
    #         sectionObj = [sectionNode.parent]

    #         for sibling in sectionNode.parent.next_siblings:
    #             #Exit if we find a h2 tag, that means the next section
    #             if sibling.name == 'h2':
    #                 break

    #             #If it is a valid tag
    #             if sibling.name != None:
    #                 sectionObj.append(sibling)

    #     sectionObjs.append(sectionObj)

    # return sectionObjs


#Routines for test module
if __name__ == '__main__':

    def saveFile(htmlData):
        """Debug function to save html data to a file and exit script."""

        f = open('teste3.html', 'w')
        f.write(htmlData.encode('utf-8'))
        f.close()

    pageObj = getPage('Angularjs')


