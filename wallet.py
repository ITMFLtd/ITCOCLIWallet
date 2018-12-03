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



"""
def main():
    global wallet
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            rpc.TESTING_MODE = True
        else:
            print("Invalid argument(s) passed.")
    print(term.enter_fullscreen)
    gui.show_splash_screen(term)
    if rpc.post("{}") is None:
        print("Failed to connect to ITCO node. Make sure node is running with correct config.")
        sys.exit(1)

    config.touch_file(WALLET_FILE)
    if rpc.TESTING_MODE:
        wallets = {"main":
                       "1228F21VOIDE839C9D9CTEST775E148D00634F6TESTE84948F092EE209D32A96"}
    else:
        wallets = config.load_json_file(WALLET_FILE)

    if wallets is None:
        print("No wallet could be detected. Creating one for you...")
        wallet = rpc.create_wallet()['wallet']
        with open(WALLET_FILE, 'w') as f:
            json.dump({"main": wallet}, f)

    wallet_name = gui.gui_select_from(term, list(wallets.keys()), prompt='Select the wallet you want to use:')
    wallet = wallets[wallet_name]

    print(term.clear)
    print("Opened wallet.")
    print()
    balances = rpc.wallet_balances(wallet)['balances']
    for balance in balances:
        print("Balance: " + balances[balance]['balance'] + " ITCO \nAddress: " + balance)

    # Begin main loop

    while True:
        print(term.move(term.height - term.get_location(timeout=5)[1] - 1, 0))
        command = input(term.bold(term.red("ITCO Wallet") + " > "))
        if not command:
            print("No command entered.")
            continue
        if command == "help":
            print("help".ljust(15) + "Prints this help page.")
            print("balances".ljust(15) + "Lists your accounts and balances.")
            print("clear".ljust(15) + "Clears your current wallet page to clean it up.")
            print("history".ljust(15) + "Shows a list of recent transactions.")
            print("receive".ljust(15) + "Select address and show QR")
            print("send".ljust(15) + "Send ITCO to another account.")
            print("quit/exit".ljust(15) + "Exits wallet")
        elif command == "balances":
            print(term.clear)
            balances = rpc.wallet_balances(wallet)['balances']
            for balance in balances:
                print("Balance: " + balances[balance]['balance'] + " ITCO \nAddress: " + balance)
        elif command == "send":
            options = []
            balances = rpc.wallet_balances(wallet)['balances']
            for balance in balances:
                options.append(balance)
            src = gui.gui_select_from(term, options, prompt='Select your account to send from.')
            dest = input("Enter the address to send to\n> ").strip()
            if 'error' in rpc.account_balance(dest).keys():
                print("Invalid ITCO address entered.")
                continue
            amount = input("Send amount: ")
            if amount > balances[src]['balance']:
                print("Send amount higher than account balance!")
                continue
            print("Really send " + amount + " ITCO to " + dest + "? (y/n)")
            with term.cbreak():
                key = term.inkey()
            if key == 'y':
                response = rpc.send(wallet, src, dest, amount)
                if 'error' in response.keys():
                    print('An error occurred during sending: ' + response['error'])
                    continue
                print("Transaction sent in block: " + response['block'])
                continue
            print("Transaction cancelled.")
        elif command == "history":
            options = []
            balances = rpc.wallet_balances(wallet)['balances']
            for balance in balances:
                options.append(balance)
            account = gui.gui_select_from(term, options, prompt='Select your account to check history.')
            history = rpc.history(account)
            for transaction in history['history']:
                print(transaction['type'] + " " + transaction['amount'] + " ITCO to/from " + transaction['account'])
        elif command == "receive":
            options = []
            balances = rpc.wallet_balances(wallet)['balances']
            for balance in balances:
                options.append(balance)
            account = gui.gui_select_from(term, options, prompt='Select the account you wish to receive from.')
            if account == "New":
                break
            qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_Q)
            qr.add_data(account)
            qr.print_ascii()
        elif command == "new_account":
            print("New account created: " + rpc.create_account(wallet)['account'])
        elif command == "quit" or command[0] == "exit":
            print(term.clear)
            exit(0)
        elif command == "clear":
            print(term.clear)
        else:
            print("Command not found, try using the help command.")
"""

if __name__ == "__main__":
    main()
