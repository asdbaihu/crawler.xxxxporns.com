import config_crawler
from utility import model
import handler
import time
import random


def main():
    while True:
        list_datas = model.get_list_datas(config_crawler.LIST_DATA_TABLE_NAME)

        if not list_datas:
            time.sleep(300)
        else:
            for list_data in list_datas:
                time.sleep(random.randint(5, 10))
                detail_data = handler.get_detail_info(list_data)
                model.update_detail_info(config_crawler.LIST_DATA_TABLE_NAME, detail_data)


if __name__ == '__main__':
    main()