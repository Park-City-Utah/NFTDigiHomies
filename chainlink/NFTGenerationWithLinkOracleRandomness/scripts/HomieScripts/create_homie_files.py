from os import error
from brownie import DigiHomie, network
from metadata import sample_metadata
from scripts.helpful_scripts import *
from pathlib import Path


def main():
    print("Working on " + network.show_active())
    digiHomie = DigiHomie[len(DigiHomie)-1]
    number_of_tokens = digiHomie.tokenCounter()
    print("The number of tokens deployed is {}".format(number_of_tokens))
    #write_metadata(digiHomie, number_of_tokens)
    rando = digiHomie.rando()
    print("The random number is " + str(rando))
    for token_id in range(number_of_tokens):
        print("Current token: {}".format(token_id))
        homie_metadata = sample_metadata.metadata_template
        homie_metadata["name"] = str(token_id)
        homie_metadata["description"] = 'An Eternal Etherium Digital Homie!'
        homie_metadata["image"] = 'ipfs://QmdGqDw4MuAov7wFZkmLd2H29sMcFN6kmPLranX7rUSd1i'
        homie_metadata["background_color"] = '0F7CB3'
        generateHomie(rando, token_id, homie_metadata)
