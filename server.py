import os
import cherrypy
import numpy as np

from nvgtt import getLinksScore


class IndexHandler(object):
    @cherrypy.expose
    def index(self):
        # return open('public/index.html')
        return 'lucas'

class UploadHandler(object):
    exposed = True

    def GET(self, article):

        def getVectVal(vect):
            return vect[3]

        presVects = getLinksScore(article)

        presVects.sort(key=getVectVal, reverse=True)

        resultArr = []

        for vect in presVects:
            if vect[1] == article:
                continue
            #resultArr.append("<a href='upload?='" + vect[1].encode('utf-8') + "'>" + vect[0].encode('utf-8') + "</a> " + str(vect[2]))
            resultArr.append("<a href='upload?article=" + vect[0] + "'>" + vect[1].encode('utf-8') + "</a> " + 
                str(vect[2]) + " " + str(vect[3]))

        return '<html><body><span style="font-size:16px;">' + '<br>'.join(resultArr) + '</span></body></html>'

# must think how to keep going
    def POST(self, file):

        return 'post'
     


if __name__ == '__main__':

    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.staticdir.dir': './public'
        },

        '/upload':{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            # 'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
    }

    webapp = IndexHandler()
    webapp.upload = UploadHandler()

    # Read port selected by the cloud for our application
    #PORT = int(os.getenv('PORT', 8080))
    PORT = 80

    # Set server port
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': PORT})

    cherrypy.quickstart(webapp, '/', conf)