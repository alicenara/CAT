from tests.test_website import test_initial_data, read_data
import logging.handlers
import logging
import json
import os

ABS_DIRPATH = os.path.dirname(os.path.abspath(__file__))
LOGS_PATH = os.path.join(ABS_DIRPATH, "logs")


def main():

    # Configuring logs

    if not os.path.isdir(LOGS_PATH):
        os.mkdir(LOGS_PATH)

    log_filename = os.path.join(LOGS_PATH, "test_manager.log")
    level = logging.INFO
    log_format = "%(asctime)s %(levelname)s [%(name)s] %(process)d.%(processName)s : " \
                 "lin %(lineno)s, %(funcName)s - %(message)s"
    max_log_size_mb = 10
    log_backups = 7

    root_logger = logging.getLogger()
    log_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1024 * 1024 * max_log_size_mb, mode="a",
                                                       backupCount=log_backups)
    formatter = logging.Formatter(log_format)
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)
    root_logger.setLevel(level)

    log = logging.getLogger("Test Manager")
    log.info("Starting the program")
    print "Starting the program"

    # Display the menu
    display_menu()
    option = int(raw_input())

    while option != 3:
        if option == 1:
            add_site()
        elif option == 2:
            # Run all tests
            do_tests()
        else:
            print "Wrong option"
        display_menu()
        option = int(raw_input())


def display_menu():
    print "***************************"
    print "********** Menu ***********"
    print "* 1. Add a site           *"
    print "* 2. Do tests             *"
    print "* 3. Quit                 *"
    print "***************************"


def add_site():
    all_data = read_data()
    if all_data is not None:
        print "URL: "
        url = raw_input()
        print "Words: "
        words = raw_input()
        all_data['web'].append({'url': url, 'words': words})
        filetowrite = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests", "initial_data.txt")
        with open(filetowrite, 'w+') as ftw:
            ftw.write(json.dumps(all_data))
        print "ok"


def do_tests():
    # perform each one of the tests
    print "***************************"
    print "*** Probing the website ***"
    print "***************************"
    test_initial_data()

if __name__ == "__main__":
    main()
