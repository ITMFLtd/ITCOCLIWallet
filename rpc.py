import requests
import json

RPC_ADDRESS = "http://localhost:1761"


def account_balance(account):
    data = {
        "action": "account_balance",
        "account": account
    }
    return post(data).json()


def wallet_balances(wallet):
    data = {
        "action": "wallet_balances",
        "wallet": wallet
    }
    return post(data).json()


def wallet_info(wallet):
    data = {
        "action": "wallet_info",
        "wallet": wallet
    }
    return post(data).json()


def create_wallet():
    data = {
        "action": "wallet_create"
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
    return post(data).json()


def post(data):
    try:
        return requests.post(RPC_ADDRESS, data=json.dumps(data))
    except requests.exceptions.RequestException:
        return None
