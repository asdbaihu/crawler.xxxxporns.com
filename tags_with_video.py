from utility import model
import config_crawler


def main():
    mysql_connection = model.mysql_connect()
    tags = model.get_tags_with_related_video(config_crawler.LIST_DATA_TABLE_NAME, 1, config_crawler.TAGS_WITH_RELATED_VIDEO_PAGE_SIZE, mysql_connection)

    for tag in tags:
        tag_lists = tag['tags'].split(',')
        for tag_list in tag_lists:
            model.save_related_video_tags(config_crawler.TAGS_WITH_RELATED_VIDEO_TABLE_NAME, tag_list, mysql_connection)


if __name__ == '__main__':
    main()