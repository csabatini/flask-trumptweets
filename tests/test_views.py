from flask_testing import TestCase
from app import create_app


class ViewsTestCase(TestCase):
    def create_app(self):
        return create_app()

    def test_root_url_renders_index_html(self):
        response = self.client.get('/')

        self.assert200(response)
        self.assert_template_used('index.html')

    def test_invalid_url_returns_404(self):
        response = self.client.get('/unknown')

        self.assert404(response)
