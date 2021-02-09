import unittest
import os

from src.app import create_app

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(env_name)
        self.client = self.app.test_client

    # Route 1
    def test_200_ping(self):
        req = self.client().get(route_1)
        self.assertEqual(req.status_code, 200)
        self.assertTrue(req.json["success"])

    # Route 2
    def test_200_one_tag(self):
        req = self.client().get(route_2 + "?tag=history")
        self.assertEqual(req.status_code, 200)
        self.assertTrue(req.json["posts"])
        for post in req.json["posts"]:
            self.assertTrue("history" in post["tags"])

    def test_200_two_tags(self):
        req = self.client().get(route_2 + "?tag=history,tech")
        self.assertEqual(req.status_code, 200)
        self.assertTrue(req.json["posts"])
        for post in req.json["posts"]:
            self.assertTrue("history" in post["tags"] or "tech" in post["tags"])

    def test_400_no_tag_param(self):
        req = self.client().get(route_2 + "")
        self.assertEqual(req.status_code, 400)
        self.assertEqual(req.json["error"], "Tags parameter is required")

    def test_200_sort(self):
        req = self.client().get(route_2 + "?tag=history" + "&sortBy=likes")
        self.assertEqual(req.status_code, 200)
        prev, curr = 0, 0
        for post in req.json["posts"]:
            self.assertTrue("history" in post["tags"])
            curr = post["likes"]
            self.assertTrue(curr >= prev)
            prev = curr

    def test_400_sort_bad(self):
        req = self.client().get(route_2 + "?tag=history" + "&sortBy=badsort")
        self.assertEqual(req.status_code, 400)
        self.assertEqual(req.json["error"], "sortBy parameter is invalid")

    def test_400_direction_bad(self):
        req = self.client().get(route_2 + "?tag=history" + "&direction=baddir")
        self.assertEqual(req.status_code, 400)
        self.assertEqual(req.json["error"], "direction parameter is invalid")


if __name__ == "__main__":
    env_name = os.getenv('FLASK_ENV')
    route_1 = "/api/ping"
    route_2 = "/api/posts"
    unittest.main()
