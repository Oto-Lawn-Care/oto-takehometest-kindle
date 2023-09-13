import unittest
from flask import Flask, json
from app.routes import routes
from parameterized import parameterized


class BookRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        routes.register_routes(self.app)
        self.client = self.app.test_client()

    def extract_data(self, response):
        parsed_data = json.loads(response.data)
        if isinstance(parsed_data, dict):
            return parsed_data.get("data", parsed_data)
        return parsed_data

    mock_data1 = {
        "author": "Test",
        "country": "Test",
        "imageLink": "Test",
        "language": "Test",
        "link": "Test",
        "pages": 864,
        "title": "Test",
        "year": 1877,
        "last_read_page": 0,
        "percentage_read": 0.0,
        "last_read_date": 0.0,
    }
    mock_data2 = {
        "country": "Test",
        "imageLink": "Test",
        "language": "Test",
        "link": "Test",
        "pages": 864,
        "title": "Test",
        "year": 1877,
        "last_read_page": 0,
        "percentage_read": 0.0,
        "last_read_date": 0.0,
    }

    @parameterized.expand(
        [
            ("GET", "/global/books", 200, list),
            ("POST", "/global/books", 200, dict, mock_data1),
            ("POST", "/global/books", 400, dict, mock_data2),
            ("GET", "/global/books/search/title/Oedipus the King", 200, list),
            ("GET", "/global/books/search/title/Oedipus the King/author", 200, list),
            ("GET", "/global/books/search/test/test", 400, dict),
            ("GET", "/global/books/search/title/1", 404, dict),
            ("GET", "/user/books", 200, list),
            ("GET", "/user/books/search/title/Oedipus the King", 200, list),
            ("GET", "/user/books/search/title/Oedipus the King/author", 200, list),
            ("GET", "/user/books/search/test/test", 400, dict),
            ("GET", "/user/books/search/title/1", 404, dict),
            ("GET", "/user/books/top/last_read_date", 404, dict),
            ("GET", "/user/books/last-read", 404, dict),
            ("POST", "/user/books/58184ccb-a664-4e5c-b97d-d8c0a7cfdb2e", 200, dict),
            (
                "PATCH",
                "/user/books/58184ccb-a664-4e5c-b97d-d8c0a7cfdb2e/page/202",
                400,
                dict,
            ),
            (
                "PATCH",
                "/user/books/58184ccb-a664-4e5c-b97d-d8c0a7cfdb2e/page/20",
                200,
                dict,
            ),
            ("GET", "/user/books/top/last_read_date", 200, dict),
            ("GET", "/user/books/last-read", 200, dict),
            (
                "DELETE",
                "/user/books/58184ccb-a664-4e5c-b97d-d8c0a7cfdb2e",
                200,
                dict,
            ),
            (
                "DELETE",
                "/user/books/58184ccb-a664-4e5c-b97d-d8c0a7cfdb2e",
                404,
                dict,
            ),
        ]
    )
    def test_endpoint_responses(
        self, request_type, endpoint, expected_status, expected_type, mock_data=None
    ):
        with self.subTest(endpoint=endpoint):
            if request_type == "GET":
                response = self.client.get(endpoint)
            elif request_type == "PATCH":
                response = self.client.patch(endpoint)
            elif request_type == "POST":
                response = self.client.post(endpoint, json=mock_data)
            elif request_type == "DELETE":
                response = self.client.delete(endpoint)

            success_message = f"Endpoint: {endpoint}, Status Code: {response.status_code} - Test PASSED"
            fail_message = f"Endpoint: {endpoint}, Status Code: {response.status_code} - Expected: {expected_status}"

            self.assertEqual(response.status_code, expected_status, fail_message)
            print(success_message)

            if request_type == "DELETE" and expected_status == 204:
                return

            data = self.extract_data(response)
            self.assertIsInstance(data, expected_type)


if __name__ == "__main__":
    unittest.main()
