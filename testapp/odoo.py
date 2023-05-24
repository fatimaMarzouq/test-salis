import json
import random

import requests


def get_odoo_version(url):
    xmlrpc_url = '{}/jsonrpc/'.format(url)
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "version",
            "args": {},
        },
        "id": None,
    }
    response = requests.post(xmlrpc_url, json=data)
    if response.status_code == 200:
        result = response.json().get("result")
        if result:
            return result
        else:
            return "Error: Empty response from Odoo server"
    else:
        return "Error: Failed to connect to Odoo server"
    

def authenticate_odoo_user(url, *args):
    xmlrpc_url = '{}/jsonrpc/'.format(url)
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "login",
            "args": args,
        },
        "id": None,
    }
    response = requests.post(xmlrpc_url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    # print(response.content)
    # print("Response Status Code:", response.status_code)
    # print("Response Content:", response.json())
    if response.status_code == 200:
        result = response.json().get("result")
        if result:
            return result
        else:
            return "Error: Authentication failed"
    else:
        return "Error: Failed to connect to Odoo server"


def execute_odoo_method(url, db, uid, password, model, method, args=None, kwargs=None):
    endpoint = '{}/jsonrpc'.format(url)
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [db, uid, password, model, method, args or [], kwargs or {}],
            "kwargs": {},
        },
        "id": None
    }
    response = requests.post(endpoint, json=data)
    print(response.json())
    if response.status_code == 200:
        try:
            result = response.json().get("result")
            return result
        except ValueError:
            return "Error: Invalid JSON response from Odoo server"
    else:
        return "Error: Failed to connect to Odoo server"
