# pip install git+https://github.com/truenas/api_client.git
from truenas_api_client import Client

import json
import ssl
import time

config_file_path = "./config.json"

try:
    with open (config_file_path, 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file '{config_file_path}' was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{config_file_path}'. Check for syntax errors.")
    exit()

username = config_data["truenas_api_username"]
key = config_data["truenas_api_key"]
url = config_data["truenas_api_url"]
prefix = config_data["cert_name_prefix"]
private_key = config_data["private_key_file"]
certificate = config_data["certificate_file"]

try:
    with Client(url) as client:
        resp = client.call("auth.login_ex", {
            "mechanism": "API_KEY_PLAIN",
            "username": username,
            "api_key": key
        })
        assert resp["response_type"] == "SUCCESS"

        cert_name_new = f"{prefix}{int(time.time())}"
        with open(certificate, 'r') as file:
            cert_data = file.read()
        with open(private_key, 'r') as file:
            key_data = file.read()
        resp = client.call('certificate.create', {"name":cert_name_new,"create_type":"CERTIFICATE_CREATE_IMPORTED","certificate":cert_data,"privatekey":key_data}, job=True)
        new_cert_id = resp["id"]
        print(f"Created new cert with ID: {new_cert_id} and name: {cert_name_new}")

        resp = client.call('system.general.update',{"ui_certificate":new_cert_id})
        assert resp["ui_certificate"]["id"] == new_cert_id
        print(f"Switched UI to cert with ID: {resp["ui_certificate"]["id"]}")

        resp = client.call('certificate.query', [["name","^",prefix]])
        for cert in resp:
            if cert['id'] != new_cert_id:
                client.call('certificate.delete', cert['id'], job=True)
                print(f"Deleted old cert with ID: {cert['id']}")

except Exception as e:
    print(f"An error occurred: {e}")
    print(e.__traceback__)
