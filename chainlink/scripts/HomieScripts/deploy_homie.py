# Deplploys and funds with Link

from brownie import DigiHomie, accounts, network, config, interface


def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(network.show_active())
    publish_source = False
    digiHomie = DigiHomie.deploy(
        config['networks'][network.show_active()]['vrf_coordinator'],
        config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['keyhash'],
        {"from": dev},
        publish_source=publish_source
    )
    fund_homie(digiHomie)

    # Generate single homie
    # Then look this whole call to create each

    #rando = digiHomie.getRandomNumber()
    #print("This is my number" + str(rando))
    return digiHomie


def fund_homie(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(
        config['networks'][network.show_active()]['link_token'])
    link_token.transfer(nft_contract, 100000000000000000, {'from': dev})
