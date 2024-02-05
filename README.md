
### foundation.app

[CVE ID]
CVE-2023-50053

[Description]
In the Web3 authentication process of Foundation, the signed message lacks a nonce (random number), leading to replay attacks.

[Vendor of Product]
Foundation.app

[Affected Product Code Base]
Foundation platform - 1.0

[Vulnerability Type Other]
Replay Attack

[Reference]
https://foundation.app/

---
Foundation.app's message structure is vulnerable due to the absence of a nonce. 
This omission exposes the Web3 authentication process to replay attacks.

Message example:
```
Please sign this message to connect to Foundation.
```

### galxe.com

[CVE ID]
CVE-2023-50059

[Description]
In the Web3 authentication process of Galxe, the server does not check the random number, leading to replay attacks.

[Vendor of Product]
galxe.com

[Affected Product Code Base]
Galxe platform - 1.0

[Vulnerability Type Other]
Replay Attack

[Reference]
https://galxe.com

---

The galxe.com's message includes a `Nonce` and `Expiration Time`. However, our findings indicate that the server fails to verify these details. 
Therefore, once an attacker obtains a user's signature, they can replay the signature and gain access to the user's account.

Message example:

```
galxe.com wants you to sign in with your Ethereum account:
0x36E7C6FeB20A90b07F63863D09cC12C4c9f39064

Sign in with Ethereum to the app.

URI: https://galxe.com
Version: 1
Chain ID: 1
Nonce: WyiTj2tJ8VGfWzx6L
Issued At: 2023-04-12T10:56:11.158Z
Expiration Time: 2023-04-13T10:56:11.149Z
Not Before: 2023-04-13T10:56:11.149Z
```


# Web3 Authentication Replay Attacks

## Web3 Authentication

Web3 Authentication operates on a challenge-response mechanism. In essence, during the authentication process, users employ their crypto wallets to sign a specific message generated by the website. Once the website verifies this signature, it ascertains the ownership of the corresponding address (public key, account), thereby authenticating the user's identity.

The process is outlined in the figure below:

1. The user accesses the website and clicks on "connect wallet." They then select the appropriate address (public key) to connect.
2. The user initiates Web3 authentication by clicking the "login button."
3. A "Signature Request Page" appears from the wallet, prompting the user to sign a message using the Personal Sign protocol ([EIP-191](https://eips.ethereum.org/EIPS/eip-191)).
4. After reviewing the message content, the user signs it.
5. The wallet sends the signature back to the website's front-end.
6. The front-end forwards the message, signature, and address (public key) to the server (back-end) for verification.
7. The server verifies these components and issues a token.
8. The browser receives the user token, completing the Web3 authentication process.



<img src="https://github.com/d0scoo1/Web3AuthRA/assets/13929425/d7e28a11-d0c0-4433-9411-13a8730a7b17" alt="Web3 Authentication" width=400/>


## Replay Attack

A secure message should incorporate a `nonce` or `timestamp` to prevent replay attacks. The server must check the message to ensure its legitimacy.

Without a nonce or proper server-side validation, an attacker could potentially use a previously obtained user signature to access the user's account by replaying the signature.




