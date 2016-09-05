from libs.TestWebsite import TestWebsite
import logging
import json
import os

INITIAL_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_data.txt")
log = logging.getLogger("T_ProbeWebsite")


"""
Read initial data from file
"""


def read_data():
    with open(INITIAL_DATA, "r") as f:
        web = f.read()

    if web is None or web == "":
        print "The file is empty"
        return None

    try:
        web = json.loads(web)
    except Exception as err:
        log.error("Initial data malformed: data = {}, error = {}".format(web, err))
        print "Initial data malformed: {}".format(web)
        return None
    return web


"""
Do some tests
"""


def test_initial_data():

    # Website testing
    web = read_data()
    test = TestWebsite()
    if web is None or 'web' not in web:
        log.error("JSON is malformed, 'web' not found: {}".format(web))
        return None

    for w in web['web']:
        if test.test_website(w):
            log.info("OK - URL {}".format(w['url']))
            print "OK - URL {}".format(w['url'])
        else:
            log.info("FAILED - URL {}".format(w['url']))
            print "FAILED - URL {}".format(w['url'])