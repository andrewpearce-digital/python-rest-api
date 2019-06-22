import service_api as service_api
from assertpy import assert_that


def test_get_root():
    response = service_api.get_root()
    print(response)
    assert_that(response.status_code == 200).is_true()


def test_get_items():
    response = service_api.get_items()
    print(response)
    assert_that(response.status_code == 200).is_true()


def test_post_items():
    response = service_api.post_items('first_item', 'First Item')
    print(response)
    assert_that(response.status_code == 201).is_true()


def test_get_item():
    service_api.post_items('second_item', 'Second Item')
    response = service_api.get_item('second_item')
    print(response)
    assert_that(response.status_code == 200).is_true()


def test_delete_item():
    service_api.post_items('third_item', 'Third Item')
    response = service_api.delete_item('third_item')
    print(response)
    assert_that(response.status_code == 204).is_true()
