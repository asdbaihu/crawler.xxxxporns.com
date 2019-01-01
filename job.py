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
                time.sleep(random.randint(10, 30))
                detail_data = handler.get_detail_info(list_data)
                model.update_detail_info(config_crawler.LIST_DATA_TABLE_NAME, detail_data)

                for tag in detail_data['tags']:
                    tag_info = model.get_tag_by_name(config_crawler.TAGS_TABLE_NAME, tag)

                    if not tag_info:
                        model.insert_tag(config_crawler.TAGS_TABLE_NAME, tag)


if __name__ == '__main__':
    main()