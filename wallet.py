import os
from rpc import *
from config import *
import json
import sys
from blessed import Terminal

WALLET_FILE = "wallets.json"

wallet = None
term = Terminal()


def main():
    global wallet
    print(term.enter_fullscreen)
    print(term.move_y(term.height // 2 - 2) +
          term.center('Welcome to ITCOWallet').rstrip())
    print(term.move_y(term.height // 2 - 1) +
          term.center('Press Any Key to Continue').rstrip())
    term.inkey()
    print(term.clear)
    if post("{}") is None:
        print("Failed to connect to ITCO node. Make sure node is running with correct config.")
        sys.exit(1)

    touch_file(WALLET_FILE)

    wallets = load_json_file(WALLET_FILE)

    if wallets is None:
        print("No wallet could be detected. Creating one for you...")
        wallet = create_wallet()['wallet']
        with open(WALLET_FILE, 'w') as f:
            json.dump({"main": wallet}, f)

    while wallet is None:
        print(term.clear)
        print("Which wallet would you like to open?")
        print("Do not enter a wallet name to default to \"main\".")
        for w in wallets:
            print(w)
        wallet_name = input("\nEnter wallet name: ")
        if not wallet_name:
            wallet_name = "main"
        if wallet_name in wallets:
            wallet = wallets[wallet_name]
        else:
            print(term.clear)
            print("Wallet not found with name: " + wallet_name)
            print("Press any key to try again...")
            term.inkey()
    print(term.clear)
    print("Opened wallet.")
    print()
    balances = wallet_balances(wallet)['balances']
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
            print("quit/exit".ljust(15) + "Exits wallet")
        elif command == "balances":
            print(term.clear)
            balances = wallet_balances(wallet)['balances']
            for balance in balances:
                print("Balance: " + balances[balance]['balance'] + " ITCO \nAddress: " + balance)
        elif command == "quit" or command[0] == "exit":
            print(term.clear)
            exit(0)
        elif command == "clear":
            print(term.clear)
        else:
            print("Command not found, try using the help command.")


if __name__ == "__main__":
    main()
