import requests, json
from . import SEARCH_PROJECT, GET_PROJECT

def is_slug_valid(project_name) -> json:
    req = requests.get(GET_PROJECT + project_name + "/check")
    if req.reason != 'OK':
        return
    return req.json()


def search_project(project_name, facets, index, offset, limit) -> json:
    if is_slug_valid(project_name) is None:
        return

    params = {'query': project_name, 'facets': facets, 'index': index, 'offset': offset, 'limit': limit}
    req = requests.get(SEARCH_PROJECT, params=params)
    if req.reason != 'OK':
        return
    return req.json()

def get_project(project_name) -> json:
    if is_slug_valid(project_name) is None:
        return

    req = requests.get(GET_PROJECT + project_name)
    if req.reason != 'OK':
        return
    return req.json()




# data = r.json()
# print(data)