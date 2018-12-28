import logging
import config_crawler
import os
import time


def write_log(msg='', filename='no_name'):
    if os.path.exists(config_crawler.LOG_PATH) is not True:
        exit('日志目录( '+config_crawler.LOG_PATH+' )不存在')

    logging.basicConfig(filename=config_crawler.LOG_PATH + os.sep + time.strftime('%Y-%m-%d', time.localtime()) + '.' + filename + '.log', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

    logging.info(msg)