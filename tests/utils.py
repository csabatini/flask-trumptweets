import os
import json
import logging


def load_mock_data(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resource_file = os.path.join(base_dir, 'test_data/%s' % filename)

    json_text = '[]'
    try:
        with open(resource_file, 'r') as f:
            json_text = f.read()
    except IOError:
        logging.exception('could not load file %s' % filename)

    return json.loads(json_text)
