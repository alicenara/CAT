from libs.TestWebsite import TestWebsite
import logging
import json
import os

INITIAL_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),'initial_data.txt')
#log = logging.getLogger("test_website")

def read_data():
  with open(INITIAL_DATA,"r") as f:
    web = f.read()
   
  try:
    web = json.loads(web)
  except Exception as err:
    #log.error("Initial data malformed: {}".format(web))
    print "Initial data malformed: {}".format(web)
    return None
  return web

def test_initial_data():
  web = read_data()
  test = TestWebsite()
  if web is None or not 'web' in web:
    #log.error("JSON is malformed, 'web' not found: {}".format(web))
    print "lol not found {}".format(web)
    return None
  else:
    for w in web['web']:
      if test.test_website(w):
	#log.info("url {} passed web test".format(w['url']))
	print "url {} passed web test".format(w['url'])
      else:
	#log.info("url {} NOT passed web test".format(w['url']))
	print "url {} NOT passed web test".format(w['url'])  