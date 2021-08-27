from os import error
from brownie import DigiHomie, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_body, get_eyes, get_mouth
from pathlib import Path


def main():
    print("Working on " + network.show_active())
    digiHomie = DigiHomie[len(DigiHomie)-1]
    number_of_tokens = digiHomie.tokenCounter()
    print("The number of tokens deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, digiHomie)


def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        homie_metadata = sample_metadata.metadata_template
        body = get_body(nft_contract.tokenIdToBody(token_id))
        eyes = get_eyes(nft_contract.tokenIdToEyes(token_id))
        mouth = get_mouth(nft_contract.tokenIdToMouth(token_id))
        metadata_file_name = (
            "./metadata/"+str(token_id)+".json"
        )
        if Path(metadata_file_name).exists():
            print("{} already exists!".format(metadata_file_name))
        else:
            print("Creating metadata file {}".format(metadata_file_name))
            homie_metadata["name"] = str(token_id)
            homie_metadata["description"] = 'An Eternal Etherium Digital Homie!'
            homie_metadata["image"] = 'ipfs://<hash>'
            homie_metadata["background_color"] = '0F7CB3'
            homie_metadata["attributes"] = [
                {"trait_type": 'Body', "value": str(body)},
                {"trait_type": 'Eyes', "value": str(eyes)},
                {"trait_type": 'Mouth', "value": str(mouth)}
            ]
            # attributes
            print(homie_metadata)
