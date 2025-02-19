import unittest
from main import app

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        """Set up a test client before each test"""
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage_loads(self):
        """Test if homepage loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload an Image', response.data)  # Check page content

    def test_upload_without_file(self):
        """Test if uploading without a file returns error"""
        response = self.client.post('/upload', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file uploaded', response.data)

if __name__ == "__main__":
    unittest.main()
