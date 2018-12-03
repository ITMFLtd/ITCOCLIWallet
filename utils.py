import config


def get_selected_wallet():
    wallet = config.get("selected_wallet")
    if not wallet:
        print("No wallet has been selected. Try \"wallet.py wallet\"")
        return None
    return wallet
