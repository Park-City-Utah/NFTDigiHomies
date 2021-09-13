from pathlib import Path
from brownie import (
    network,
    DigiHomie,
    accounts,
    config,
    Contract,
)
from scripts.helpful_scripts import *
from metadata import sample_metadata
from web3 import Web3
from PIL import Image
import numpy as np
import os as os
import json as json
from pathlib import Path
import requests

ASSETFOLDER = "../../Assets/"
LOADINGURI = "ipfs://Qme9i2UjhqA6evVSWZaCHgSF4AvgQzsb4mVUDwP971ZNfL"
TOTAL = 5
setURI = True

#############################################################################
##  Homie Class - Generation of Homie NFT object includes random asset     ##
# assignment and generation of PNG/Metat data
#############################################################################


##Creates Homies - 'setURI' boolean determines URI##
##URI = FALSE - Set URI to 'loading' and meta to 'TBD'##
##URI = FALSE - Set IPFS URI in mapping for later resolution##
##URI = TRUE - Set URI & mapping to IPFS URI##
def main():
    print("Working on " + network.show_active())
    dev = accounts.add(config["wallets"]["from_key"])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    iteration = digiHomie.tokenCounter()

    while(iteration < TOTAL):
        print("Iteration: " + str(iteration))
        print("Token Counter: " + str(digiHomie.tokenCounter()))

        # Generate homie object (image, metadata)
        myHomie = Homie()

        metaPath = "{}.json".format(myHomie.path)
        metaName = "{}.json".format(iteration)

        imagePath = "{}.png".format(myHomie.path)
        imageName = "{}.png".format(iteration)

        print("MetaDataPath: {}".format(metaPath))
        print("MetaName: {}".format(metaName))
        print("ImageDataPath: {}".format(imagePath))
        print("ImageName: {}".format(imageName))

        ##IFF upload to IPFS requested##
        image_to_upload = None
        meta_to_upload = None
        if os.getenv("UPLOAD_IPFS") == "true":

            # Upload and return IPFS image uri
            image_to_upload = upload_to_ipfs(imagePath, imageName)
            # Set image property of metadata
            myHomie.data['image'] = image_to_upload

            # Meta data upload to IPFS = returns meta
            with open(metaPath, 'w') as f:
                json.dump(myHomie.data, f)
            # Returns the meta uri
            metaURI = upload_to_ipfs(metaPath, metaName)

        if(setURI == True):
            transaction = digiHomie.adminMintHomie(
                metaURI, {"from": dev})
            print("Setting URI to {} ".format(metaURI))
        else:
            transaction = digiHomie.adminMintHomiePending(
                metaURI, {"from": dev})
            print("Setting URI to 'loading' URI")
        transaction.wait(1)
        iteration = iteration+1


class Homie():
    tokenCounter = 0
    path = ''

    def _init_(self):
        Homie.tokenCounter += 1
        self.id = Homie.tokenCounter
        self.data = generate_meta_data(self.id)
        self.path = generateHomies(self.id)

    @classmethod
    def generate_meta_data(token_id):
        homie_metadata = sample_metadata.metadata_template
        homie_metadata["name"] = str(token_id)
        homie_metadata["description"] = 'An Eternal Ethereum Digital Homie!'
        homie_metadata["image"] = ''
        homie_metadata["background_color"] = '0F7CB3'
        # Will add image and attributes after creation of Homie (image, meta)
        homie_metadata["attributes"] = []
        return homie_metadata

    @classmethod
    def generate_homie(token_id):
        body = generateRandomNumber(1, 6)
        eyes = generateRandomNumber(1, 8)
        mouth = generateRandomNumber(1, 7)
        # OPTIONAL - higher range equals increase randomness, less likely to align with exisiting feature
        hair = generateRandomNumber(0, 8)
        facialHair = generateRandomNumber(0, 10)
        jewelry = generateRandomNumber(0, 10)
        smoke = generateRandomNumber(0, 15)
        hat = generateRandomNumber(0, 15)
        glasses = generateRandomNumber(0, 10)
        mask = generateRandomNumber(0, 25)
        special = generateRandomNumber(0, 200)

        # Feature Dict
        bodyDict = createBodyDict()
        eyeDict = createEyeDict()
        mouthDict = createMouthDict()
        hairDict = createHairDict()
        facialHairDict = createFacialHairDict()
        jewelryDict = createJewelryDict()
        smokeDict = createSmokeDict()
        hatDict = createHatDict()
        glassesDict = createGlassesDict()
        maskDict = createMaskDict()
        specialDict = createSpecialDict()

        Swag = 0

        # Special characteristic - Allow smoke & jewelry only
        if(0 < special <= 2):
            img0 = Image.open(ASSETFOLDER + "Special/" + str(special) + ".png")
            Homie.data['attributes'].append(
                {
                    'trait_type': 'Special',
                    'value': specialDict[special]
                })
            print('Special' + str(special))
            Swag = Swag + 70
            if(0 < smoke <= 4):
                img6 = Image.open(ASSETFOLDER + "Smoke/" + str(smoke) + ".png")
                img0.paste(img6, (0, 0), img6)
                Homie.data['attributes'].append(
                    {
                        'trait_type': 'Smoke',
                        'value': smokeDict[smoke]
                    })
                Swag = Swag + 10
            else:
                smoke = 0

            if(0 < jewelry <= 5):
                img5 = Image.open(ASSETFOLDER + "Jewelry/" +
                                  str(jewelry) + ".png")
                img0.paste(img5, (0, 0), img5)
                Homie.data['attributes'].append(
                    {
                        'trait_type': 'Jewelry',
                        'value': jewelryDict[jewelry]
                    })
                if(jewelry >= 4):
                    Swag = Swag + 20
                else:
                    Swag = Swag + 10
            # img0.show()
        else:
            special = 0

            # Open Required pngs (Body, Eyes, Mouth)
            img0 = Image.open(ASSETFOLDER + "Body/" + str(body) + ".png")
            Homie.data['attributes'].append(
                {
                    'trait_type': 'Body',
                    'value': bodyDict[body]
                })
            if(body > 3):
                Swag = Swag + 15
            img1 = Image.open(ASSETFOLDER + "Eyes/" + str(eyes) + ".png")
            img2 = Image.open(ASSETFOLDER + "Mouth/" + str(mouth) + ".png")

            # Paste Required PNGs
            img0.paste(img1, (0, 0), img1)
            Homie.data['attributes'].append(
                {
                    'trait_type': 'Eyes',
                    'value': eyeDict[eyes]
                })
            if(eyes == 7):
                Swag = Swag + 20
            if(eyes == 8):
                Swag = Swag + 25
            img0.paste(img2, (0, 0), img2)
            Homie.data['attributes'].append(
                {
                    'trait_type': 'Mouth',
                    'value': mouthDict[mouth]
                })
            if(mouth == 7):
                Swag = Swag + 10
            # Open AND Paste Optional PNGs
            if(0 < hair < 9):
                img3 = Image.open(ASSETFOLDER + "Hair/" + str(hair) + ".png")
                img0.paste(img3, (0, 0), img3)
                Homie.data['attributes'].append(
                    {
                        'trait_type': 'Hair',
                        'value': hairDict[hair]
                    })
                if(3 < hair <= 6):
                    Swag = Swag + 10
                if(hair >= 7):
                    Swag = Swag + 15
            if(0 < facialHair <= 7):
                img4 = Image.open(ASSETFOLDER + "FacialHair/" +
                                  str(facialHair) + ".png")
                img0.paste(img4, (0, 0), img4)
                Homie.data['attributes'].append(
                    {
                        'trait_type': 'Facial Hair',
                        'value': facialHairDict[facialHair]
                    })
                if(facialHair == 7):
                    Swag = Swag + 10
                if(hair == 6):
                    Swag = Swag + 5
            else:
                facialHair = 0
            if(0 < jewelry <= 5):
                img5 = Image.open(ASSETFOLDER + "Jewelry/" +
                                  str(jewelry) + ".png")
                img0.paste(img5, (0, 0), img5)
                Homie.data['attributes'].append(
                    {
                        'trait_type': 'Jewelry',
                        'value': jewelryDict[jewelry]
                    })
                if(jewelry >= 4):
                    Swag = Swag + 20
                if(jewelry < 4):
                    Swag = Swag + 10
            else:
                jewelry = 0

            # Mask - If mask, no smoke, hat or glasses added
            if(0 < mask <= 5):
                if(mask < 3 and hair != 6):
                    img9 = Image.open(
                        ASSETFOLDER + "Mask/" + str(mask) + ".png")
                    img0.paste(img9, (0, 0), img9)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Mask',
                            'value': maskDict[mask]
                        })
                if(mask == 5):
                    img9 = Image.open(
                        ASSETFOLDER + "Mask/" + str(mask) + ".png")
                    img0.paste(img9, (0, 0), img9)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Mask',
                            'value': maskDict[mask]
                        })
                    Swag = Swag + 45
                if(2 < mask < 5):
                    img9 = Image.open(
                        ASSETFOLDER + "Mask/" + str(mask) + ".png")
                    img0.paste(img9, (0, 0), img9)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Mask',
                            'value': maskDict[mask]
                        })
                    Swag = Swag + 35
                if(mask <= 2):
                    img9 = Image.open(
                        ASSETFOLDER + "Mask/" + str(mask) + ".png")
                    img0.paste(img9, (0, 0), img9)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Mask',
                            'value': maskDict[mask]
                        })
                    Swag = Swag + 20
            else:
                if((0 < hat <= 4) and (hair != 6)):
                    img7 = Image.open(ASSETFOLDER + "Hat/" + str(hat) + ".png")
                    img0.paste(img7, (0, 0), img7)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Hat',
                            'value': hatDict[hat]
                        })
                    if(hat == 4):
                        Swag = Swag + 20
                    else:
                        Swag = Swag + 10
                else:
                    hat = 0
                if(0 < smoke <= 4):
                    img6 = Image.open(
                        ASSETFOLDER + "Smoke/" + str(smoke) + ".png")
                    img0.paste(img6, (0, 0), img6)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Smoke',
                            'value': smokeDict[smoke]
                        })
                    Swag = Swag + 15
                else:
                    smoke = 0
                if(0 < glasses <= 6):
                    img8 = Image.open(ASSETFOLDER + "Glasses/" +
                                      str(glasses) + ".png")
                    img0.paste(img8, (0, 0), img8)
                    Homie.data['attributes'].append(
                        {
                            'trait_type': 'Glasses',
                            'value': glassesDict[glasses]
                        })
                    if(glasses <= 3):
                        Swag = Swag + 15
                    else:
                        Swag = Swag = 5
                else:
                    glasses = 0
                mask = 0        # img0.show()

        if(Swag > 100):
            Swag = 100
        Homie.data['attributes'].append(
            {
                'display_type': 'boost_number',
                'trait_type': 'Swag',
                'value': Swag
            })

        # Create and save Homie.data
        folder = ASSETFOLDER + "Homies/{}/".format(str(token_id))
        if not os.path.isdir(folder):
            os.mkdir(folder)

        resized_img = img0.resize((300, 300), resample=Image.NEAREST)
        resized_img.save(folder + str(token_id) + '.png', "PNG")

        # Set  path in object
        path = folder + str(token_id)
        return path

        # img0.show()


def generateRandomNumber(lowIn, highIn):
    rng = np.random.default_rng()
    ranNumberArray = rng.integers(low=lowIn, high=highIn, size=1)
    return int(ranNumberArray[0])


# Upload and PIN to IPFS service
def upload_to_ipfs(filepath, name):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(
            ipfs_url + "/api/v0/add", files={"file": image_binary})
        print("Hash " + response.json()['Hash'])
        ipfs_hash = response.json()['Hash']
        filename = filepath.split("/")[-1:][0]
        print("Filename " + filename)
        uriForOS = "ipfs://{}".format(ipfs_hash)
        print("URI " + uriForOS)

        # NOTE Commented out, pin queue is async
        # ipfs_pin_command = "ipfs pin remote add --service=Pinata {}".format(ipfs_hash)
        # pin_response =
        requests.post(
            ipfs_url + "/api/v0/pin/remote/add?arg={}&name={}&service=Pinata".format(ipfs_hash, name))
        # print(pin_response)
        return uriForOS
    return None


def createBodyDict():
    bodyDict = {
        1: 'Thin',
        2: 'Thin',
        3: 'Thin',
        4: 'Thick',
        5: 'Thick',
        6: 'Thick'
    }
    return bodyDict


def createEyeDict():
    eyeDict = {
        1: 'Normal',
        2: 'Normal',
        3: 'Squint',
        4: 'Squint',
        5: 'Peer',
        6: 'Peep',
        7: 'Gold',
        8: 'Diamond'
    }
    return eyeDict


def createMouthDict():
    mouthDict = {
        1: 'Normal',
        2: 'Grin',
        3: 'Smile',
        4: 'Ohh',
        5: 'Lips',
        6: 'Missing Tooth',
        7: 'Gold Tooth'
    }
    return mouthDict


def createHairDict():
    hairDict = {
        1: 'Black',
        2: 'Brown',
        3: 'Gray',
        4: 'Pink',
        5: 'Comb-Over',
        6: 'Man-Bun',
        7: 'Corn-Rows',
        8: 'Mullet'
    }
    return hairDict


def createFacialHairDict():
    facialHairDict = {
        1: 'Light',
        2: 'Stuble',
        3: 'Handle-Bar',
        4: 'Light Handle-Bar',
        5: 'Grey Beard',
        6: 'Moustache',
        7: 'Handle-Bar'
    }
    return facialHairDict


def createJewelryDict():
    jewelryDict = {
        1: 'Gold Chain',
        2: 'Gold Chain & Earring',
        3: 'Diamond Chain',
        4: 'Diamond Chain, Earring & Nose Ring',
        5: 'XL Gold Chain & Diamond Earring'
    }
    return jewelryDict


def createSmokeDict():
    smokeDict = {
        1: 'Cigarette',
        2: 'Joint Sativa',
        3: 'Jeferey',
        4: 'Joint Indica'
    }
    return smokeDict


def createHatDict():
    hatDict = {
        1: 'Bonzai',
        2: 'Backwards Cap',
        3: 'DuRag',
        4: 'Crown'
    }
    return hatDict


def createGlassesDict():
    glassesDict = {
        1: 'Carerra',
        2: 'Miami',
        3: 'Dahmers',
        4: 'Dark Dahmers',
        5: 'Pink Stunners',
        6: 'Patch'
    }
    return glassesDict


def createMaskDict():
    maskDict = {
        1: 'Balaklava',
        2: 'Ninja',
        3: 'Doom',
        4: 'Doom 2',
        5: 'Jason'
    }
    return maskDict


def createSpecialDict():
    specialDict = {
        1: 'Alien',
        2: 'Death'
    }
    return specialDict
