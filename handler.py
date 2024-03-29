import requests
from pyquery import PyQuery
import re
from utility import hash
import config_crawler
import time
import json


def get_datas(url):
    response = requests.get(url)
    response.encoding = 'utf-8'

    return handle_datas(response.text)


def handle_datas(origin_datas):
    doc = PyQuery(origin_datas)

    datas = doc(".thumb-block").items()

    for data in datas:
        data = str(data)
        detail_url = parse_detail_url(data)
        thumb_url = parse_thumb_url(data)
        title = parse_title(data)
        video_duration = parse_video_duration(data)
        file_hash = hash.hash_with_blake2b(detail_url)

        detail_info = get_detail_info(detail_url)

        if detail_info is not None:
            single_dict = {
                'detail_url': detail_url,
                'list_thumb_url': thumb_url,
                'title': title,
                'video_duration': video_duration,
                'file_hash': file_hash,
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

            yield single_dict


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
    pattern = re.compile(r'<p><a\s+href="(.*?)">(.*?)<\/a><\/p>')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0][1]
    else:
        return ''


def parse_video_duration(data):
    pattern = re.compile(r'class="duration">(.*?)<\/span>')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return result[0]
    else:
        return ''


def get_detail_info(detail_url):

    response = requests.get(config_crawler.BASE_CRAWLER_URL + detail_url)

    fr = parse_detail_page_is_not_found(response.text)

    if fr is False:
        video_url_low = parse_detail_video_url_low(response.text)
        video_url_high = parse_detail_video_url_high(response.text)
        video_hls_url = parse_highest_quality_hls(parse_detail_hls_url(response.text))
        video_thumb_url_small = parse_detail_thumb_url_small(response.text)
        video_thumb_url_big = parse_detail_thumb_url_big(response.text)
        video_slide_thumb_url = parse_slide_thumb_url(response.text)
        video_slide_thumb_url_big = parse_slide_thumb_url_big(response.text)
        video_slide_thumb_url_minute = parse_slide_thumb_url_minute(response.text)
        video_url_cdn = parse_video_url_cdn(response.text)
        tags = parse_video_tags(response.text)

        detail_data = {
            'video_quality_url': [video_url_low, video_url_high],
            'video_hls_url': video_hls_url,
            'detail_thumb_url': [video_thumb_url_small, video_thumb_url_big],
            'thumb_slide_url': [video_slide_thumb_url, video_slide_thumb_url_big],
            'thumb_slide_minute': video_slide_thumb_url_minute,
            'video_url_cdn': video_url_cdn,
            'tags': tags,
        }

        return detail_data
    else:
        return None


def parse_related_videos(data):
    pattern = re.compile(r'var\s+video_related=(.*?);window')
    result = re.findall(pattern, data)

    if len(result) > 0:
        return json.loads(result[0])
    else:
        return ''


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
        parse_highest_quality_hls(result[0])
        return result[0]
    else:
        return ''


def parse_highest_quality_hls(hls_url):
    response = requests.get(hls_url)

    pattern_master_hls = re.compile(r'name="(\d+)p"', re.IGNORECASE)
    result = re.findall(pattern_master_hls, response.text)

    max_pixel_number = max(result)

    url_info = hls_url.split('hls.m3u8')

    base_hls_url = url_info[0]
    hls_uri = 'hls-' + max_pixel_number + 'p.m3u8' + url_info[1]

    full_highest_hls_url = base_hls_url + hls_uri

    return full_highest_hls_url




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


def parse_detail_page_is_not_found(content):
    fp = content.find('http-error-page')

    if fp > 0:
        return True
    else:
        return False


def get_all_tags(tags_url):
    response = requests.get(tags_url)

    doc = PyQuery(response.text)

    tags_html = doc('#tags').items()

    for tag_html in tags_html:
        tags = parse_tag(str(tag_html))

        return tags


def parse_tag(tag_html):
    pattern = re.compile('<b>(.*?)\s+<\/b>')
    result = re.findall(pattern, tag_html)

    return result