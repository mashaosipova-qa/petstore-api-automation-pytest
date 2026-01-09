import pytest
from api import Pets

@pytest.fixture
def api_object():
    api_obj = Pets()
    yield api_obj

    print("Cleaning up ...")
    api_obj.clean_up()