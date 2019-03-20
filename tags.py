import config_crawler
import handler
from utility import model


def main():
    tags_url = config_crawler.BASE_CRAWLER_URL + config_crawler.CRAWLER_URI

    mysql_connection = model.mysql_connect()

    tags = handler.get_all_tags(tags_url)

    model.save_all_tags(config_crawler.TAGS_TABLE_NAME, tags, mysql_connection)


if __name__ == '__main__':
    main()