import os
import rqdatac as rq
import configparser

parser = configparser.ConfigParser()
cur_path = os.getcwd()
parser.read(os.path.join(cur_path, 'config.ini'))

account = parser.get('rqdatac', 'account')
passwd = parser.get('rqdatac', 'passwd')
rq.init(account, passwd)
