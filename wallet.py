import os
import gui
import rpc
import config
import json
import sys
from blessed import Terminal

WALLET_FILE = "wallets.json"
splash = """  _____ _______ _____ ____  
 |_   _|__   __/ ____/ __ \ 
   | |    | | | |   | |  | |
   | |    | | | |   | |  | |
  _| |_   | | | |___| |__| |
 |_____|  |_|  \_____\____/ 
                            
                            """

wallet = None
term = Terminal()


def main():
    global wallet
    print(term.enter_fullscreen)
    with term.hidden_cursor():
        offset = 7
        for line in splash.splitlines():
            print(term.move_y(term.height // 2 - offset) +
                  term.center(line).rstrip())
            offset -= 1
        print(term.move_y(term.height // 2) +
              term.center(term.bold('Press Any Key to Continue')))
        with term.cbreak():
            term.inkey()
    print(term.clear)
    if rpc.post("{}") is None:
        print("Failed to connect to ITCO node. Make sure node is running with correct config.")
        sys.exit(1)

    config.touch_file(WALLET_FILE)

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
        elif command == "quit" or command[0] == "exit":
            print(term.clear)
            exit(0)
        elif command == "clear":
            print(term.clear)
        else:
            print("Command not found, try using the help command.")


if __name__ == "__main__":
    main()
