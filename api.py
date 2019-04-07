from flask import Flask
from flask import Flask
from flask import jsonify
from flask import request
from utility import model
import config_crawler
import handler
import time
import random

app = Flask(__name__)

@app.route('/api/refresh', methods=['GET'])
def refresh():
    file_hash = request.args.get('file_hash')
    video_id = request.args.get('video_id')

    if not file_hash:
        return jsonify({'results': 'file hash invalid'})

    if not video_id:
        return jsonify({'results': 'video id invalid'})

    mysql_connection = model.mysql_connect()

    video_data = model.get_data_by_file_hash(config_crawler.LIST_DATA_TABLE_NAME, file_hash, mysql_connection)

    detail_data = handler.get_detail_info(video_data['detail_url'])

    if detail_data is not None:
        detail_data.update({'expire_time': int(str(time.time()).split('.')[0]) + config_crawler.VALID_TIME_PERIOD + random.randint(300, 600)})
        detail_data.update({'file_hash': file_hash})
        model.update_detail_info(config_crawler.LIST_DATA_TABLE_NAME, detail_data, mysql_connection)
    else:
        model.delete_video_by_id(config_crawler.LIST_DATA_TABLE_NAME, video_id, mysql_connection)

    model.mysql_close(mysql_connection)

    return jsonify({'results': 'SUCCESS'})

if __name__ == '__main__':
    app.run(host=config_crawler.API_SERVER_ADDRESS, port=5001, debug=True)