import config_crawler
from utility import model
import handler
import time


def main():

    page = 1
    page_size = 20

    mysql_connection = model.mysql_connect()

    while True:
        expired_datas = model.get_expired_datas(config_crawler.LIST_DATA_TABLE_NAME, page, page_size, mysql_connection)

        for expired_data in expired_datas:
            detail_data = handler.get_detail_info(expired_data['detail_url'])
            detail_data.update({'expire_time': int(str(time.time()).split('.')[0]) + config_crawler.VALID_TIME_PERIOD})
            detail_data.update({'file_hash': expired_data['file_hash']})

            model.update_detail_info(config_crawler.LIST_DATA_TABLE_NAME, detail_data, mysql_connection)
        else:
            model.mysql_close(mysql_connection)

        page += 1


if __name__ == '__main__':
    main()