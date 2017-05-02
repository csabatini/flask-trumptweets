from datetime import datetime
from flask import abort
import requests

base_url = 'https://trumptweets.slickmobile.us/api/v1/'


def get_tags():
    tag_resp = requests.get(base_url + 'tag')
    handle_api_response(tag_resp)
    return {'tags': tag_resp.json()}


def get_tag_statuses(tag_id):
    tag_resp = requests.get(base_url + 'tag', params={'id': tag_id})
    handle_api_response(tag_resp)

    status_resp = requests.get(base_url + 'status', params={'tag_id': tag_id})
    handle_api_response(status_resp)

    # apply timestamp and row partitioning transformations
    epoch_statuses = status_resp.json()
    datetime_statuses = map(convert_epoch_to_datetime, epoch_statuses)
    status_rows = partition_status_rows(datetime_statuses)

    return {
        'tag': tag_resp.json(),
        'status_rows': status_rows
    }


#
# Render an error template in the flask view if the API call is unsuccessful
#
def handle_api_response(response):
    if response.status_code >= 400:
        abort(response.status_code)
    return None


#
# Divide a list into a grid (2d list) of rows with up to three columns
#
def partition_status_rows(statuses):
    status_count = len(statuses)
    num_rows = status_count / 3

    status_rows = []
    for i in range(0, num_rows):
        status_rows.append(statuses[(i * 3):(i * 3 + 3)])

    if status_count % 3 > 0:
        status_rows.append(statuses[((num_rows - 1) * 3 + 3):])

    return status_rows


#
# Convert epoch time (milliseconds since 1970-01-01) to a datetime object within a dictionary
#
def convert_epoch_to_datetime(status_dict):
    utc_datetime = datetime.utcfromtimestamp(status_dict['status']['created_at'] / 1000.0)
    status_dict['status']['created_at'] = utc_datetime
    return status_dict
