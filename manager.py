from tests.test_website import test_initial_data
import logging.handlers
import logging
import os

ABS_DIRPATH = os.path.dirname(os.path.abspath(__file__))
LOGS_PATH = os.path.join(ABS_DIRPATH, "logs")

if __name__ == "__main__":

    """
    Configuring logs
    """

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

    """
    Starting tests
    """
    print "***************************" 
    print "*** Probing the website ***"
    print "***************************"
    test_initial_data()
