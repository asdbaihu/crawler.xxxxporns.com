import config_crawler
import handler
from utility import model


def main():
    crawler_url = config_crawler.BASE_CRAWLER_URL + config_crawler.CRAWLER_URI
    page_info = get_list_page_tracker()

    if page_info is None:
        page = 0
    else:
        page = page_info['page_number'] + 1

    datas = handler.get_list_datas(crawler_url + str(page))

    model.list_data_insert(config_crawler.LIST_DATA_TABLE_NAME, datas)

    if page_info is None:
        model.insert_page_tracker(config_crawler.PAGE_TRACKER_TABLE_NAME, {'page_number': page, 'page_type': 1})
    else:
        model.update_page_tracker(config_crawler.PAGE_TRACKER_TABLE_NAME, {'page_number': page, 'page_type': 1})


def get_list_page_tracker():
    return model.get_page_tracker(config_crawler.PAGE_TRACKER_TABLE_NAME)


if __name__ == '__main__':
    main()