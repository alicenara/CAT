from libs.TestWebsite import TestWebsite
from libs.TestDirectoryAuthority import TestDirAuth
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


def test_websites(all_data):
    # Website testing
    test = TestWebsite()
    print "********** TESTING WEBSITES **********"

    for w in all_data['web']:
        if test.test_website(w):
            log.info("OK - URL {}".format(w['url']))
            print "OK - URL {}".format(w['url'])
        else:
            log.info("FAILED - URL {}".format(w['url']))
            print "FAILED - URL {}".format(w['url'])


def test_directory_authorities(all_data):
    # Directory authorities testing
    test = TestDirAuth()
    print "*** TESTING DIRECTORY AUTHORITIES ****"

    for d in all_data['dir_auth']:
        if test.test_website(w):
            log.info("OK - URL {}".format(w['url']))
            print "OK - URL {}".format(w['url'])
        else:
            log.info("FAILED - URL {}".format(w['url']))
            print "FAILED - URL {}".format(w['url'])


def test_initial_data():

    all_data = read_data()

    if all_data is None:
        log.error("JSON is malformed, returned None")
        return None

    tests = ['web', 'dir_auth']
    for t in tests:
        if t not in all_data:
            log.error("JSON is malformed, '{}' not found: {}".format(t, all_data))
            return None

    test_websites(all_data)
    #test_directory_authorities(all_data)
    return False
