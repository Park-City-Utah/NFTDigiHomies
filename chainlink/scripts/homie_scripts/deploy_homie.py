from brownie import DigiHomie, accounts, config
from scripts.helpful_scripts import *


def main():
    dev = accounts.add(config['wallets']['from_key'])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    transaction = digiHomie.mintHomie(
        "ipfs://Qmb3ohBTVy95vKTHgBj5qRN1g53wLkqVyRCSqhmJ4h2ej6", {"from": dev})  # no seed needed
    print("Waiting for transaction")
    transaction.wait(1)
