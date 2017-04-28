from flask_testing import TestCase
from app import create_app
from app.main import services
from utils import load_mock_data
import requests_mock

tag_url = 'https://trumptweets.slickmobile.us/api/v1/tag'
status_url = 'https://trumptweets.slickmobile.us/api/v1/status'
exp_tag_keys = ['count', 'tag', 'tag_id', 'max_created_at']


class ServicesTestCase(TestCase):
    def create_app(self):
        return create_app()

    @requests_mock.mock()
    def test_get_tags(self, mock_requests):
        mock_requests.get(tag_url, json=load_mock_data('tags.json'))

        response = services.get_tags()
        # tags response should be a dictionary
        assert type(response) == dict

        # tags response dictionary keys
        assert len(response.keys()) == 1
        assert response.keys()[0] == 'tags'

        # tags response dictionary values
        assert type(response['tags']) == list
        assert len(response['tags']) == 22

        assert type(response['tags'][0]) == dict
        assert len(response['tags'][0].keys()) == len(exp_tag_keys)
        for key in exp_tag_keys:
            assert key in response['tags'][0]

    @requests_mock.mock()
    def test_get_tag_statuses(self, mock_requests):
        mock_requests.get(tag_url, json=load_mock_data('tag.json'))
        mock_requests.get(status_url, json=load_mock_data('statuses.json'))

        tag_id = 22
        response = services.get_tag_statuses(tag_id)

        # tag statuses response should be a dictionary
        assert type(response) == dict

        # tag statuses response dictionary keys
        assert len(response.keys()) == 2
        assert 'tag' in response.keys()
        assert 'status_rows' in response.keys()

        # tag component of response: should be a dict
        assert type(response['tag']) == dict
        assert len(response['tag'].keys()) == len(exp_tag_keys)
        for key in exp_tag_keys:
            assert key in response['tag']

        # status_rows component of response: should be a list of status rows (nested lists w/ <= 3 elements)
        status_rows = response['status_rows']
        assert type(status_rows) == list
        assert len(status_rows) == 3

        for row in status_rows:
            assert type(row) == list

        # 8 statuses from the mock json array are divided into a grid of rows with up to 3 columns
        assert len(status_rows[0]) == 3
        assert len(status_rows[1]) == 3
        assert len(status_rows[2]) == 2
