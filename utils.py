import config


def get_selected_wallet():
    wallet = config.get("selected_wallet")
    if not wallet:
        print("No wallet has been selected. Try \"wallet.py wallet\"")
        return None
    return wallet


def get_wallet_from_name(name):
    wallets = config.get("wallets")
    if name in wallets:
        return wallets[name]
    return None
