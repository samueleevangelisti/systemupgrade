'''
requestss.py
'''
import requests

from utils.configs.requestss import configs
from utils import logs



def _request(method, url, headers, json):
    '''
    Basic request

    Parameters
    ----------
    method : str
        Http method
    url : str
        Url
    headers : dict | None
        Headers
    json : dict | None
        Json payload
    
    Returns
    -------
    response
    '''
    logs.request(f'method: {method}, url: {url}, headers: {headers}, json: {json}')
    response = None
    match method:
        case 'GET':
            response = requests.get(url, headers=headers, json=json, timeout=configs.TIMEOUT)
        case 'POST':
            response = requests.get(url, headers=headers, json=json, timeout=configs.TIMEOUT)
        case 'PUT':
            response = requests.get(url, headers=headers, json=json, timeout=configs.TIMEOUT)
        case 'PATCH':
            response = requests.get(url, headers=headers, json=json, timeout=configs.TIMEOUT)
        case 'DELETE':
            response = requests.get(url, headers=headers, json=json, timeout=configs.TIMEOUT)
    if response.status_code != 200:
        logs.request_error(f'response.status_code: {response.status_code}, response.text: {response.text}')
    else:
        logs.request_error(f'response.status_code: {response.status_code}, response.text: {response.text}')
    return response



def get(url, headers=None):
    '''
    Get request

    Parameters
    ----------
    url : str
        Url
    headers : dict | None
        Headers

    Returns
    -------
    response
    '''
    return _request('GET', url, headers, None)



def post(url, headers=None, json=None):
    '''
    Post request

    Parameters
    ----------
    url : str
        Url
    headers : dict | None
        Headers
    json : dict | None
        Json payload

    Returns
    -------
    response
    '''
    return _request('POST', url, headers, json)



def put(url, headers=None, json=None):
    '''
    Put request

    Parameters
    ----------
    url : str
        Url
    headers : dict | None
        Headers
    json : dict | None
        Json payload

    Returns
    -------
    response
    '''
    return _request('PUT', url, headers, json)



def patch(url, headers=None, json=None):
    '''
    Patch request

    Parameters
    ----------
    url : str
        Url
    headers : dict | None
        Headers
    json : dict | None
        Json payload

    Returns
    -------
    response
    '''
    return _request('PATCH', url, headers, json)



def delete(url, headers=None, json=None):
    '''
    Delete request

    Parameters
    ----------
    url : str
        Url
    headers : dict | None
        Headers
    json : dict | None
        Json payload

    Returns
    -------
    response
    '''
    return _request('DELETE', url, headers, json)
