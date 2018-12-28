import socket
import psutil
import signal
from pyvirtualdisplay import Display
import re
from utility import logger
import os
import random
from PIL import Image


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def kill_all_processes_by_name(name):
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            p.send_signal(sig=signal.SIGTERM)


def init_virtual_display():
    display = Display(visible=0, size=(800, 600))
    display.start()


def detect_ip_banned(html):
    pattern = re.compile('We\s+have\s+too\s+many\s+requests\s+from\s+your\s+ip\s+in\s+the\s+past\s+24h')
    result = re.findall(pattern, html)

    if len(result) > 0:
        logger.write_log('IP被封,代理自动开启中')
        return True
    else:
        return False


def process_exists_by_command(cmd):
    """/usr/local/bin/python3.6 /usr/share/nginx/html/spider-for-pornleech/run.py is a example"""

    process_info_list = os.popen('ps -ef |grep "'+ cmd +'" |grep -v grep').readlines()

    if len(process_info_list) < 1:
        return False
    else:
        return True


def make_list_unique(list_data):
    new_list_data = set(list_data)

    return list(new_list_data)


def random_string_generation(length = 8):
    result = []

    seed = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for i in range(length):
        result.append(random.choice(seed))

    salt = ''.join(result)

    return salt


def cut_image_by_ratio(path):
    """按照图片长宽比进行分割"""

    base, ext = os.path.splitext(path)

    try:
        im = Image.open(path)
    except IOError:
        return

    w,h = im.size

    flag = int(h/57)

    ww = int(w/flag)
    hh = int(h/flag)

    thumb = im.resize((ww, hh), Image.ANTIALIAS)

    filename = base + '_thumbnail' + ext

    # 保存裁切后的图片
    thumb.save(filename, quality=100)


def make_image_smaller(path, size):

    try:
        im = Image.open(path)
    except IOError:
        return

    base, ext = os.path.splitext(path)

    filename = base + '_thumbnail' + ext

    im.thumbnail((size[0], size[1]), Image.ANTIALIAS)

    im.save(filename)
