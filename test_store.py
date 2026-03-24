from jsonschema import validate, ValidationError
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id} ✅ DONE
2) *Optional* Consider using @pytest.fixture to create unique test data for each run ✅ DONE
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test ✅ DONE
3) Validate the response codes and values ✅ DONE
4) Validate the response message "Order and pet status updated successfully" ✅ DONE
'''
@pytest.fixture
def create_order():
    """Fixture to create an order for testing"""
    order_data = {'pet_id': 0}  # Using available pet from initial data
    response = api_helpers.post_api_data('/store/order', order_data)
    assert response.status_code == 201
    order = response.json()
    # Validate the order matches the schema
    try:
        validate(instance=order, schema=schemas.order)
        schema_valid = True
        schema_error = None
    except ValidationError as e:
        schema_valid = False
        schema_error = str(e)
    
    assert schema_valid, f"Order schema validation failed: {schema_error}"
    return order


def test_patch_order_by_id(create_order):
    """Test PATCH /store/order/{order_id} with valid status updates"""
    order = create_order
    order_id = order['id']
    
    # Test updating to pending status
    update_data = {'status': 'pending'}
    response = api_helpers.patch_api_data(f'/store/order/{order_id}', update_data)
    
    # Validate response code
    assert response.status_code == 200
    
    # Validate response message
    response_data = response.json()
    assert_that(response_data['message'], contains_string("Order and pet status updated successfully"))


@pytest.mark.parametrize("status", [("available"), ("sold"), ("pending")])
def test_patch_order_status_updates(status):
    """Test PATCH /store/order/{order_id} with various status updates"""
    # First, create an order
    order_data = {'pet_id': 0}
    response = api_helpers.post_api_data('/store/order', order_data)
    assert response.status_code == 201
    order = response.json()
    order_id = order['id']
    
    # Update with different status
    update_data = {'status': status}
    response = api_helpers.patch_api_data(f'/store/order/{order_id}', update_data)
    
    # Validate response code
    assert response.status_code == 200
    
    # Validate response message
    response_data = response.json()
    assert_that(response_data['message'], contains_string("Order and pet status updated successfully"))


def test_patch_order_invalid_order_id():
    """Test PATCH /store/order/{order_id} with non-existent order"""
    invalid_order_id = "invalid-uuid-12345"
    update_data = {'status': 'sold'}
    
    response = api_helpers.patch_api_data(f'/store/order/{invalid_order_id}', update_data)
    
    # Validate 404 response
    assert response.status_code == 404
    error_data = response.json()
    assert_that(error_data['message'], contains_string("Order not found"))


def test_patch_order_invalid_status():
    """Test PATCH /store/order/{order_id} with invalid status"""
    # First, create an order
    order_data = {'pet_id': 0}
    response = api_helpers.post_api_data('/store/order', order_data)
    assert response.status_code == 201
    order = response.json()
    order_id = order['id']
    
    # Try to update with invalid status
    update_data = {'status': 'invalid_status'}
    response = api_helpers.patch_api_data(f'/store/order/{order_id}', update_data)
    
    # Validate 400 response
    assert response.status_code == 400
    error_data = response.json()
    assert_that(error_data['message'], contains_string("Invalid status"))