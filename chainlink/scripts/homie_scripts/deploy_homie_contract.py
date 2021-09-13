# Deplploys and funds with Link

from brownie import DigiHomie, accounts, network, config, interface
from scripts.helpful_scripts import *
#Deploys and fund

LOADINGURI = "ipfs://Qme9i2UjhqA6evVSWZaCHgSF4AvgQzsb4mVUDwP971ZNfL"


def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(network.show_active())
    publish_source = True
    digiHomie = DigiHomie.deploy(LOADINGURI,
                                 {"from": dev},
                                 publish_source=publish_source
                                 )
    # fund_homie(digiHomie)
    # fund_with_link(digiHomie.address)
    return digiHomie
