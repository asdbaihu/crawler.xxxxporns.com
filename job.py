import config_crawler
from utility import model
import handler
import time
from utility import logger
import random
from multiprocessing import Pool
import config_crawler


def main(param):

    offset = (param - 1)*config_crawler.JOB_REFRESH_SIZE
    page_size = config_crawler.JOB_REFRESH_SIZE

    mysql_connection = model.mysql_connect()

    expired_datas = model.get_expired_datas(config_crawler.LIST_DATA_TABLE_NAME, offset, page_size, mysql_connection)

    for expired_data in expired_datas:

        logger.write_log(expired_data, 'crawl.xxxxporns.com')
        detail_data = handler.get_detail_info(expired_data['detail_url'])

        if detail_data is not None:
            detail_data.update({'expire_time': int(str(time.time()).split('.')[0]) + config_crawler.VALID_TIME_PERIOD + random.randint(300, 600)})
            detail_data.update({'file_hash': expired_data['file_hash']})
            model.update_detail_info(config_crawler.LIST_DATA_TABLE_NAME, detail_data, mysql_connection)
        else:
            model.delete_video_by_id(config_crawler.LIST_DATA_TABLE_NAME, expired_data['id'], mysql_connection)

    model.mysql_close(mysql_connection)


if __name__ == '__main__':
    l = [i*1 for i in range(1, 11)]
    pool = Pool()
    pool.map(main, l)