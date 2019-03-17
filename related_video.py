from utility import model
import config_crawler
import handler
from utility import hash
import requests
import time


def get_related_videos():
    mysql_connection = model.mysql_connect()

    last_id_info = get_last_id(mysql_connection)

    if last_id_info is None:
        last_id = 0;
    else:
        last_id = last_id_info['page_number']

    videos = model.get_videos(config_crawler.LIST_DATA_TABLE_NAME, last_id, config_crawler.PAGE_SIZE_TO_VIDEO, mysql_connection)

    if videos:
        model.set_last_id(config_crawler.PAGE_TRACKER_TABLE_NAME, videos[len(videos) - 1]['id'], mysql_connection)

        for video in videos:
            response = requests.get(config_crawler.BASE_CRAWLER_URL + video['detail_url'])
            related_videos = handler.parse_related_videos(response.text)

            for relate_video in related_videos:
                detail_info = handler.get_detail_info(relate_video['u'])
                single_dict = {
                    'detail_url': relate_video['u'],
                    'list_thumb_url': relate_video['i'],
                    'title': relate_video['tf'],
                    'video_duration': relate_video['d'],
                    'file_hash': hash.hash_with_blake2b(relate_video['u']),
                    'addtime': int(str(time.time()).split('.')[0]),
                    'expire_time': int(str(time.time()).split('.')[0]) + config_crawler.VALID_TIME_PERIOD,

                    'video_quality_url': ','.join(detail_info['video_quality_url']),
                    'video_hls_url': detail_info['video_hls_url'],
                    'detail_thumb_url': ','.join(detail_info['detail_thumb_url']),
                    'thumb_slide_url': ','.join(detail_info['thumb_slide_url']),
                    'thumb_slide_minute': detail_info['thumb_slide_minute'],
                    'cdn_url': detail_info['video_url_cdn'],
                    'tags': ','.join(detail_info['tags']),
                    'status': 1,
                }

                model.data_insert(config_crawler.LIST_DATA_TABLE_NAME, single_dict, mysql_connection)
                model.set_related_videos(config_crawler.RELATED_VIDEOS_TABLE_NAME, video['id'], single_dict['file_hash'], mysql_connection)
                model.set_have_related_video(config_crawler.LIST_DATA_TABLE_NAME, video['id'], mysql_connection)
                

def get_last_id(mysql_connection):
    return model.get_last_id(config_crawler.PAGE_TRACKER_TABLE_NAME, mysql_connection)


if __name__ == '__main__':
    get_related_videos()