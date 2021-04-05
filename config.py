import os
import configparser

# cur path of project
CUR_PATH = os.path.dirname(os.path.relpath(__file__))

# read .ini
config = configparser.ConfigParser()
config.read(os.path.join(CUR_PATH, './config.ini'))

TUSHARE_TOKEN = config.get('tushare', 'token')
