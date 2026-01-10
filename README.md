# Automated API Tests for the Pet Application

This project implements automated API tests for a pet management service using **Python**, **Pytest** and the **Requests** library.

### Project Structure:

* `api.py` – Library of API methods
* `test_pets.py` – Test suite that validates logic for pets and users, including HTTP Method Validation
* `conftest.py` – Contains the `api_object` fixture that automatically creates a Pets API instance and performs cleanup after each test


### Running Tests:

* `pytest tests/test_pets.py -v` – Run all tests with verbose output (`-v`), showing each test name and result.
* `pytest tests/test_pets.py -s -v` – Runs tests with verbose output (`-v`) and displays print statements.

---
### Short Test discriptions:
#### User and Authentication Tests

* `test_get_token` - Verify authenticated user can generate valid access token
* `test_get_registered_user` – Verify new user can register with valid credentials
* `test_list_users` – Verify authenticated user can retrieve list of users
* `test_delete_user` – Verify user can be deleted and subsequently blocked from logging in

#### Pet Management Tests
* `test_create_pet` – Verify authenticated user can successfully create a new pet
* `test_get_pet_by_id` – Verify user can retrieve pet by its ID
* `test_update_pet` – Verify user can update pet information like name, type, and age
* `test_delete_pet` – Verify user can delete pet and confirm it no longer exists
* `test_get_pet_photo` – Verify user can upload photo to an existing pet
* `test_add_like_to_pet` – Verify user can add a like to a pet
* `test_add_comment_to_pet` – Verify user can add a comment to a pet

#### API Method Validation Tests
* `test_check_GET_PET_ID_not_support_other_method` – Verify that /pet/{id} accepts methods GET/DELETE and rejects methods POST/PUT/PATCH **[parametrized test]**


