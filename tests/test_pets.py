import pytest

def test_get_token(api_object):
    """Verify authenticated user can generate valid access token"""
    token, status, _ = api_object.generate_token()
    assert token, "Token is empty or None"
    assert status == 200,  f'Login failed (status {status})'

def test_list_users(api_object):
    """Verify authenticated user can retrieve list of users"""
    status, user_ids = api_object.get_list_users()
    assert status == 200, f'List users failed (status {status})'
    assert user_ids

def test_create_pet(api_object):
    """Verify authenticated user can successfully create a new pet"""
    pet_id, status = api_object.create_pet()
    assert status == 200, f'Create pet failed (status {status})'
    assert pet_id

def test_get_pet_photo(api_object):
    """Verify user can upload photo to existing pet"""
    pet_id, _ = api_object.create_pet()
    status, link = api_object.get_pet_photo(pet_id)
    assert status == 200, f'Get pet photo failed (status {status})'
    assert link

def test_add_like_to_pet(api_object):
    """Verify user can add like to a pet"""
    pet_id, _ = api_object.create_pet()
    status = api_object.add_like_to_pet(pet_id)
    assert status == 200, f'Add like to pet failed (status {status})'

def test_add_comment_to_pet(api_object):
    """Verify user can add comment to a pet"""
    pet_id, _ = api_object.create_pet()
    status, pet_id = api_object.add_comment_to_pet(pet_id)
    assert status == 200, f'Add comment to pet {pet_id} failed (status: {status})'

def test_get_pet_by_id(api_object):
    """Verify user can retrieve pet by its ID"""
    created_pet_id, _ = api_object.create_pet() # ID of created pet
    found_pet_id, status = api_object.get_pet_by_id(created_pet_id)
    assert status == 200, f'Get pet by id failed (status {status})'
    assert found_pet_id == created_pet_id, f'ID mismatch: created {created_pet_id}, found {found_pet_id}'


def test_delete_pet(api_object):
    """Verify user can delete pet"""
    pet_id, _ = api_object.create_pet()
    pet_id, status = api_object.delete_pet(pet_id)
    assert status == 200, f'DELETE pet {pet_id} failed (status: {status})'
    _, status_after_delete = api_object.get_pet_by_id(pet_id)
    assert status_after_delete == 404, f'Pet {pet_id} still exists (status: {status_after_delete})'

def test_get_registered_user(api_object):
    """Verify new user can register with valid credentials"""
    user_id, status, _, _ = api_object.get_registered_user()
    assert status == 200, f'Registration failed (status {status})'
    assert isinstance(user_id, int),  f'ID is not integer'
    assert user_id > 0, f'Invalid user ID: {user_id}'


def test_delete_user(api_object):
    """Verify user can be deleted"""
    user_id_for_delete, status_before, email, password = api_object.get_registered_user()
    user_id, status, email, password = api_object.delete_user(user_id_for_delete, email, password)
    assert status == 200, f'Delete user failed (status {status})'
    status_after = api_object.check_user_deleted(email, password)
    assert status_after == 400, f'Deleted user still can login (status: {status_after})'


def test_update_pet(api_object):
    """Verify user can update pet information"""
    pet_id, _ = api_object.create_pet()
    pet_id, status, updated_pet = api_object.update_pet(pet_id)
    assert status == 200, f'Update pet failed (status {status})'

    updated_pet, status = api_object.verify_pet_updated(pet_id)
    assert status == 200, f'Update pet failed (status {status})'
    assert 'UPDATEDpet_' in updated_pet['name'], f'Name not updated: {updated_pet["name"]}'
    assert updated_pet['type'] == 'dog', f'Type wrong: {updated_pet["type"]}'
    assert updated_pet['age'] == 1, f'Age wrong: {updated_pet["age"]}'
    assert updated_pet['id'] == pet_id, 'ID mismatch'

@pytest.mark.parametrize(
    "method, expected_status_code",
    [
        ("GET", 200),
        ("POST", 405),
        ("PATCH", 405),
        ("PUT", 405),
        ("DELETE", 200),
    ],
)
def test_check_GET_PET_ID_not_support_other_method(api_object, method, expected_status_code):
    """Verify that /pet/{id} accepts methods GET/DELETE and rejects methods POST/PUT/PATCH"""
    pet_id, _ = api_object.create_pet()
    response = api_object.call_pet_endpoint_with_specific_method(method, pet_id)
    assert response.status_code == expected_status_code, f'Not expected ({expected_status_code}) status code - {response.status_code}'