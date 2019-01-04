import config_crawler
import handler
from utility import model


def main():
    crawler_url = config_crawler.BASE_CRAWLER_URL + config_crawler.CRAWLER_URI

    mysql_connection = model.mysql_connect()

    page_info = get_page_tracker(mysql_connection)

    if page_info is None:
        page = 0
        model.insert_page_tracker(config_crawler.PAGE_TRACKER_TABLE_NAME, {'page_number': page, 'page_type': 1}, mysql_connection)
    else:
        page = page_info['page_number'] + 1
        model.update_page_tracker(config_crawler.PAGE_TRACKER_TABLE_NAME, {'page_number': page, 'page_type': 1}, mysql_connection)

    datas = handler.get_datas(crawler_url + str(page))

    for data in datas:
        model.data_insert(config_crawler.LIST_DATA_TABLE_NAME, data, mysql_connection)
        model.insert_tag(config_crawler.TAGS_TABLE_NAME, data['tags'], mysql_connection)

    model.mysql_close(mysql_connection)


def get_page_tracker(mysql_connection):
    return model.get_page_tracker(config_crawler.PAGE_TRACKER_TABLE_NAME, mysql_connection)


if __name__ == '__main__':
    main()