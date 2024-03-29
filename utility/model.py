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


def get_expired_datas(table, page_size, mysql_connection):

    with mysql_connection.cursor() as cursor:
        sql = 'SELECT * FROM %s WHERE expire_time < %s and is_related = 1 ORDER BY ID DESC LIMIT %s' % (table, int(str(time.time()).split('.')[0]), page_size)

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


def set_related_videos(table, origin_video_id, related_file_hash, mysql_connection):
    with mysql_connection.cursor() as cursor:

        sql = 'INSERT INTO %s (related_file_hash, origin_video_id) VALUES %s' % (table, '(%s, %s)')

        cursor.execute(sql, (related_file_hash, origin_video_id))

        mysql_connection.commit()


def get_videos(table, last_id, page_size, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE id > %s and is_related = 0 ORDER BY id ASC limit %s' % (table, '%s', '%s')

        cursor.execute(sql, (last_id, page_size))

        result = cursor.fetchall()

        return result


def set_last_id(table, last_id, mysql_connection):

    delete_last_id(table, mysql_connection)

    with mysql_connection.cursor() as cursor:

        sql = 'INSERT INTO %s (page_type, page_number) VALUES %s' % (table, '(%s, %s)')

        cursor.execute(sql, (2, last_id))

        mysql_connection.commit()


def get_last_id(table, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE page_type = 2' % table

        cursor.execute(sql)

        result = cursor.fetchone()

        return result


def delete_last_id(table, mysql_connection):
    with mysql_connection.cursor() as cursor:
        sql = 'DELETE FROM %s WHERE page_type = 2' % table

        cursor.execute(sql)

        mysql_connection.commit()


def set_have_related_video(table, origin_video_id, mysql_connection):

    with mysql_connection.cursor() as cursor:
        sql = 'UPDATE %s SET is_related = 1 WHERE id = %s' % (table, '(%s)')

        cursor.execute(sql, origin_video_id)

        mysql_connection.commit()


def get_tag_by_random(table, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT * FROM %s ORDER BY rand() limit 1' % table

        cursor.execute(sql)

        result = cursor.fetchone()

        return result


def save_all_tags(table, tags, mysql_connection):
    with mysql_connection.cursor() as cursor:

        sql_insertion = 'INSERT INTO %s (name, hot_level) VALUES %s' % (table, '(%s, %s)')

        for tag in tags:
            sql_select = 'SELECT * FROM %s WHERE name = %s' % (table, '%s')


            cursor.execute(sql_select, tag)

            tag_info = cursor.fetchone()

            if not tag_info:
                cursor.execute(sql_insertion, (tag, 0))

        mysql_connection.commit()


def get_tags_with_related_video(table, is_related, page_size, mysql_connection):

    with mysql_connection.cursor() as cursor:

        sql = 'SELECT tags FROM %s WHERE is_related = %s ORDER BY id DESC limit %s' % (table, '%s', '%s')

        cursor.execute(sql, (is_related, page_size))

        result = cursor.fetchall()

        return result


def save_related_video_tags(table, tag, mysql_connection):
    with mysql_connection.cursor() as cursor:

        sql_insertion = 'INSERT INTO %s (name, hot_level) VALUES %s' % (table, '(%s, %s)')

        sql_select = 'SELECT * FROM %s WHERE name = %s' % (table, '%s')


        cursor.execute(sql_select, tag)

        tag_info = cursor.fetchone()

        if not tag_info:
            cursor.execute(sql_insertion, (tag, 0))

        mysql_connection.commit()