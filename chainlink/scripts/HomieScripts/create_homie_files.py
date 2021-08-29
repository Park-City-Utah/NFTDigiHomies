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
    for token_id in range(1):
        print("Current token: {}".format(token_id))
        homie_metadata = sample_metadata.metadata_template
        homie_metadata["name"] = str(token_id)
        homie_metadata["description"] = 'An Eternal Etherium Digital Homie!'
        homie_metadata["image"] = ''
        homie_metadata["background_color"] = '0F7CB3'
        # Will add image and attributes after creation of Homie (image, meta)
        generateHomie(token_id, homie_metadata)
