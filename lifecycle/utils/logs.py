"""
logs wrapper
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import logging


LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
#fileHandler = logging.FileHandler("logs.log")
#rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
LOG.addHandler(consoleHandler)
