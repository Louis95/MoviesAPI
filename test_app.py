import unittest
from app import app
from models import Movies, Actors
from faker import Faker
import json
from datetime import datetime
import tempfile


CASTING_ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJVRkdSVGMzTUVOQlJVSkZNREE0UWpsRk1qQkJSa1EyTXpnM05VSTFNamxDUWtFNE9UY3hPQSJ9.eyJpc3MiOiJodHRwczovL3NlcnZlcmxlc3MtdG9kby1hcHAuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTFlN2M0MTVkZjhhMGM1NmU3YzBhNSIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNTg2NjIwNjQ4LCJleHAiOjE1ODY2Mjc4NDgsImF6cCI6IkFFdEZKMlNBdVI5THFhejVSWXl1Q3BRZEdHZEtjNXV0Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.YZVTc7Hm7EGuoUxOD3WpeP3XyDY5VFESsFFX0kQZxWtNS2tLqDGQY1qizge3UwDEZMcs4fD31aY4PNPFV3HXpz2pGpNCXl6gSBYr6gNMAUUpbhhmlNM8y3kiYlh0wO1cHvT_jKhEts_Fw_pb6habL4W-UyiknPpXa8k13VUuvfp7lyXSWnRwDXs6UWotAtw12nA4bYxqHBmKAHh0VH1Cnzc8iPAGgJ9CdAC5gRbvKlMCeeEeB85tXukMIAvtMXEDPtpi6otp_zOZbbpxi6ImeNvlxeVuoTKecM30BoXJhbvmwyW3Aev2QBvWgl8K5V_WQHZl_S4hjd-3YQNOmOyp-Q"



EXECUTIVE_PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJVRkdSVGMzTUVOQlJVSkZNREE0UWpsRk1qQkJSa1EyTXpnM05VSTFNamxDUWtFNE9UY3hPQSJ9.eyJpc3MiOiJodHRwczovL3NlcnZlcmxlc3MtdG9kby1hcHAuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTFlNTFhNTRjMzIyMGM2OTc0OTAwMiIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNTg2NjIwMTk0LCJleHAiOjE1ODY2MjczOTQsImF6cCI6IkFFdEZKMlNBdVI5THFhejVSWXl1Q3BRZEdHZEtjNXV0Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.ootWJhj259aAmUGYFPDTpvJwDlVytGEy4eW875ZH_Gk5e8LO-4gwxVwESEe67H70t6_xfmvqJfYwmjQ24250eGderHdt7eQr7MAyqv2LE-S45Rd2EWJS7nhiCJM2vDQ-62_j_2GZWwHD99XVZvy_PbCZ-47pjfHkIf-z2AUrq9zmVVSLogVI_om8Z1lYf8o5cW7SopfkIo5Ebuk3VvklBU1zDlwv-SqMnTAXG6zcFd-yydgkRn7LxEiA4TlHWvmPcJb07vW-dFcWGsvMV8YOPfsixVPB0BBpQ1jkPsVmKzwoFmVNc7-zISN9EQ2nTdxSl4mBG64ed_Zw1QnDeeyEaw"



EXPIRED_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6" \
                "IkpXVCIsImt" \
                "pZCI6Ik1rVTBNa1JETjBVM1JrSkRR" \
                "akkzUVRZeE9VTkdO" \
                "RFU1T0RCQ1JVWTFPREl6UWtZMlJqaz" \
                "FRdyJ9.eyJpc3MiOiJodHRwczovL2Rld" \
                "i1oM3ZoNXZuNC5ldS5hd" \
                "XRoMC5jb20vIiwic3ViIjoiYXV0aDB" \
                "8NWU0ZWIwNTQ4MDBmMzcwY2RhNmJjZjU" \
                "xIiwiYXVkIjoiaHR0cDo" \
                "vL2xvY2Fsc2hvc3Q6NTAwMCIsIml" \
                "hdCI6MTU4MjI4MjcwOCwiZXhwIjo" \
                "xNTgyMjg5OTA4LCJhenAiOiJxbX" \
                "VrbTV3RmRBMXZpcWVZMGxUcXJ2ck" \
                "lURHhoU3hybyIsInNjb3BlIjoiI" \
                "iwicGVybWlzc2lvbnMiOlsiZG" \
                "VsZXRlOmFjdG9ycyIsImRlbGV0Z" \
                "Tptb3ZpZXMiLCJnZXQ6YWN0b3I" \
                "tZGV0YWlscyIsImdldDphY3RvcnMi" \
                "LCJnZXQ6bW92aWVzIiwicGF0Y2g6" \
                "bW92aWVzIiwicG9zdDphY3RvcnMi" \
                "LCJwb3N0Om1vdmllcyJdfQ.l2SuzbQ" \
                "uvczXio5lLK9ty6U7Du9oji2DeSQ" \
                "pbmiPD5wskJLT8mbPQRXKg_x-dtyu" \
                "8ParR3DYZEJ7nJvrcOo9P1nnaR5n" \
                "Ua7elujxQgD9XqTWN09onQznIE3DK" \
                "MUzHl9xtxWEwKIRQmeNvwc8ClaHPO" \
                "712sYPnWZEEk3puch0Oj8jjDU1Sj" \
                "3D4DpioP27x9tfMbcJeJcog_a_0pHN-" \
                "pyEC5FshSuIgST-dJxioifP18MnjcpE" \
                "rkQRQnquwsNKSvn6VWB-VN_i" \
                "__-Cpa4J5Bu2oAQ8Bow3st--A4hqjY" \
                "7j0sHi7-Tm8YHbRnGFsehUbh7SIYmAY9BVjjf6x-Fwv_thIg"


fake = Faker()

def get_headers(token):
    return {'Authorization': f'Bearer {token}'}


now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class MoviesTestCase(unittest.TestCase):
    """This class represents the movies test case"""

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client

    def test_get_authorization_url(self):
        res = self.client().get('/authorization/url')
        self.assertEqual(res.status_code, 200)

    def test_post_movie_with_valid_token(self):
        post_data = {"title": fake.name(), "release_date": "2019/09/22"}
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        res = self.client().post("/movies", json=post_data, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_get_movies_with_invalid_token(self):
        auth_header = get_headers("invalid token")
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Unauthorized")

    def test_patch_movie(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"title": fake.text()}
        movie_id = Movies.query.all()[0].id
        res = self.client().patch(f'/movies/{movie_id}', json=data, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_movie_404(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"title": "fake text"}
        movie_id = 10000
        res = self.client().patch(f'/movies/{movie_id}', json=data, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        movie_id = Movies.query.all()[0].id
        res = self.client().delete(f'/movies/{movie_id}', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_movie_404(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        movie_id = 1000
        res = self.client().patch(f'/movies/{movie_id}', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_get_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_get_actors_401(self):
        auth_header = get_headers("invalid token")
        res = self.client().get("/actors", headers=auth_header)
        self.assertEqual(res.status_code, 401)

    def test_post_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"name": fake.name(), "age": 13, "gender": "Male"}
        res = self.client().post("/actors", headers=auth_header, json=data)
        self.assertEqual(res.status_code, 200)

    def test_patch_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        data = {"name": fake.name(), "age": 13, "gender": "Male"}
        self.client().post("/actors", headers=auth_header, json=data)
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        actor_id = Actors.query.all()[0].id
        data = {"name": fake.name()}
        res = self.client().patch(f'/actors/{actor_id}', headers=auth_header, json=data)
        self.assertEqual(res.status_code, 200)

    def test_post_actors_401(self):
        auth_header = get_headers(EXPIRED_TOKEN)
        data = {"name": fake.name(), "age": 13, "gender": "Male"}
        res = self.client().post("/actors", headers=auth_header, json=data)
        self.assertEqual(res.status_code, 401)

    def test_delete_actors(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        actor_id = Actors.query.all()[0].id
        res = self.client().delete(f'/actors/{actor_id}', headers=auth_header)
        self.assertEqual(res.status_code, 200)

    def test_delete_actors_404(self):
        auth_header = get_headers(EXECUTIVE_PRODUCER_TOKEN)
        actor_id = 1000
        res = self.client().delete(f'/movies/{actor_id}', headers=auth_header)
        self.assertEqual(res.status_code, 404)

    def test_401_missing_permission(self):
        auth_header = get_headers(CASTING_ASSISTANT_TOKEN)
        actor_id = Actors.query.all()[0].id
        res = self.client().delete(f'/movies/{actor_id}', headers=auth_header)
        self.assertEqual(res.status_code, 401)

    def test_401_token_expired(self):
        auth_header = get_headers(EXPIRED_TOKEN)
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "token has expired")


if __name__ == '__main__':
    unittest.main()
