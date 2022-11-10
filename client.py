import requests
r = requests.get("http://192.168.0.15/VendingSys_Server/Order/Scan/1/1")
print(r.text)