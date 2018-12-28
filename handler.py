import requests
from pyquery import PyQuery
import re
from utility import hash
import config_crawler
from utility import logger


def get_list_datas(url):
    response = requests.get(url)
    return handle_list_datas(response.text)


def handle_list_datas(origin_datas):
    doc = PyQuery(origin_datas)

    datas = doc(".thumb-block").items()

    list_data = []

    for data in datas:
        data = str(data)
        detail_url = parse_detail_url(data)
        thumb_url = parse_thumb_url(data)
        title = parse_title(data)
        video_duration = parse_video_duration(data)
        file_hash = hash.hash_with_blake2b(detail_url)

        single_dict = {
            'detail_url': detail_url,
            'list_thumb_url': thumb_url,
            'title': title,
            'video_duration': video_duration,
            'file_hash': file_hash
        }

        list_data.append(single_dict)

    return list_data


def parse_detail_url(data):
    pattern = re.compile(r'<a\s+href="(.*?)"><img\s+')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_thumb_url(data):
    pattern = re.compile(r'data-src="(.*?)"\s+')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_title(data):
    pattern = re.compile(r'title="(.*?)">')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_video_duration(data):
    pattern = re.compile(r'class="duration">(.*?)<\/span>')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def get_detail_info(list_data):
    logger.write_log('Crawling the url ' + list_data['detail_url'], 'crawl')
    response = requests.get(config_crawler.BASE_CRAWLER_URL + list_data['detail_url'])

    video_url_low = parse_detail_video_url_low(response.text)
    video_url_high = parse_detail_video_url_high(response.text)
    video_hls_url = parse_detail_hls_url(response.text)
    video_thumb_url_small = parse_detail_thumb_url_small(response.text)
    video_thumb_url_big = parse_detail_thumb_url_big(response.text)
    video_slide_thumb_url = parse_slide_thumb_url(response.text)
    video_slide_thumb_url_big = parse_slide_thumb_url_big(response.text)
    video_slide_thumb_url_minute = parse_slide_thumb_url_minute(response.text)
    video_url_cdn = parse_video_url_cdn(response.text)
    tags = parse_video_tags(response.text)

    detail_datas = {
        'video_quality_url': [video_url_low, video_url_high],
        'video_hls_url': video_hls_url,
        'detail_thumb_url': [video_thumb_url_small, video_thumb_url_big],
        'thumb_slide_url': [video_slide_thumb_url, video_slide_thumb_url_big],
        'thumb_slide_minute': video_slide_thumb_url_minute,
        'video_url_cdn': video_url_cdn,
        'file_hash': hash.hash_with_blake2b(list_data['detail_url']),
        'status': 1,
        'tags': tags
    }

    return detail_datas


def parse_detail_video_url_low(data):
    pattern = re.compile(r'setVideoUrlLow\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_detail_video_url_high(data):
    pattern = re.compile(r'setVideoUrlHigh\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_detail_hls_url(data):
    pattern = re.compile(r'setVideoHLS\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_detail_thumb_url_small(data):
    pattern = re.compile(r'setThumbUrl\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_detail_thumb_url_big(data):
    pattern = re.compile(r'setThumbUrl169\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_slide_thumb_url(data):
    pattern = re.compile(r'setThumbSlide\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_slide_thumb_url_big(data):
    pattern = re.compile(r'setThumbSlideBig\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_slide_thumb_url_minute(data):
    pattern = re.compile(r'setThumbSlideMinute\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_video_url_cdn(data):
    pattern = re.compile(r'setStaticDomain\(\'(.*?)\'\)')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def parse_video_tags(data):
    doc = PyQuery(data)
    tags = []

    for content in doc('.video-metadata li').items():
        tag = do_parse_video_tag(str(content))

        if tag:
            tags.append(tag)

    return tags


def do_parse_video_tag(data):
    pattern = re.compile(r'btn-default">(.*?)<\/a>')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''
