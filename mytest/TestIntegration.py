import boto3
import subprocess
import json
import os
import unittest

client = boto3.client('apigateway')
environment = os.environ.get('ENVIRONMENT')
ENDPOINT = "https://{}.execute-api.us-east-1.amazonaws.com/Prod/todos"
TEST_ID = ''


class TestIntegration(unittest.TestCase):
    api_id = None

    @classmethod
    def setUpClass(cls) -> None:
        response = client.get_rest_apis()
        apis = response.get('items')
        todo_api = f"todo-list-aws-{environment}"
        cls.api_id = None
        for api in apis:
            if api.get('name') == todo_api:
                cls.api_id = api.get('id')
                break

    @classmethod
    def tearDownClass(cls) -> None:
        command = ['curl', '-X', 'GET', ENDPOINT.format(cls.api_id)]
        res = json.loads(subprocess.check_output(command).decode())
        for elem in res:
            command = ['curl', '-X', 'DELETE',
                       ENDPOINT.format(cls.api_id) + '/' + elem.get('id')]
            subprocess.check_output(command)

    def test0_api_create(self):
        command = ['curl', '-X', 'POST', ENDPOINT.format(self.api_id),
                   '--data', '{"text": "Learn Serverless"}']
        res = json.loads(subprocess.check_output(command).decode())
        global TEST_ID
        TEST_ID = res.get('id')
        assert (res.get('text') == "Learn Serverless")

    def test1_api_list(self):
        command = ['curl', '-X', 'GET', ENDPOINT.format(self.api_id)]
        res = json.loads(subprocess.check_output(command).decode())
        assert (res[0].get('id') == TEST_ID)
        assert (res[0].get('text') == "Learn Serverless")

    def test2_api_get(self):
        command = ['curl', '-X', 'GET',
                   ENDPOINT.format(self.api_id) + '/' + TEST_ID]
        res = json.loads(subprocess.check_output(command).decode())
        assert (res.get('id') == TEST_ID)
        assert (res.get('text') == "Learn Serverless")

    def test3_api_update(self):
        command = ['curl', '-X', 'PUT',
                   ENDPOINT.format(self.api_id) + '/' + TEST_ID, '--data',
                   '{"text": "Learn python and more", "checked": true}']
        res = json.loads(subprocess.check_output(command).decode())
        assert (res.get('id') == TEST_ID)
        assert (res.get('text') == "Learn python and more")
        assert (res.get('checked'))

    def test4_api_translate(self):
        command = ['curl', '-X', 'GET',
                   ENDPOINT.format(self.api_id) + '/' + TEST_ID + '/es']
        res = json.loads(subprocess.check_output(command).decode())
        assert (res.get('id') == TEST_ID)
        assert (res.get('text') != "Learn python and more")
        assert (res.get('checked'))

    def test5_api_delete(self):
        command = ['curl', '-X', 'DELETE',
                   ENDPOINT.format(self.api_id) + '/' + TEST_ID]
        subprocess.check_output(command)
        command = ['curl', '-X', 'GET', ENDPOINT.format(self.api_id)]
        res = json.loads(subprocess.check_output(command).decode())
        assert (res == [])


if __name__ == '__main__':
    unittest.main()
