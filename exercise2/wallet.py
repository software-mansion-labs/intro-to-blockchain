import argparse
import requests
from simple_cryptography import PrivateKey, PublicKey

class Wallet:
    node_url: str
    private_key: PrivateKey
    public_key: PublicKey

    def __init__(self, node_url: str):
        self.node_url = node_url

        # TODO: Akceptować private key jako argument albo wczytywać z pliku

    def get_unspent_transactions(self):
        """
        TODO: Znajdź wszystkie niewykorzystane transakcje powiązane z tym portfelem.
        """
    
    def get_balance(self):
        """
        TODO: Zwróć liczbę niewykorzystanych transakcji
        """

    def transfer(self, recipient):
        """
        TODO: Jeśli istnieje jakakolwiek niewykorzystana transakcja, przekaż ją do nowego właściciela.
        """

parser = argparse.ArgumentParser()

parser.add_argument("command", choices=["transfer", "get_balance"])
parser.add_argument("-r", "--recipient", help="Address of the recipient", type=str)

wallet = Wallet("url") # TODO: Set url here

if __name__ == "__main__":
    args = parser.parse_args()

    if args.command == "transfer":
        if args.recipient == None:
            raise Exception("Missing one or more required arguments (-r/--recipient)")
        
        wallet.transfer(args.recipient, args.amount)
    
    if args.command == "get_balance":
        wallet.get_balance()


