import requests
import base64
import json
import os

#supress TLS related warning.
requests.packages.urllib3.disable_warnings()

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

call_api = os.environ["CALL_API"]
url = os.environ["SERVER_URL"] + "/token"
clientid=os.environ["CLIENTID"]
secret=os.environ["SECRET"]
headers={'Authorization': 'Basic ' + base64.b64encode(clientid+':'+secret),'Content-Type': 'application/x-www-form-urlencoded'}
assertion=os.environ["ASSERTION"]
data = 'grant_type=urn:ietf:params:oauth:grant-type:saml2-bearer&assertion='+assertion

response = requests.post(url, data=data,headers=headers,verify=False)
print(response.text)

if (response.status_code == 200):
    json_data=json.loads(response.text)
    access_token=json_data['access_token']
    print('Access Token: ' + access_token)

    if (call_api == 'true'):
        api_ep = os.environ["API_EP"]
        api_headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(api_ep,headers=api_headers,verify=False)
        print(response.text)
else:
    print(response.text)
