import re
import os
import urllib2
import logging
from datetime import datetime
from ontologyutils.ou_settings import Config

__author__ = 'gautierk'

class HPOActions():
    DOWNLOAD='download'

class HPODownloader():

    def __init__(self):
        pass

    def download(self):
        now = datetime.utcnow()
        today = datetime.strptime("{:%Y-%m-%d}".format(datetime.now()), '%Y-%m-%d')

        for dir in [Config.HPO_DIRECTORY, Config.HPO_OBO_DIRECTORY, Config.HPO_ANNOTATIONS_DIRECTORY]:
            if not os.path.exists(dir):
                os.makedirs(dir)

        for url in Config.HPO_URIS:
            directory = Config.HPO_ANNOTATIONS_DIRECTORY
            filename = re.match("^.+/([^/]+)$", url).groups()[0]
            print url
            #match = re.match("^.+/([^/]+)$", url)
            if re.match(Config.HPO_OBO_MATCH, url):
                directory = Config.HPO_OBO_DIRECTORY
            elif re.match(Config.HPO_ANNOTATIONS_MATCH, url):
                directory = Config.HPO_ANNOTATIONS_DIRECTORY

            print filename
            # get a new version of HPO
            req = urllib2.Request(url)

            try:
                response = urllib2.urlopen(req)

                # Open our local file for writing
                local_file = open('%s/%s'%(directory, filename), "wb")
                #Write to our local file
                local_file.write(response.read())
                local_file.close()

                logging.info("downloaded %s"%filename)

            #handle errors
            except urllib2.HTTPError, e:
                print "HTTP Error:",e.code , url
            except urllib2.URLError, e:
                print "URL Error:",e.reason , url