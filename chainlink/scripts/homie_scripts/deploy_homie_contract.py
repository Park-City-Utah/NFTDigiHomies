# Deplploys and funds with Link

from brownie import DigiHomie, accounts, network, config, interface
from scripts.helpful_scripts import *
#Deploys and fund


def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(network.show_active())
    publish_source = False
    digiHomie = DigiHomie.deploy(
        {"from": dev},
        publish_source=publish_source
    )
    # fund_homie(digiHomie)
    # fund_with_link(digiHomie.address)
    return digiHomie


""" 
def fund_homie(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(
        config['networks'][network.show_active()]['link_token'])
    link_token.transfer(nft_contract, 100000000000000000, {'from': dev}) """
