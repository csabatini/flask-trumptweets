from flask_testing import TestCase
from app import create_app
from test_services import status_url
from test_services import tag_url
from utils import load_mock_data
import responses


class ViewsTestCase(TestCase):
    def create_app(self):
        return create_app()

    @responses.activate
    def test_root_url_renders_index_html(self):
        responses.add(responses.GET, tag_url, json=load_mock_data('tags.json'))
        response = self.client.get('/')

        self.assert200(response)
        self.assert_template_used('index.html')

    @responses.activate
    def test_tag_url_renders_tag_html(self):
        responses.add(responses.GET, tag_url, json=load_mock_data('tag.json'))
        responses.add(responses.GET, status_url, json=load_mock_data('statuses.json'))

        response = self.client.get('/tag/22')
        self.assert200(response)
        self.assert_template_used('tag.html')

    @responses.activate
    def test_invalid_tag_id_renders_404_html(self):
        responses.add(responses.GET, tag_url, status=404)
        responses.add(responses.GET, status_url, json=load_mock_data('statuses.json'))

        response = self.client.get('/tag/50')  # invalid tag id
        self.assert404(response)
        self.assert_template_used('404.html')

    @responses.activate
    def test_internal_error_renders_500_html(self):
        responses.add(responses.GET, tag_url, status=500)

        response = self.client.get('/')
        self.assert_500(response)
        self.assert_template_used('500.html')
