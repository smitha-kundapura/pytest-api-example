from jsonschema import validate
import pytest
import schemas
import api_helpers
import random
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

'''
Test to verify the PATCH request for updating an order by ID.
Here, I have used the fixture get_new_order_id to create a new order and get the order ID.
This test will update the order status to "pending" and validate the response.'''
def test_patch_order_by_id_with_fixture(get_new_order_id):
    order_id = get_new_order_id
    status = "pending"
    patch_data = {
        "status": status
    }
    test_endpoint = f"/store/order/{order_id}"
    response = api_helpers.patch_api_data(test_endpoint, patch_data)
    resp_json = response.json()
    print(resp_json["message"])
    
    # Validate the response status code for 200 with message containing "Order and pet status updated successfully"
    assert response.status_code == 200
    assert_that(resp_json["message"], contains_string("Order and pet status updated successfully"))
    # Validate the order object if present in response
    if "order" in resp_json:
        order = resp_json["order"]
        assert_that(order["id"], is_(order_id))
        assert_that(order["status"], is_(status))


'''Test to verify cases when order is not found. 
Here, I have hard Coded 1 as it has pending pending. 
Might create fixture for pending pets if required.'''
def test_patch_order_by_id_error():
    patch_data = {
        "status": "delivered"
    }
    test_endpoint = f"/store/order/1" #Hard Coded 1 as it has pending pending. Might create fixture for pending pets if required.
    response = api_helpers.patch_api_data(test_endpoint, patch_data)
    resp_json = response.json()
    print(resp_json["message"])
    #Validate the response status code for 404 with message containing "Order not found. You have requested"
    assert response.status_code == 404
    assert_that(resp_json["message"], contains_string("Order not found"))
    

'''
Fixture to create a new order with a unique pet_id.
This fixture will create a new pet and then create an order for that pet.
This will ensure that the order_id is unique for each test run.'''
@pytest.fixture
def get_new_order_id():
    # Create new pet with unique pet_id 
    pet_id = random.randint(1, 1000)
    pet_data = {
        "id": pet_id,
        "name": f"TestPet{pet_id}",
        "type": "dog",
        "status": "available" 
    }
    test_endpoint = "/pets/"
    response = api_helpers.post_api_data(test_endpoint, pet_data)
    resp_json = response.json()
    assert response.status_code == 201
    assert resp_json["id"] == pet_id

    #Create an order for the newly created pet
    order_data = {
        "pet_id": pet_id,
        "quantity": 1,
        "status": "available",
        "shipDate": "2023-10-01T00:00:00Z",
        "complete": True
    }
    test_endpoint = "/store/order"
    order_response = api_helpers.post_api_data(test_endpoint, order_data)
    order_resp_json = order_response.json()
    assert order_response.status_code == 201
    assert order_resp_json["pet_id"] == pet_id
    # Validate the order schema
    validate(instance=order_resp_json, schema=schemas.order)
    print(f"Created order with ID: {resp_json['id']} for pet ID: {pet_id}")
    return order_resp_json["id"]