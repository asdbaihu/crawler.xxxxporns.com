import pymysql.cursors
import config_database

def connect():
    connection_obj = pymysql.connect(
        host=config_database.DB_HOST,
        user=config_database.DB_USERNAME,
        password=config_database.DB_PASSWORD,
        db=config_database.DB_DATABASE,
        charset=config_database.DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection_obj


def list_data_insert(table, datas):
    connection_obj = connect()

    with connection_obj.cursor() as cursor:
        for data in datas:

            sql = 'INSERT INTO %s (detail_url, list_thumb_url, title, video_duration, file_hash, addtime) VALUES %s' % (table, '(%s, %s, %s, %s, %s, %s)')

            cursor.execute(sql, (data['detail_url'], data['list_thumb_url'], data['title'], data['video_duration'], data['file_hash'], data['addtime']))

    connection_obj.commit()

    connection_obj.close()

    return True


def get_page_tracker(table):
    connection_obj = connect()

    with connection_obj.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE page_type = 1' % table

        cursor.execute(sql)

        result = cursor.fetchone()

        connection_obj.close()

        return result


def insert_page_tracker(table, data):
    connection_obj = connect()

    with connection_obj.cursor() as cursor:
        sql = 'INSERT INTO %s (page_type, page_number) VALUES %s' % (table, '(%s, %s)')

        cursor.execute(sql, (data['page_type'], data['page_number']))

        connection_obj.commit()

        connection_obj.close()

        return True


def update_page_tracker(table, data):
    connection_obj = connect();

    with connection_obj.cursor() as cursor:
        sql = 'UPDATE %s SET page_number = %s WHERE page_type = 1' % (table, '(%s)')

        cursor.execute(sql, (data['page_number']))

        connection_obj.commit()

        connection_obj.close()

        return True


def get_list_datas(table, page, page_size):

    offset = (page - 1)*page_size

    connection_obj = connect()

    with connection_obj.cursor() as cursor:
        sql = 'SELECT * FROM %s LIMIT %s, %s' % (table, offset, page_size)

        cursor.execute(sql)

        result = cursor.fetchall()

        connection_obj.close()

        return result


def update_detail_info(table, data):

    connection_obj = connect()

    with connection_obj.cursor() as cursor:
        sql = 'UPDATE %s SET video_quality_url = %s, video_hls_url = %s, detail_thumb_url = %s, thumb_slide_url = %s, thumb_slide_minute = %s, cdn_url = %s, tags = %s ,status = %s WHERE file_hash = %s' % (table, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')

        cursor.execute(
            sql, (
                ','.join(data['video_quality_url']),
                data['video_hls_url'],
                ','.join(data['detail_thumb_url']),
                ','.join(data['thumb_slide_url']),
                data['thumb_slide_minute'],
                data['video_url_cdn'],
                ','.join(data['tags']),
                data['status'],
                data['file_hash'],
            )
        )

        connection_obj.commit()

        connection_obj.close()


def insert_tag(table, tag):

    connection_obj = connect()

    with connection_obj.cursor() as cursor:
        sql = 'INSERT INTO %s (name) VALUES %s' % (table, '(%s)')

        cursor.execute(sql, tag)

        connection_obj.commit()

        connection_obj.close()


    return True


def get_tag_by_name(table, data):
    connection_obj = connect()

    with connection_obj.cursor() as cursor:

        sql = 'SELECT * FROM %s WHERE name = %s' % (table, '%s')

        cursor.execute(sql, data)

        result = cursor.fetchone()

        connection_obj.close()

        return result
