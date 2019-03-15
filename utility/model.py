import pymysql.cursors
import config_database
import time
import json

def mysql_connect():
    connection_obj = pymysql.connect(
        host=config_database.DB_HOST,
        user=config_database.DB_USERNAME,
        password=config_database.DB_PASSWORD,
        db=config_database.DB_DATABASE,
        charset=config_database.DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection_obj


def mysql_close(connection):
    connection.close()


def data_insert(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:

        data_info = get_data_by_file_hash(table, data['file_hash'], mysql_connection)

        if not data_info:
            sql = 'INSERT INTO %s (detail_url, list_thumb_url, title, video_duration, file_hash, addtime,' \
                  'expire_time, video_quality_url, video_hls_url, detail_thumb_url, thumb_slide_url, thumb_slide_minute,' \
                  'cdn_url, tags, status) VALUES %s' % (
            table, '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

            cursor.execute(sql, (
            data['detail_url'], data['list_thumb_url'], data['title'], data['video_duration'], data['file_hash'],
            data['addtime'], data['expire_time'], data['video_quality_url'], data['video_hls_url'], data['detail_thumb_url'],
            data['thumb_slide_url'], data['thumb_slide_minute'], data['cdn_url'], data['tags'], data['status']))

            mysql_connection.commit()


def get_data_by_file_hash(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE file_hash = %s' % (table, '%s')

        cursor.execute(sql, data)

        result = cursor.fetchone()

        return result


def get_page_tracker(table, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE page_type = 1' % table

        cursor.execute(sql)

        result = cursor.fetchone()

        return result


def insert_page_tracker(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:
        sql = 'INSERT INTO %s (page_type, page_number) VALUES %s' % (table, '(%s, %s)')

        cursor.execute(sql, (data['page_type'], data['page_number']))

        mysql_connection.commit()


def update_page_tracker(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:
        sql = 'UPDATE %s SET page_number = %s WHERE page_type = 1' % (table, '(%s)')

        cursor.execute(sql, (data['page_number']))

        mysql_connection.commit()


def insert_tag(table, tag, mysql_connection):

    with mysql_connection.cursor() as cursor:

        for tag in tag.split(','):

            tag_info = get_tag_by_name(table, tag, mysql_connection)

            if not tag_info:
                sql = 'INSERT INTO %s (name) VALUES %s' % (table, '(%s)')

                cursor.execute(sql, tag)

                mysql_connection.commit()


def get_tag_by_name(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE name = %s' % (table, '%s')

        cursor.execute(sql, data)

        result = cursor.fetchone()

        return result


def get_expired_datas(table, page, page_size, mysql_connection):

    offset = (page - 1)*page_size

    with mysql_connection.cursor() as cursor:
        sql = 'SELECT * FROM %s WHERE expire_time < %s ORDER BY ID DESC LIMIT %s, %s' % (table, int(str(time.time()).split('.')[0]), offset, page_size)

        cursor.execute(sql)

        result = cursor.fetchall()

        for data in result:
            yield data


def update_detail_info(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:
        sql = 'UPDATE %s SET video_quality_url = %s, video_hls_url = %s, detail_thumb_url = %s, thumb_slide_url = %s, thumb_slide_minute = %s, cdn_url = %s, tags = %s ,expire_time = %s WHERE file_hash = %s' % (table, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')

        cursor.execute(
            sql, (
                ','.join(data['video_quality_url']),
                data['video_hls_url'],
                ','.join(data['detail_thumb_url']),
                ','.join(data['thumb_slide_url']),
                data['thumb_slide_minute'],
                data['video_url_cdn'],
                ','.join(data['tags']),
                data['expire_time'],
                data['file_hash'],
            )
        )

        mysql_connection.commit()


def delete_video_by_id(table, data, mysql_connection):

    with mysql_connection.cursor() as cursor:
        sql = 'DELETE FROM %s WHERE id = %s' % (table, '%s')

        cursor.execute(sql, data)

        mysql_connection.commit()


def set_related_videos(table, data, mysql_connection):
    with mysql_connection.cursor() as cursor:

        delete_related_videos(table, data['file_hash'], mysql_connection)

        sql = 'INSERT INTO %s (file_hash, related_videos) VALUES %s' % (table, '(%s, %s)')

        cursor.execute(sql, (data['file_hash'], json.dumps(data['related_videos'])))

        mysql_connection.commit()


def delete_related_videos(table, data, mysql_connection):
    with mysql_connection.cursor() as cursor:
        sql = 'DELETE FROM %s WHERE file_hash = %s' % (table, '%s')

        cursor.execute(sql, data)

        mysql_connection.commit()