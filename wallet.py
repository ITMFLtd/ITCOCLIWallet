#!/usr/bin/python
import rpc
import sys
import click
import qrcode
import config
import utils


@click.group()
def cli():
    pass

@cli.group()
def wallet():
    pass

@cli.group()
def account():
    pass


@cli.command()
def status():
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    wallet_info = rpc.wallet_info(config.get("wallets")[wallet])
    print(wallet + ":")
    print("Balance: " + wallet_info["balance"] + " ITCO")
    print("Pending: " + wallet_info["pending"] + " ITCO")
    print("Number of accounts: " + wallet_info["accounts_count"])
    print()


@cli.command()
def send():
    print("Please enter the address of the account you'd like to send from")
    sender = click.prompt("")
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    accounts = rpc.wallet_balances(utils.get_wallet_from_name(wallet))["balances"].keys()
    matches = [x for x in accounts if x.startswith(sender)]
    if not matches:
        print("Could not locate any account addresses in the currently selected wallet that match the entry.")
        return
    if len(matches) > 1:
        print("Multiple matches were found for your given query. Please be more specific.")
        for match in matches:
            print(match)
        return
    match = matches[0]
    print("Found a match based on your input: " + match)
    if not click.confirm("Is this correct"):
        print("Aborting...")
        return
    print("Please enter the address of the account you'd like to send to")
    recv = click.prompt("")
    balance = int(rpc.account_balance(match)["balance"])
    print("You currently have " + str(balance) + " ITCO available to send.")
    amount = click.prompt("How much would you like to send", type=int)
    if amount > balance:
        print("The amount entered was higher than your available balance!")
        return
    print("You are about to send " + str(amount) + " ITCO from " + match + " to " + recv)
    print("Please triple check your target address and amount. This action is NOT reversible.")
    if not click.confirm("Is this correct"):
        print("Aborting...")
        return
    response = rpc.send(utils.get_wallet_from_name(wallet), match, recv, amount)
    if 'error' in response.keys():
        print('An error occurred during sending: ' + response['error'])
        return
    print("Transaction sent in block: " + response['block'])


@account.command(name="qr")
@click.argument("account")
def qr(account):
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    accounts = rpc.wallet_balances(utils.get_wallet_from_name(wallet))["balances"].keys()
    matches = [x for x in accounts if x.startswith(account)]
    if not matches:
        print("Could not locate any account addresses in the currently selected wallet that match the entry.")
        return
    if len(matches) > 1:
        print("Multiple matches were found for your given query. Please be more specific.")
        for match in matches:
            print(match)
        return
    match = matches[0]
    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_Q)
    qr.add_data(match)
    qr.print_ascii()


@account.command(name="new")
def new_account():
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    account = rpc.create_account(utils.get_wallet_from_name(wallet))['account']
    print("New account created: " + account)


@account.command(name="list")
@click.option("--verbose", "-v", is_flag=True, default=False)
def list_account(verbose):
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    wallet_balances = rpc.wallet_balances(config.get("wallets").get(wallet))
    for account, balances in wallet_balances["balances"].items():
        print(account + (":" if verbose else ""))
        if verbose:
            print("Balance: " + balances["balance"] + " ITCO")
            print("Pending: " + balances["pending"] + " ITCO")
            print()


@account.command(name="history")
@click.argument("account")
def history(account):
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    accounts = rpc.wallet_balances(config.get("wallets").get(wallet))["balances"].keys()
    matches = [x for x in accounts if x.startswith(account)]
    if not matches:
        print("Could not locate any account addresses in the currently selected wallet that match the entry.")
        return
    if len(matches) > 1:
        print("Multiple matches were found for your given query. Please be more specific.")
        for match in matches:
            print(match)
        return
    match = matches[0]
    history = rpc.history(match)["history"]
    if not history:
        print("No history available for this account.")
        return
    print("History for account: " + match)
    for transaction in history:
        print(transaction['type'] + " " + transaction['amount'] + " ITCO to/from " + transaction['account'])


@wallet.command()
@click.argument('wallet')
def set(wallet):
    if wallet in config.get("wallets"):
        config.conf["selected_wallet"] = wallet
        config.save_json_file()
        print("Your selected wallet is now " + wallet)
    else:
        print("Could not find a wallet with that name. Check your config.json.")


@wallet.command(name="list")
@click.option("--verbose", "-v", is_flag=True, default=False)
def list_wallet(verbose):
    wallets = config.get("wallets")
    for wallet in wallets:
        print(wallet + ": " + wallets[wallet])
        if verbose:
            wallet_info = rpc.wallet_info(wallets[wallet])
            print("Balance: " + wallet_info["balance"] + " ITCO")
            print("Pending: " + wallet_info["pending"] + " ITCO")
            print("Number of accounts: " + wallet_info["accounts_count"])
            print()


@wallet.command(name="selected")
def selected_wallet():
    wallet = utils.get_selected_wallet()
    if wallet is None:
        return
    print("Currently selected wallet is: " + wallet)
    print("Wallet ID: " + config.get("wallets")[wallet])


def main():
    config.init_config()
    if rpc.post("{}") is None:
        print("Failed to connect to ITCO node. Make sure node is running with correct config.")
        sys.exit(1)
    if not config.get("wallets"):
        print("There are no wallets associated with this account. Creating one now...")
        wallet = rpc.create_wallet()['wallet']
        config.get("wallets")["main"] = wallet
    cli()


if __name__ == "__main__":
    main()
