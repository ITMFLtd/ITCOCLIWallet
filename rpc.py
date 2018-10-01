import requests
import json

RPC_ADDRESS = "http://localhost:1761"
TESTING_MODE = False


def account_balance(account):
    data = {
        "action": "account_balance",
        "account": account
    }
    if TESTING_MODE:
        return {
            "balance": "10000",
            "pending": "10000"
        }
    return post(data).json()


def wallet_balances(wallet):
    data = {
        "action": "wallet_balances",
        "wallet": wallet
    }
    if TESTING_MODE:
        return {
            "balances": {
                "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": {
                    "balance": "10000",
                    "pending": "10000"
                },
                "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi08008135": {
                    "balance": "10000",
                    "pending": "10000"
                }
            }
        }
    return post(data).json()


def wallet_info(wallet):
    data = {
        "action": "wallet_info",
        "wallet": wallet
    }
    if TESTING_MODE:
        return {
            "balance": "10000",
            "pending": "10000",
            "accounts_count": "3",
            "adhoc_count": "1",
            "deterministic_count": "2",
            "deterministic_index": "2"
        }
    return post(data).json()


def create_wallet():
    data = {
        "action": "wallet_create"
    }
    if TESTING_MODE:
        return {
            "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        }
    return post(data).json()


def send(wallet, src, dest, amount):
    data = {
        "action": "send",
        "wallet": wallet,
        "source": src,
        "destination": dest,
        "amount": amount
    }
    if TESTING_MODE:
        return {
            "block": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        }
    return post(data).json()


def history(account):
    data = {
        "action": "account_history",
        "account": account,
        "count": 10
    }
    if TESTING_MODE:
        return {
            "account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
            "history": [
                {
                    "type": "send",
                    "account": "xrb_38ztgpejb7yrm7rr586nenkn597s3a1sqiy3m3uyqjicht7kzuhnihdk6zpz",
                    "amount": "80000000000000000000000000000000000",
                    "hash": "80392607E85E73CC3E94B4126F24488EBDFEB174944B890C97E8F36D89591DC5"
                }
            ],
            "previous": "8D3AB98B301224253750D448B4BD997132400CEDD0A8432F775724F2D9821C72"
        }
    response = post(data).json()
    return response


def account_block_count(account):
    data = {
        "action": "account_block_count",
        "account": account
    }
    if TESTING_MODE:
        return {
            "block_count": "19"
        }
    return post(data).json()


def create_account(wallet):
    data = {
        "action": "account_create",
        "wallet": wallet
    }
    if TESTING_MODE:
        return {
            "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        }
    return post(data).json()


def post(data):
    if TESTING_MODE:
        return {}
    try:
        return requests.post(RPC_ADDRESS, data=json.dumps(data))
    except requests.exceptions.RequestException:
        return None
