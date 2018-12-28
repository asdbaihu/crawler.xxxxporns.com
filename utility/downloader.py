import os
from utility import logger
import requests


def download(url, path, log_type):
    dir_path = os.path.dirname(path)

    if os.path.exists(dir_path) is not True:
        try:
            os.makedirs(dir_path)
        except PermissionError:
            logger.write_log('附件目录( '+dir_path+' )无法创建' + dir_path, log_type)

    if os.path.isfile(path) is not True:
        source = requests.get(url)
        try:
            with open(path, 'wb') as f:
                f.write(source.content)
        except PermissionError:
            logger.write_log('附件目录( '+path+' )不可写', log_type)
