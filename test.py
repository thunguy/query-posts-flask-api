import unittest
from app import app

class TestAppAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # Test ping status and response
    def test_ping(self):
        resp = self.app.get('/api/ping')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json['success'])

    # Test query for a single tag
    def test_tag_query(self):
        resp = self.app.get('/api/posts?tags=science')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json['posts'])
        for post in resp.json['posts']:
            self.assertTrue('science' in post['tags'])

    # Test query for multiple tags
    def test_tags_query(self):
        resp = self.app.get('/api/posts?tags=startups,health')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json['posts'])
        for post in resp.json['posts']:
            self.assertTrue('startups' in post['tags'] or 'health' in post['tags'])

    # Test error handling for missing tags input
    def test_tags_error(self):
        resp = self.app.get('/api/posts?tags=')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json['error'], 'tags parameter is required')

    # Test for custom sortBy in default ascending direction
    def test_custom_sort(self):
        resp = self.app.get('/api/posts?tags=history,politics&sortBy=likes&direction=')
        self.assertEqual(resp.status_code, 200)
        prev, curr = 0, 0
        for post in resp.json['posts']:
            self.assertTrue('history' in post['tags'] or 'politics' in post['tags'])
            curr = post['likes']
            self.assertTrue(curr >= prev)
            prev = curr

    # Test for default sortBy 'id' in custom descending direction
    def test_custom_direction(self):
        resp = self.app.get('/api/posts?tags=culture,design&sortBy=&direction=desc')
        self.assertEqual(resp.status_code, 200)
        curr, prev = 0, 0
        for post in resp.json['posts'][::-1]:
            self.assertTrue('culture' in post['tags'] or 'design' in post['tags'])
            curr = post['id']
            self.assertTrue(curr >= prev)
            prev = curr

    # Test error handling for invalid sortBy input
    def test_sort_error(self):
        resp = self.app.get('/api/posts?tags=health&sortBy=lokes')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json['error'], 'sortBy parameter is invalid')


if __name__ == "__main__":
    unittest.main()
