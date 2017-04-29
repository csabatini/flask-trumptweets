from datetime import datetime
import requests

base_url = 'https://trumptweets.slickmobile.us/api/v1/'


def get_tags():
    tag_list = requests.get(base_url + 'tag').json()
    return {'tags': tag_list}


def get_tag_statuses(tag_id):
    tag = requests.get(base_url + 'tag', params={'id': tag_id}).json()
    epoch_statuses = requests.get(base_url + 'status', params={'tag_id': tag_id}).json()

    # apply timestamp and row partitioning transformations
    utc_statuses = map(convert_epoch_to_datetime, epoch_statuses)
    status_rows = partition_status_rows(utc_statuses)

    return {
        'tag': tag,
        'status_rows': status_rows
    }


#
# partition_status_rows is a helper function for dividing a list into a grid (2d list) of x rows by 3 columns
# If the original number of objects isn't divisible by 3, the remainder (1 or 2) will be in the last row
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


def convert_epoch_to_datetime(status_dict):
    utc_datetime = datetime.utcfromtimestamp(status_dict['status']['created_at'] / 1000.0)
    status_dict['status']['created_at'] = utc_datetime
    return status_dict
