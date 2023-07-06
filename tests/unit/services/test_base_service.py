import httpretty
import json
from tests.test_config import HttprettyTestCase
from cardda_python.http_client import HttpClient
from cardda_python.services.base_service import BaseService
from cardda_python.resources.base_resource import BaseResource

class SomeResource(BaseResource):
    name = "something"

    @property
    def allowed_nested_attributes(self):
        base = super().allowed_nested_attributes
        extended = ["nested_object"]
        return base + extended

class SomeService(BaseService):
    resource = SomeResource
    methods = ["all", "find", "create", "save", "delete"]

SOME_RESOURCE_AS_JSON = {
    "id": "1",
    "some_field": "some_value",
    "other_field": "other_value",
    "nested_object": {
        "nested_field": "nested_value"
    }
}

class TestBaseService(HttprettyTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        base_url = "https://api.cardda.com/v1"
        api_key = "your-api-key"
        cls.client = HttpClient(base_url, api_key)
        cls.service = SomeService(cls.client)


    def test_all(self):
        expected_response = [SOME_RESOURCE_AS_JSON]
        # Configure httpretty to mock the request
        httpretty.register_uri(
            httpretty.GET,
            f"{self.client.base_url}/{SomeResource.name}/",
            responses=[
                httpretty.Response(body=json.dumps(expected_response), status=200, content_type='application/json')
            ]
        )

        # Make the request
        response = self.service.all()
        # Assertions
        self.assertEqual(list(map(lambda x: x.as_json(), response)), expected_response)
        for entry in response:
            self.assertEqual(isinstance(entry, SomeResource), True)

    

    def test_find(self):
        expected_response = SOME_RESOURCE_AS_JSON
        # Configure httpretty to mock the request
        httpretty.register_uri(
            httpretty.GET,
            f"{self.client.base_url}/{SomeResource.name}/{SOME_RESOURCE_AS_JSON['id']}",
            responses=[
                httpretty.Response(body=json.dumps(expected_response), status=200, content_type='application/json')
            ]
        )
        # Make the request
        response = self.service.find(SOME_RESOURCE_AS_JSON['id'])
        # Assertions
        self.assertEqual(response.as_json(), expected_response)
        self.assertEqual(isinstance(response, SomeResource), True)
    
    def test_save(self):
        resource = SomeResource(SOME_RESOURCE_AS_JSON)
        resource.some_field = "updated_value"
        expected_response = resource.as_json()
        expected_request = resource.as_json()

        def request_callback(request, uri, headers):
            # Request body has to be the same as the response
            assert request.body.decode("utf-8") == json.dumps(expected_request), 'unexpected body: {}'.format(request.body)
            # Check if the request body matches the desired condition
            return (200, headers, json.dumps(expected_response))
    
        # Configure httpretty to mock the request
        httpretty.register_uri(
            httpretty.PATCH,
            f"{self.client.base_url}/{SomeResource.name}/{expected_response['id']}",
            body=request_callback
        )
        # Make the request
        response = self.service.save(resource)
        # Assertions
        self.assertEqual(response.as_json(), expected_response)
        self.assertEqual(isinstance(response, SomeResource), True)
    
    def test_create(self):
        resource = SomeResource(SOME_RESOURCE_AS_JSON)
        expected_response = SOME_RESOURCE_AS_JSON
        expected_request = resource.as_json()

        def request_callback(request, uri, headers):
            # Request body has to be the same as the response
            assert request.body.decode("utf-8") == json.dumps(expected_request), 'unexpected body: {}'.format(request.body)
            # Check if the request body matches the desired condition
            return (200, headers, json.dumps(expected_response))
        
        # Configure httpretty to mock the request
        httpretty.register_uri(
            httpretty.POST,
            f"{self.client.base_url}/{SomeResource.name}/",
            body=request_callback
        )
        # Make the request
        response = self.service.create(**expected_request)
        # Assertions
        self.assertEqual(response.as_json(), expected_response)
        self.assertEqual(isinstance(response, SomeResource), True)
    
    def test_delete(self):
        expected_response = SOME_RESOURCE_AS_JSON
        # Configure httpretty to mock the request
        httpretty.register_uri(
            httpretty.DELETE,
            f"{self.client.base_url}/{SomeResource.name}/{SOME_RESOURCE_AS_JSON['id']}",
            responses=[
                httpretty.Response(body=json.dumps(expected_response), status=200, content_type='application/json')
            ]
        )
        # Make the request
        response = self.service.delete(SomeResource(SOME_RESOURCE_AS_JSON))

        # Assertions
        self.assertEqual(response.as_json(), expected_response)
        self.assertEqual(isinstance(response, SomeResource), True)