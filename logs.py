import logging

logs = logging.getLogger()
logs.setLevel(logging.DEBUG)
#fileHandler = logging.FileHandler("logs.log")
#rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
logs.addHandler(consoleHandler)


# wrapper
def info(m):
    logs.info(m)

# wrapper
def error(m):
    logs.error(m)

# wrapper
def debug(m):
    logs.debug(m)

# wrapper
def warning(m):
    logs.warning(m)
