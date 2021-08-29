from brownie import DigiHomie, accounts, config
from scripts.helpful_scripts import *
import time


def main():
    dev = accounts.add(config['wallets']['from_key'])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    # fund_with_link(digiHomie.address)
    transaction = digiHomie.createHomie(
        "ipfs://Qmb3ohBTVy95vKTHgBj5qRN1g53wLkqVyRCSqhmJ4h2ej6", {"from": dev})  # no seed needed
    #print("Waiting for second transaction")
    transaction.wait(1)
    # time.sleep(60)
    # emit request we have in digihomie
    #requestId = transaction.events['requestedCollectable']['requestId']
    # token_id = digiHomie.requestIdToTokenId(
    # requestId)  # get token id from mapping
    # breed = getBreed(advanced_collectable.tokenIdToBreed(tokenId)
    #print('TokenId is {}'.format(token_id))
