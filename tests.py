import os
import unittest
import json

from app import create_app
from models import setup_db, Show, Magician

# Tokens are formatted as such to limit lenght on a line
ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkotU2tTb3BhU3FyMU9FaVlad3FQNiJ9.eyJpc3MiOiJodHRwczovL2Rldi12NnRnNGYzei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxMzUyMGNhZmRiNmMwMDEzMmU1MjVhIiwiYXVkIjoibWFnaWMiLCJpYXQiOjE1OTUxMTExNzksImV4cCI6MTU5NTE5NzU3OSwiYXpwIjoiOEkzZVA1WEZFbFRaNzFrRlV0RHAzR2haMHFJSjlsdjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDptYWdpY2lhbnMiLCJnZXQ6c2hvd3MiXX0.jWzNulFyT4zVnLhaMkmOe1wyVMg3n01gzCdFpt2N11Ql8aXEBBOVIG3eYlwqceK1b-kbQbKbwtOXPFQQ0gh61m9nXRR9w2OI_OoudRewnWgOVLy-Rg1ty8dmHSr4jPLFb2qUttstkwLvc5lD-Rp7ZzFA02pU29Pew1Hfn4NSKTWeEm92aaD1HBfrjIbdMaTZetUGInMyh-iBELfLnGFbwEICeQC2nCuyP1TsRwxph9QFus2dNOpkBkbJxJvS9UPz6eSz__MaWk9cJEbfvhJssYzp1N8Fac2s0n1NpQZmD9vj310ykxEckcq2KwqNWvVPbocDl3qZTrFOSIw9n6x_PA')
DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkotU2tTb3BhU3FyMU9FaVlad3FQNiJ9.eyJpc3MiOiJodHRwczovL2Rldi12NnRnNGYzei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxMzUyNjc3ZmY2MGQwMDE5ZDY2MzU1IiwiYXVkIjoibWFnaWMiLCJpYXQiOjE1OTUxMTEyNTMsImV4cCI6MTU5NTE5NzY1MywiYXpwIjoiOEkzZVA1WEZFbFRaNzFrRlV0RHAzR2haMHFJSjlsdjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptYWdpY2lhbnMiLCJnZXQ6bWFnaWNpYW5zIiwiZ2V0OnNob3dzIiwicGF0Y2g6bWFnaWNpYW5zIiwicGF0Y2g6c2hvd3MiLCJwb3N0Om1hZ2ljaWFucyJdfQ.noMZjrN8B_HwH4NAhH3QEnimxPIQjnzduYMn_i1X0wt4959syqaibfRddpIuR68lTXed415EhBdAo03It43sm3F5YHBjwidZjHoIea6IQaZoGq_jFl17SwZZLyw_HrOnihJaTimJhjGGPJ8YlhiwGrJ5SaqsJ8o5sb2BgQ6tR0N2ssbG-U2QlX-8U2xzQrqBxsWEptB2YANiqwsEwGJiLV1gjxXjAtVN7ac0aUyAUTopR620UWBMAvo2li3hB1hHlSE2qpJkUGAjpNV8eFq214K95eXojnZEJPdTwMBwLVcDNrC2EZDkHSO6EgFpUTWvfNmlkFIKxlNNhhsMmb98cw')
PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkotU2tTb3BhU3FyMU9FaVlad3FQNiJ9.eyJpc3MiOiJodHRwczovL2Rldi12NnRnNGYzei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxMzUyOTZkYmY2ZmYwMDEzNWM4MGY1IiwiYXVkIjoibWFnaWMiLCJpYXQiOjE1OTUxMTEzMTYsImV4cCI6MTU5NTE5NzcxNiwiYXpwIjoiOEkzZVA1WEZFbFRaNzFrRlV0RHAzR2haMHFJSjlsdjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptYWdpY2lhbnMiLCJkZWxldGU6c2hvd3MiLCJnZXQ6bWFnaWNpYW5zIiwiZ2V0OnNob3dzIiwicGF0Y2g6bWFnaWNpYW5zIiwicGF0Y2g6c2hvd3MiLCJwb3N0Om1hZ2ljaWFucyIsInBvc3Q6c2hvd3MiXX0.rE6q-tqgzov8sZhGfliXpp9n0p8kYETqyux05WOIGnmwQ-QmnDzaLJevVsVWTFEWMdLehha3161uozg_fz5TZ56CVwIlG4z6FUt61UqH-bqQofIAQNsmYdZ3THy0wTGJiZfJVWnZEqG5L1LeVOUpU2xkeXF2uXajQYIHBJhvV6jARZJB4l4yiQzbGwyhDQVVQP-LcVEDCWUKdxeqaSfCVuHpzXkURA4CMkDR58RbMT61vubjkqkHI4k3BItDit789nssLaZtRS8os0VXcCUoczXLuSlO52oU4sIda4nk7EUZWjeAzlekQiomOc80-wdJ93CcjTkEhPaqmEg6KVeeAQ')


class CastingAgencyTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_show = {
            'show_name': 'Goblet of Fire',
            'show_date': '2010-02-02',
        }
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  Tests that you can get all shows
    def test_get_all_shows(self):
        response = self.client().get(
            '/shows',
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['shows'])

    # Test to get a specific show
    def test_get_show_by_id(self):
        response = self.client().get(
            '/shows/1',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['show'])
        #self.assertEqual(data['show']['show_name'], 'The Prisoner of Azkaban')

    # tests for an invalid id to get a specific show
    def test_404_get_show_by_id(self):
        response = self.client().get(
            '/shows/100',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a show
    def test_post_show(self):
        response = self.client().post(
            '/shows',
            json=self.test_show,
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['show'])
        #self.assertEqual(data['show']['show_name'], 'The Philosophers Stone')
        #self.assertEqual(data['show']['show_date'],'Wed, 0 Jan 2010 00:00:00 GMT')

    # Test to create a show if no data is sent
    def test_400_post_show(self):
        response = self.client().post(
            '/shows',
            json={},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for creating a show
    def test_403_post_show_unauthorized(self):
        response = self.client().post(
            '/shows',
            json=self.test_show,
            headers={'Authorization': f'Bearer {DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update a show
    def test_patch_show(self):
        response = self.client().patch(
            '/shows/1',
            json={'show_name': 'Magic Wand', 'show_date': "2019-11-12"},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['show'])
        self.assertEqual(data['show']['show_name'], 'Magic Wand')
        self.assertEqual(
            data['show']['show_date'],
            'Tue, 12 Nov 2019 00:00:00 GMT')

    # Test that 400 is returned if no data is sent to update a show
    def test_400_patch_show(self):
        response = self.client().patch(
            '/shows/1',
            json={},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for updating a show
    def test_403_patch_show_unauthorized(self):
        response = self.client().patch(
            '/shows/1',
            json=self.test_show,
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific show
    def test_404_patch_show(self):
        response = self.client().patch(
            '/shows/12323',
            json=self.test_show,
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests to delete a show
    def test_delete_show(self):
        response = self.client().delete(
            '/shows/3',
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting a show
    def test_403_delete_show(self):
        response = self.client().delete(
            '/shows/2',
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to delete a specific show
    def test_404_delete_show(self):
        response = self.client().delete(
            '/shows/22321',
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    #  Tests that you can get all magicians
    def test_get_all_magicians(self):
        response = self.client().get(
            '/magicians',
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['magicians'])

    # Test to get a specific magician
    def test_get_magician_by_id(self):
        response = self.client().get(
            '/magicians/1',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['magician'])
        #self.assertEqual(data['magician']['name'], 'Harry Potter')

    # tests for an invalid id to get a specific magician
    def test_404_get_magician_by_id(self):
        response = self.client().get(
            '/magicians/100',
            headers={"Authorization": "Bearer " + ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create an magician
    def test_post_magician(self):
        response = self.client().post(
            '/magicians',
            json={'name': 'Ron Weasley', 'age': 20, "gender": "male"},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['magician']['name'], 'Ron Weasley')
        self.assertEqual(data['magician']['age'], 20)
        self.assertEqual(data['magician']['gender'], 'male')

    # Test to create an magician if no data is sent
    def test_400_post_magician(self):
        response = self.client().post(
            '/magicians',
            json={},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for creating an magician
    def test_403_post_magician_unauthorized(self):
        response = self.client().post(
            '/magicians',
            json={'name': 'Hermione Granger', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update an magician
    def test_patch_magician(self):
        response = self.client().patch(
            '/magicians/1',
            json={'name': 'Hermione Granger', 'age': 25, "gender": "female"},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['magician']['name'], 'Hermione Granger')
        self.assertEqual(data['magician']['age'], 25)
        self.assertEqual(data['magician']['gender'], 'female')

    # Test that 400 is returned if no data is sent to update an magician
    def test_400_patch_magician(self):
        response = self.client().patch(
            '/magicians/1',
            json={},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for updating an magician
    def test_403_patch_magician_unauthorized(self):
        response = self.client().patch(
            '/magicians/1',
            json={'name': 'Ron', 'age': 15, "gender": "male"},
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific magician
    def test_404_patch_magician(self):
        response = self.client().patch(
            '/magician/12323',
            json={'name': 'John', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests to delete an magician
    def test_delete_magician(self):
        response = self.client().delete(
            '/magicians/3',
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting an magician
    def test_403_delete_magician(self):
        response = self.client().delete(
            '/magicians/2',
            headers={'Authorization': f'Bearer {ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific magician
    def test_404_delete_magician(self):
        response = self.client().delete(
            '/magicians/22321',
            headers={'Authorization': f'Bearer {PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
