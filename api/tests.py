from django.test import TestCase
import requests
import getpass

# Create your tests here.

class ApiEndpoint(TestCase):
    def test_login_endpoint(self):
        url = "http://localhost:8080/auth/login/"
        password = getpass.getpass()

        data = {'email': "udo@gmail.com", "pasword": password}
        response = requests.post(url=url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    # def test_login_endpoint(self):
    #     url = "http://localhost:8080/api/organization/"
    #     name = 

    #     data = {'email': "udo@gmail.com", "pasword": password}
    #     response = requests.post(url=url, json=data)
    #     print(response.json())
    #     self.assertEqual(response.status_code, 200)
