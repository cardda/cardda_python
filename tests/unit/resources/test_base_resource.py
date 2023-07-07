import unittest
from cardda_python.resources import BaseResource, BankAccount


class SomeResource(BaseResource):
    name="something"
    allowed_nested_attributes=["nested_object", "other_object"]
    nested_objects={ "other_object" : "BankAccount"}

SOME_RESOURCE_AS_JSON = {
    "id": "1",
    "some_field": "some_value",
    "other_field": "other_value",
    "nested_object": {
        "nested_field": "nested_value"
    }
}

class TestBaseResource(unittest.TestCase):
    
    def test_init(self):
        resource = SomeResource(SOME_RESOURCE_AS_JSON)

        self.assertEqual(resource.id, SOME_RESOURCE_AS_JSON["id"])
        self.assertEqual(resource.some_field, SOME_RESOURCE_AS_JSON["some_field"])
        self.assertEqual(resource.other_field, SOME_RESOURCE_AS_JSON["other_field"])
        self.assertDictEqual(resource.nested_object, SOME_RESOURCE_AS_JSON["nested_object"])
    
    def test_overwrite(self):
        resource = SomeResource(SOME_RESOURCE_AS_JSON)
        new_data = {"new_field": "new_value"}
        resource.overwrite(new_data)

        self.assertRaises(AttributeError, lambda: resource.id)
        self.assertRaises(AttributeError, lambda: resource.some_field)
        self.assertRaises(AttributeError, lambda: resource.other_field)
        self.assertRaises(AttributeError, lambda: resource.nested_object)
        self.assertEqual(resource.new_field, new_data["new_field"])
    
    def test_objectize(self):
        new_data = {**SOME_RESOURCE_AS_JSON, "other_object": {"custom_id": "custom_id_value"}}
        resource = SomeResource(new_data)

        self.assertEqual(isinstance(resource.other_object, BankAccount), True)
        self.assertEqual(resource.other_object.custom_id, new_data["other_object"]["custom_id"])
        self.assertDictEqual(resource.as_json(), new_data)


