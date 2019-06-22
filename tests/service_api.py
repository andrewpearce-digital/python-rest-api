import requests
import os

# service_url = 'http://localhost:5000'
service_url = os.getenv('SERVICE_URL', 'http://localhost:5000')


def get_root():
    response = requests.get(service_url)
    print(response)
    return response


def get_items():
    response = requests.get(service_url+'/items')
    print(response)
    return response


def post_items(identifier, name):
    response = requests.post(
        service_url+'/items', data={'identifier': identifier, 'name': name})
    print(response)
    return response


def get_item(identifier):
    response = requests.get(service_url+'/item/{}'.format(identifier))
    print(response)
    return response


def delete_item(identifier):
    response = requests.delete(service_url+'/item/{}'.format(identifier))
    print(response)
    return response


print(service_url)
get_items()
