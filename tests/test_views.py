from flask_testing import TestCase
from app import create_app
from test_services import status_url
from test_services import tag_url
from utils import load_mock_data
import requests_mock


class ViewsTestCase(TestCase):
    def create_app(self):
        return create_app()

    @requests_mock.mock()
    def test_root_url_renders_index_html(self, mock_requests):
        mock_requests.get(tag_url, json=load_mock_data('tags.json'))
        response = self.client.get('/')

        self.assert200(response)
        self.assert_template_used('index.html')

    @requests_mock.mock()
    def test_tag_url_renders_tag_html(self, mock_requests):
        mock_requests.get(tag_url, json=load_mock_data('tag.json'))
        mock_requests.get(status_url, json=load_mock_data('statuses.json'))

        response = self.client.get('/tag/22')
        self.assert200(response)
        self.assert_template_used('tag.html')

    # TODO: implement
    # def test_invalid_tag_url_renders_404_html(self):
    #     # mock_requests.get(tag_url, json=load_mock_data('tag.json'))
    #     # mock_requests.get(status_url, json=load_mock_data('statuses.json'))
    #
    #     response = self.client.get('/tag/50')
    #     self.assert200(response)
    #     self.assert_template_used('tag.html')

    def test_invalid_url_renders_404_html(self):
        response = self.client.get('/unknown')

        self.assert404(response)
