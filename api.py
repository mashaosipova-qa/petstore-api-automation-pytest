import requests
import datetime
import uuid

from requests import Response

from settings import VALID_EMAIL, VALID_PASSWORD, VALID_EMAIL_TEMPLATE, BASE_URL

class Pets:
    """API library for http://34.141.58.52:8000/#/ """

    def __init__(self):
        self.base_url = BASE_URL
        self.pets_to_cleanup = [] # Create an empty list to track pets that need to be removed after testing
        self.session = requests.Session() # Create session
        _, _, _ = self.generate_token()
        self.user_id = None

    def generate_token(self) -> tuple:
        """Authenticate once and store token in session for all subsequent requests (Endpoint: POST /login)"""
        data = {'email': VALID_EMAIL, 'password': VALID_PASSWORD}
        res = self.session.post(self.base_url + "login", json=data)
        if res.status_code == 200:
            token = res.json()['token']
            self.user_id = res.json()['id']
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            return token, res.status_code, self.user_id
        return None, res.status_code, None

    def get_list_users(self) -> tuple:
        """Retrieve list of users (Endpoint: GET /users)"""
        res = self.session.get(self.base_url + "users")
        return res.status_code, res.json()

    def create_pet(self) -> tuple:
        """Add new pet (Endpoint: POST /pet)"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_name = f"Professor_{timestamp}"
        data = {'name' : unique_name, 'type' : 'cat', 'age' : 9, 'owner_id' : self.user_id}
        res = self.session.post(self.base_url + "pet", json=data)
        pet_id = res.json()['id']
        status = res.status_code
        print(pet_id)
        self.pets_to_cleanup.append(pet_id)
        return pet_id, status

    def get_pet_photo(self, pet_id) -> tuple:
        """Upload pet photo (Endpoint: POST /pet/{id}/image)"""
        pic_file = open('tests/photo/14.jpg', 'rb')
        try:
            files = {'pic': ('test.jpg', pic_file, 'image/jpeg')}
            res = self.session.post(self.base_url + f'pet/{pet_id}/image', files=files)
            status = res.status_code
            link = res.json()['link']
            return status, link
        finally:
            pic_file.close()

    def add_like_to_pet(self, pet_id) -> int:
        """Add like to pet (Endpoint: PUT /pet/{id}/like)"""
        res = self.session.put(self.base_url + f'pet/{pet_id}/like')
        status = res.status_code
        return status

    def get_pet_by_id(self, pet_id) -> tuple:
        """Retrieve pet details by pet ID (Endpoint: GET /pet/{id})"""
        res = self.session.get(self.base_url + f'pet/{pet_id}')
        status = res.status_code
        found_pet_id = res.json()['pet']['id'] if status == 200 else None
        return found_pet_id, status

    def delete_pet(self, pet_id) -> tuple:
        """Delete pet by id (Endpoint: DELETE /pet/{id})"""
        res = self.session.delete(self.base_url + f'pet/{pet_id}')
        status = res.status_code
        return pet_id, status

    def add_comment_to_pet(self, pet_id) -> tuple:
        """Request to Swagger API to add comment with valid message (Endpoint: PUT /pet/{id}/comment)"""
        comment_data = {"message": "Test comment from API"}
        res = self.session.put(self.base_url + f'pet/{pet_id}/comment', json=comment_data)
        status = res.status_code
        return status, pet_id

    def get_registered_user(self) -> tuple:
        """Request to Swagger API to register new user (Endpoint: POST /register)"""
        e = uuid.uuid4().hex[:8]
        email = VALID_EMAIL_TEMPLATE.format(e)
        password = VALID_PASSWORD
        data = {'email': email, 'password': password, 'confirm_password': password}
        res = requests.post(self.base_url + 'register', json=data)
        my_id = res.json()['id']
        status = res.status_code
        print(my_id)
        return my_id, status, email, password

    def delete_user(self, user_id_for_delete, email, password) -> tuple:
        """Delete user by ID (Endpoint: DELETE /users/{id})"""
        data = {'email': email, 'password': password}
        res = requests.post(self.base_url + "login", json=data)
        my_token = res.json()['token']
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.delete(self.base_url + f'users/{user_id_for_delete}', headers=headers)
        status_after = res.status_code
        return user_id_for_delete, status_after, email, password

    def check_user_deleted(self, email, password) -> int:
        """Verify deleted user cannot login (Endpoint: POST /login)"""
        data = {'email' : email, 'password' : password}
        res = requests.post(self.base_url + 'login', json=data)
        status = res.status_code
        return status

    def update_pet(self, pet_id) -> tuple:
        """Update pet partially (Endpoint: PATCH /pet)"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        updated_name = f'UPDATEDpet_{timestamp}'
        updated_pet = {'id' : pet_id, 'name' : updated_name, 'type': 'dog', 'age': 1}
        res_patch = self.session.patch(self.base_url + 'pet', json=updated_pet)
        status_after_update = res_patch.status_code
        print(updated_pet)
        return pet_id, status_after_update,updated_pet

    def verify_pet_updated(self, pet_id) -> tuple:
        """Check pet data updated correctly (Endpoint: Get /pet/{id})"""
        res = self.session.get(self.base_url + f'pet/{pet_id}')
        status = res.status_code
        if status == 200:
            pet_data = res.json()['pet']
        else:
            pet_data = None
        return pet_data, status

    def call_pet_endpoint_with_specific_method(self, method, pet_id) -> Response:
        """Make HTTP request to /pet/{id} endpoint with given method for method validation testing"""
        return self.session.request(method=method, url=f"{self.base_url}/pet/{pet_id}")

    def clean_up(self):
        for pet_id in self.pets_to_cleanup:
            try:
                self.delete_pet(pet_id)
                print(f"Pet #{pet_id} deleted")
            except Exception as e:
                print(f"Pet #{pet_id} delete failed (reason: {e})")
