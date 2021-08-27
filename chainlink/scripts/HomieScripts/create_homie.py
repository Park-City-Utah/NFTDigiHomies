from brownie import DigiHomie, accounts, config
from scripts.helpful_scripts import get_body, get_eyes, get_mouth
import time


def main():
    dev = accounts.add(config['wallets']['from_key'])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    transaction = digiHomie.createHomie(
        "None", {"from": dev})  # no seed needed
    transaction.wait(1)
    # emit reques we have un digihomie
    requestId = transaction.events['requestedCollectable']['requestId']
    time.sleep(30)
    token_id = digiHomie.requestIdToTokenId(
        requestId)  # get token id from mapping
    body = get_body(digiHomie.tokenIdToBody(token_id))
    print('Body type of tokenId {} is {}'.format(token_id, body))
    eyes = get_eyes(digiHomie.tokenIdToEyes(token_id))
    print('Eyes type of tokenId {} is {}'.format(token_id, eyes))
    mouth = get_mouth(digiHomie.tokenIdToMouth(token_id))
    print('Mouth type of tokenId {} is {}'.format(token_id, mouth))
