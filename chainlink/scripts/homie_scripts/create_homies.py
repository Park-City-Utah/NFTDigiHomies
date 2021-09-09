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

##################################################################################
##  Final Steps:                                                                ##
##  1 - CreatHomies(500, True) - Create 1-499 end to end, revealed              ##
##  2 - CreateHomies(500, False) - Create 500-999 with 'PENDING' meta           ##
##  3 - SetTokenMApping(500) - Create image/meta and MAP, for later MINTING     ##
##  4 - UserMintHomies(1-10) - MINT and setTokenURI to MAPPED via tokenIdtoURI  ##
##  5 - ResovleTokenURI(x) - Will 'reveal' minted 'PENDING' tokens              ##
##  6 - ResolveAllTokenURIs() - Will 'reveal' ALL minted 'PENDING' tokens       ##
##################################################################################

# Loading uri "ipfs://Qme9i2UjhqA6evVSWZaCHgSF4AvgQzsb4mVUDwP971ZNfL"


def main():

    # Test
    # i = 0
    # while(i < 500):
    #     generateHomiesAndFilesTEST(i)
    #     i = i + 1

    # Create tokens, set TOTAL - number it will create up to, from current total
    # createHomies(10, True)  # With URI

    # Create tokens, set TOTAL - number it will create up to, from current total (5, must be < 5)
    # createHomies(20, False)  # Without URI (mapped but not exposed)

    # Will NOT mint, will create image/meta and store uri in contract mapping, for later userMint
    # setTokenMapping(30)

    #print("Total tokens is {}".format(getTokenCount()))

    # Resolve mapped will set 'pending' URI to mapped (final) URI of meta w/ png and traits in tact
    # WILL BE THE EXACT # (token) - resolveTokenURI(11) will expose the # 11 token
    resolveTokenURI(10)
    # resolveTokenURI(1)
    # resolveTokenURI(8)

    # Resolve ALL tokens should resolve rest, will skip set
    # resolveAllTokensURIs()

    # mappedURI = getMappedURI(3)
    # print("Mapped URI is {}".format(mappedURI))
    # tokenURI = getTokenURI(3)
    # print("TokenURI is: {}".format(tokenURI))

    ## Retrieve metadata URI by tokenId()##
    # setTokenMapping(8)  # Must be larger, starts from last...

    #print("Mapped URI: {}".format(getMappedURI(22)))
    #print("Token URI: {}".format(getTokenURI(22)))

    # User can mint any mapped, but not created, up to total
    # userMintHomies(2)

    # Print token count & mapped count
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    print("Token Counter: " + str(digiHomie.tokenCounter()))
    print("Mapped Counter: " + str(digiHomie.mappedCounter()))


def userMintHomies(total):
    print("Working on " + network.show_active())
    print("Minting {} tokens by resolving tokenURI to mappedURI in tokenIdToMapped()".format(total))
    dev = accounts.add(config["wallets"]["from_key"])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    transaction = digiHomie.userMintHomies(total, {"from": dev})


##Retrieve metadata URI from mapping via tokenId##
def setTokenMapping(total):
    print("Working on " + network.show_active())
    dev = accounts.add(config["wallets"]["from_key"])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent

    iteration = digiHomie.mappedCounter()
    while(iteration < total):
        print("Iteration: " + str(iteration))
        print("Token Counter: " + str(digiHomie.tokenCounter()))
        print("Mapped Counter: " + str(digiHomie.mappedCounter()))

        # Generate image, metadata and upload to IPFS
        uri = generateHomies(iteration)
        print("URI: {}".format(uri))
        transaction = digiHomie.setTokenMapping(uri, {"from": dev})
        print("Setting URI to {} ".format(uri))
        transaction.wait(1)
        iteration = iteration + 1
        print("Token Counter: " + str(digiHomie.tokenCounter()))
        print("Mapped Counter: " + str(digiHomie.mappedCounter()))


def getTokenURI(tokenId):
    digiHomie = DigiHomie[len(DigiHomie)-1]
    tokenURI = digiHomie.tokenURI(tokenId)
    return tokenURI


##Retrieve metadata URI from mapping via tokenId##
def getMappedURI(tokenId):
    digiHomie = DigiHomie[len(DigiHomie)-1]
    mappedURI = digiHomie.tokenIdToURI(tokenId)
    return mappedURI


##Retreive total tokens/homies deployed##
def getTokenCount():
    digiHomie = DigiHomie[len(DigiHomie)-1]
    number_of_homies = digiHomie.tokenCounter()
    # print("The number of NFTs deployed: {}".format(number_of_homies))
    return number_of_homies


##Retreive total tokens/homies deployed##
def getMappedCount():
    digiHomie = DigiHomie[len(DigiHomie)-1]
    mapped = digiHomie.mappedCounter()
    # print("The number of NFTs deployed: {}".format(number_of_homies))
    return mapped

# User mint will simply call mint


##Creates Homies - 'setURI' boolean determines URI##
##URI = FALSE - Set URI to 'loading' and meta to 'TBD'##
##URI = FALSE - Set IPFS URI in mapping for later resolution##
##URI = TRUE - Set URI & mapping to IPFS URI##
def createHomies(total, setURI):
    print("Working on " + network.show_active())
    dev = accounts.add(config["wallets"]["from_key"])
    digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
    iteration = digiHomie.tokenCounter()
    while(iteration < total):
        print("Iteration: " + str(iteration))
        print("Token Counter: " + str(digiHomie.tokenCounter()))

        # Generate image, metadata and upload to IPFS
        uri = generateHomies(iteration)
        print("URI: {}".format(uri))

        if(setURI == True):
            transaction = digiHomie.mintHomie(
                uri, {"from": dev})
            print("Setting URI to {} ".format(uri))
        else:
            transaction = digiHomie.mintHomiePending(
                uri, {"from": dev})
            print("Setting URI to 'loading' URI")
        transaction.wait(1)
        iteration = iteration+1


##Sets URI to mapped value, exposing IPFS URI (image, desc etc)##
def resolveTokenURI(token_id):
    dev = accounts.add(config["wallets"]["from_key"])
    print("Working on " + network.show_active())

    # Print token URI, mapped and set
    print("Resolving URI for tokenId: {}".format(token_id))
    uri = getTokenURI(token_id)
    print("URI is {}".format(uri))
    mappedURI = getMappedURI(token_id)
    print("Mapped URI is {}".format(mappedURI))

    # Set token to mapped value, print
    digiHomie = DigiHomie[len(DigiHomie) - 1]
    uri = digiHomie.tokenIdToURI(token_id)
    print("Resoving URI to mapped value: {}".format(uri))
    digiHomie.setTokenURI(token_id, uri, {"from": dev})
    uri = getTokenURI(token_id)
    print("URI is {}".format(uri))
    mappedURI = getMappedURI(token_id)
    print("Mapped URI is {}".format(mappedURI))
    print('Please give up to 20 minutes, and "refresh metadata" button')


##Resolve all URIs current not set (user Minted)##
def resolveAllTokensURIs():
    print("Working on " + network.show_active())
    dev = accounts.add(config["wallets"]["from_key"])
    digiHomie = DigiHomie[len(DigiHomie) - 1]
    number_of_homies = digiHomie.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_homies))
    for token_id in range(number_of_homies):
        # Print mapped and URI
        currentURI = getTokenURI(token_id)
        print("Current URI is {}".format(currentURI))
        mappedURI = getMappedURI(token_id)
        print("Mapped URI is {}".format(mappedURI))

        if(digiHomie.tokenURI(token_id).startswith("ipfs://Qme9i2UjhqA6evVSWZaCHgSF4AvgQzsb4mVUDwP971ZNfL")):
            print("Resolving token: {}".format(token_id))

            uri = digiHomie.tokenIdToURI(token_id)
            print("Resoving URI to mapped value: {}".format(uri))
            digiHomie.setTokenURI(token_id, uri, {"from": dev})
            # Print mapped and URI
            currentURI = getTokenURI(token_id)
            print("URI is {}".format(currentURI))
            mappedURI = getMappedURI(token_id)
            print("Mapped URI is {}".format(mappedURI))
        else:
            print("\nSkipping {}, we already set that tokenURI!".format(token_id))


def generate_meta_data(token_id):
    homie_metadata = sample_metadata.metadata_template
    homie_metadata["name"] = str(token_id)
    homie_metadata["description"] = 'An Eternal Ethereum Digital Homie!'
    homie_metadata["image"] = ''
    homie_metadata["background_color"] = '0F7CB3'
    # Will add image and attributes after creation of Homie (image, meta)
    homie_metadata["attributes"] = []
    return homie_metadata


def generateRandomNumber(lowIn, highIn):
    rng = np.random.default_rng()
    ranNumberArray = rng.integers(low=lowIn, high=highIn, size=1)
    return int(ranNumberArray[0])


def generateHomies(token_id):
    # Generate metat data template
    data = generate_meta_data(token_id)

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
    mask = generateRandomNumber(0, 15)
    special = generateRandomNumber(0, 220)

    # Feature map
    bodyMap = createBodyMap()
    eyeMap = createEyeMap()
    mouthMap = createMouthMap()
    hairMap = createHairMap()
    facialHairMap = createFacialHairMap()
    jewelryMap = createJewelryMap()
    smokeMap = createSmokeMap()
    hatMap = createHatMap()
    glassesMap = createGlassesMap()
    maskMap = createMaskMap()
    specialMap = createSpecialMap()

    # Create data object for json file creation
    # data = createDataMap(i)

    Swag = 0

    # Special characteristic - Allow smoke & jewelry only
    if(0 < special <= 2):
        img0 = Image.open(ASSETFOLDER + "Special/" + str(special) + ".png")
        data['attributes'].append(
            {
                'trait_type': 'Special',
                'value': specialMap[special]
            })
        print('Special' + str(special))
        Swag = Swag + 70
        if(0 < smoke <= 4):
            img6 = Image.open(ASSETFOLDER + "Smoke/" + str(smoke) + ".png")
            img0.paste(img6, (0, 0), img6)
            data['attributes'].append(
                {
                    'trait_type': 'Smoke',
                    'value': smokeMap[smoke]
                })
            Swag = Swag + 10
        else:
            smoke = 0

        if(0 < jewelry <= 5):
            img5 = Image.open(ASSETFOLDER + "Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
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
        data['attributes'].append(
            {
                'trait_type': 'Body',
                'value': bodyMap[body]
            })
        if(body > 3):
            Swag = Swag + 15
        img1 = Image.open(ASSETFOLDER + "Eyes/" + str(eyes) + ".png")
        img2 = Image.open(ASSETFOLDER + "Mouth/" + str(mouth) + ".png")

        # Paste Required PNGs
        img0.paste(img1, (0, 0), img1)
        data['attributes'].append(
            {
                'trait_type': 'Eyes',
                'value': eyeMap[eyes]
            })
        if(eyes == 7):
            Swag = Swag + 20
        if(eyes == 8):
            Swag = Swag + 25
        img0.paste(img2, (0, 0), img2)
        data['attributes'].append(
            {
                'trait_type': 'Mouth',
                'value': mouthMap[mouth]
            })
        if(mouth == 7):
            Swag = Swag + 10
        # Open AND Paste Optional PNGs
        if(0 < hair < 9):
            img3 = Image.open(ASSETFOLDER + "Hair/" + str(hair) + ".png")
            img0.paste(img3, (0, 0), img3)
            data['attributes'].append(
                {
                    'trait_type': 'Hair',
                    'value': hairMap[hair]
                })
            if(3 < hair <= 6):
                Swag = Swag + 10
            if(hair >= 7):
                Swag = Swag + 15
        if(0 < facialHair <= 7):
            img4 = Image.open(ASSETFOLDER + "FacialHair/" +
                              str(facialHair) + ".png")
            img0.paste(img4, (0, 0), img4)
            data['attributes'].append(
                {
                    'trait_type': 'Facial Hair',
                    'value': facialHairMap[facialHair]
                })
            if(facialHair == 7):
                Swag = Swag + 10
            if(hair == 6):
                Swag = Swag + 5
        else:
            facialHair = 0
        if(0 < jewelry <= 5):
            img5 = Image.open(ASSETFOLDER + "Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
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
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
            if(mask == 5):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
                Swag = Swag + 45
            if(2 < mask < 5):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
                Swag = Swag + 35
            if(mask <= 2):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
                Swag = Swag + 20
        else:
            if((0 < hat <= 4) and (hair != 6)):
                img7 = Image.open(ASSETFOLDER + "Hat/" + str(hat) + ".png")
                img0.paste(img7, (0, 0), img7)
                data['attributes'].append(
                    {
                        'trait_type': 'Hat',
                        'value': hatMap[hat]
                    })
                if(hat == 4):
                    Swag = Swag + 20
                else:
                    Swag = Swag + 10
            else:
                hat = 0
            if(0 < smoke <= 4):
                img6 = Image.open(ASSETFOLDER + "Smoke/" + str(smoke) + ".png")
                img0.paste(img6, (0, 0), img6)
                data['attributes'].append(
                    {
                        'trait_type': 'Smoke',
                        'value': smokeMap[smoke]
                    })
                Swag = Swag + 15
            else:
                smoke = 0
            if(0 < glasses <= 6):
                img8 = Image.open(ASSETFOLDER + "Glasses/" +
                                  str(glasses) + ".png")
                img0.paste(img8, (0, 0), img8)
                data['attributes'].append(
                    {
                        'trait_type': 'Glasses',
                        'value': glassesMap[glasses]
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
    data['attributes'].append(
        {
            'display_type': 'boost_number',
            'trait_type': 'Swag',
            'value': Swag
        })
    # print("Swag: {}".format(str(Swag)))

    # Create and save data
    folder = ASSETFOLDER + "Homies/{}/".format(str(token_id))
    if not os.path.isdir(folder):
        os.mkdir(folder)

    resized_img = img0.resize((300, 300), resample=Image.NEAREST)
    resized_img.save(folder + str(token_id) + '.png', "PNG")

    # img0.show()

    ##IFF upload to IPFS requested##
    image_to_upload = None
    meta_to_upload = None
    if os.getenv("UPLOAD_IPFS") == "true":

        image_name = str(token_id) + ".png"
        meta_name = str(token_id) + ".json"

        # Image upload to IPFS
        image_path = folder + str(token_id) + '.png'
        print('ImagePath: ' + image_path)
        # Returns the image uri
        image_to_upload = upload_to_ipfs(image_path, image_name)
        # Set image property of metadata
        data['image'] = image_to_upload

        # Meta data upload to IPFS = returns meta
        meta_path = folder + str(token_id) + 'data.json'
        with open(folder + str(token_id) + 'data.json', 'w') as f:
            json.dump(data, f)
        # Returns the meta uri
        meta_to_upload = upload_to_ipfs(meta_path, meta_name)
    return meta_to_upload


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


def createBodyMap():
    bodyMap = {
        1: 'Thin',
        2: 'Thin',
        3: 'Thin',
        4: 'Thick',
        5: 'Thick',
        6: 'Thick'
    }
    return bodyMap


def createEyeMap():
    eyeMap = {
        1: 'Normal',
        2: 'Normal',
        3: 'Squint',
        4: 'Squint',
        5: 'Peer',
        6: 'Peep',
        7: 'Gold',
        8: 'Diamond'
    }
    return eyeMap


def createMouthMap():
    mouthMap = {
        1: 'Normal',
        2: 'Grin',
        3: 'Smile',
        4: 'Ohh',
        5: 'Lips',
        6: 'Missing Tooth',
        7: 'Gold Tooth'
    }
    return mouthMap


def createHairMap():
    hairMap = {
        1: 'Black',
        2: 'Brown',
        3: 'Gray',
        4: 'Pink',
        5: 'Comb-Over',
        6: 'Man-Bun',
        7: 'Corn-Rows',
        8: 'Mullet'
    }
    return hairMap


def createFacialHairMap():
    facialHairMap = {
        1: 'Light',
        2: 'Stuble',
        3: 'Handle-Bar',
        4: 'Light Handle-Bar',
        5: 'Grey Beard',
        6: 'Moustache',
        7: 'Handle-Bar'
    }
    return facialHairMap


def createJewelryMap():
    jewelryMap = {
        1: 'Gold Chain',
        2: 'Gold Chain & Earring',
        3: 'Diamond Chain',
        4: 'Diamond Chain, Earring & Nose Ring',
        5: 'XL Gold Chain & Diamond Earring'
    }
    return jewelryMap


def createSmokeMap():
    smokeMap = {
        1: 'Cigarette',
        2: 'Joint Sativa',
        3: 'Jeferey',
        4: 'Joint Indica'
    }
    return smokeMap


def createHatMap():
    hatMap = {
        1: 'Bonzai',
        2: 'Backwards Cap',
        3: 'DuRag',
        4: 'Crown'
    }
    return hatMap


def createGlassesMap():
    glassesMap = {
        1: 'Carerra',
        2: 'Miami',
        3: 'Dahmers',
        4: 'Dark Dahmers',
        5: 'Pink Stunners',
        6: 'Patch'
    }
    return glassesMap


def createMaskMap():
    maskMap = {
        1: 'Balaklava',
        2: 'Ninja',
        3: 'Doom',
        4: 'Doom 2',
        5: 'Jason'
    }
    return maskMap


def createSpecialMap():
    specialMap = {
        1: 'Alien',
        2: 'Death'
    }
    return specialMap


def generateHomiesAndFilesTEST(token_id):
    # Generate metat data template
    data = generate_meta_data(token_id)

    body = generateRandomNumber(1, 6)
    eyes = ((generateRandomNumber(1, 100000) % 8) + 1)
    mouth = generateRandomNumber(1, 7)
    # OPTIONAL - higher range equals increase randomness, less likely to align with exisiting feature
    hair = ((generateRandomNumber(0, 100000) % 8) + 1)
    facialHair = generateRandomNumber(0, 10)
    jewelry = generateRandomNumber(0, 9)
    smoke = generateRandomNumber(0, 15)
    hat = generateRandomNumber(0, 15)
    glasses = generateRandomNumber(0, 10)
    mask = generateRandomNumber(0, 15)
    special = generateRandomNumber(0, 200)

    # Feature map
    bodyMap = createBodyMap()
    eyeMap = createEyeMap()
    mouthMap = createMouthMap()
    hairMap = createHairMap()
    facialHairMap = createFacialHairMap()
    jewelryMap = createJewelryMap()
    smokeMap = createSmokeMap()
    hatMap = createHatMap()
    glassesMap = createGlassesMap()
    maskMap = createMaskMap()
    specialMap = createSpecialMap()

    # Create data object for json file creation
    # data = createDataMap(i)

    Swag = 0

    # Special characteristic - Allow smoke & jewelry only
    if(0 < special <= 2):
        img0 = Image.open(ASSETFOLDER + "Special/" + str(special) + ".png")
        data['attributes'].append(
            {
                'trait_type': 'Special',
                'value': specialMap[special]
            })
        print('Special' + str(special))
        Swag = Swag + 70
        if(0 < smoke <= 4):
            img6 = Image.open(ASSETFOLDER + "Smoke/" + str(smoke) + ".png")
            img0.paste(img6, (0, 0), img6)
            data['attributes'].append(
                {
                    'trait_type': 'Smoke',
                    'value': smokeMap[smoke]
                })
            Swag = Swag + 10
        else:
            smoke = 0

        if(0 < jewelry <= 5):
            img5 = Image.open(ASSETFOLDER + "Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
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
        data['attributes'].append(
            {
                'trait_type': 'Body',
                'value': bodyMap[body]
            })
        if(body > 3):
            Swag = Swag + 15
        img1 = Image.open(ASSETFOLDER + "Eyes/" + str(eyes) + ".png")
        img2 = Image.open(ASSETFOLDER + "Mouth/" + str(mouth) + ".png")

        # Paste Required PNGs
        img0.paste(img1, (0, 0), img1)
        data['attributes'].append(
            {
                'trait_type': 'Eyes',
                'value': eyeMap[eyes]
            })
        if(eyes == 7):
            Swag = Swag + 20
        if(eyes == 8):
            Swag = Swag + 25
            print("Diamond Eyes")
        img0.paste(img2, (0, 0), img2)
        data['attributes'].append(
            {
                'trait_type': 'Mouth',
                'value': mouthMap[mouth]
            })
        if(mouth == 7):
            Swag = Swag + 10
        # Open AND Paste Optional PNGs
        if(0 < hair < 9):
            img3 = Image.open(ASSETFOLDER + "Hair/" + str(hair) + ".png")
            img0.paste(img3, (0, 0), img3)
            data['attributes'].append(
                {
                    'trait_type': 'Hair',
                    'value': hairMap[hair]
                })
            if(3 < hair <= 6):
                Swag = Swag + 10
            if(hair >= 7):
                print("Possible Mullet")
                Swag = Swag + 15
        if(0 < facialHair <= 7):
            img4 = Image.open(ASSETFOLDER + "FacialHair/" +
                              str(facialHair) + ".png")
            img0.paste(img4, (0, 0), img4)
            data['attributes'].append(
                {
                    'trait_type': 'Facial Hair',
                    'value': facialHairMap[facialHair]
                })
            if(facialHair == 7):
                Swag = Swag + 10
            if(hair == 6):
                Swag = Swag + 5
        else:
            facialHair = 0
        if(0 < jewelry <= 5):
            img5 = Image.open(ASSETFOLDER + "Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
                })
            if(jewelry >= 4):
                Swag = Swag + 20
            else:
                Swag = Swag + 10
        else:
            jewelry = 0

        # Mask - If mask, no smoke, hat or glasses added
        if(0 < mask <= 5):
            if(mask < 3 and hair != 6):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
            if(mask == 5):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
                Swag = Swag + 45
            if(2 < mask < 5):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
                Swag = Swag + 35
            if(mask <= 2):
                img9 = Image.open(ASSETFOLDER + "Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
                Swag = Swag + 20
        else:
            if((0 < hat <= 4) and (hair != 6)):
                img7 = Image.open(ASSETFOLDER + "Hat/" + str(hat) + ".png")
                img0.paste(img7, (0, 0), img7)
                data['attributes'].append(
                    {
                        'trait_type': 'Hat',
                        'value': hatMap[hat]
                    })
                if(hat == 4):
                    Swag = Swag + 20
                else:
                    Swag = Swag + 10
            else:
                hat = 0
            if(0 < smoke <= 4):
                img6 = Image.open(ASSETFOLDER + "Smoke/" + str(smoke) + ".png")
                img0.paste(img6, (0, 0), img6)
                data['attributes'].append(
                    {
                        'trait_type': 'Smoke',
                        'value': smokeMap[smoke]
                    })
                Swag = Swag + 15
            else:
                smoke = 0
            if(0 < glasses <= 6):
                img8 = Image.open(ASSETFOLDER + "Glasses/" +
                                  str(glasses) + ".png")
                img0.paste(img8, (0, 0), img8)
                data['attributes'].append(
                    {
                        'trait_type': 'Glasses',
                        'value': glassesMap[glasses]
                    })
                if(glasses <= 3):
                    Swag = Swag + 15
                else:
                    Swag = Swag = 5
            else:
                glasses = 0
            mask = 0        # img0.show()
    data['attributes'].append(
        {
            'display_type': 'boost_number',
            'trait_type': 'Swag',
            'value': Swag
        })
    # print("Swag: {}".format(str(Swag)))

    # Create and save data
    folder = ASSETFOLDER + "Homies/"
    if not os.path.isdir(folder):
        os.mkdir(folder)

    # Saves images to single folder
    resized_img = img0.resize((300, 300), resample=Image.NEAREST)
    resized_img.save(folder + str(token_id) + '.png', "PNG")

    # Set image property of metadata
    data['image'] = "ipfs://FOLDER"  # mint will set number to end of base URI

    # img0.show()

    # Add image to IPFS
    with open(folder + str(token_id) + '.json', 'w') as f:
        json.dump(data, f)
