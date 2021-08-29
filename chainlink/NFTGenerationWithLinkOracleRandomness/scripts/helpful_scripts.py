from pathlib import Path
from brownie import (
    network,
    accounts,
    config,
    LinkToken,
    MockV3Aggregator,
    MockOracle,
    VRFCoordinatorMock,
    Contract,
)
from web3 import Web3
from PIL import Image
import numpy as np
import os as os
import json as json
from pathlib import Path
import requests

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

contract_to_mock = {
    "link_token": LinkToken,
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "oracle": MockOracle,
}

DECIMALS = 18
INITIAL_VALUE = Web3.toWei(2000, "ether")


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """If you want to use this function, go to the brownie config and add a new entry for
    the contract that you want to be able to 'get'. Then add an entry in the in the variable 'contract_to_mock'.
    You'll see examples like the 'link_token'.
        This script will then either:
            - Get a address from the config
            - Or deploy a mock to use for a network that doesn't have it

        Args:
            contract_name (string): This is the name that is refered to in the
            brownie config and 'contract_to_mock' variable.

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            Contract of the type specificed by the dictonary. This could be either
            a mock or the 'real' contract on a live network.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try:
            contract_address = config["networks"][network.show_active(
            )][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=1000000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # Keep this line to show how it could be done without deploying a mock
    # tx = interface.LinkTokenInterface(link_token.address).transfer(
    #     contract_address, amount, {"from": account}
    # )
    tx = link_token.transfer(contract_address, amount, {"from": account})
    print("Funded {}".format(contract_address))
    return tx


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock VRFCoordinator...")
    mock_vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account}
    )
    print(f"Deployed to {mock_vrf_coordinator.address}")

    print("Deploying Mock Oracle...")
    mock_oracle = MockOracle.deploy(link_token.address, {"from": account})
    print(f"Deployed to {mock_oracle.address}")
    print("Mocks Deployed!")

# Required - random generation to exclude 0 'get_<feature>'


def get_body(body_number):
    switch = {
        0: 'Thin Light',
        1: 'Thin Mid',
        2: 'Thin Dark',
        3: 'Thick Light',
        4: 'Thick Mid',
        5: 'Thick Dark'
    }
    print(body_number)
    print(switch[body_number])
    return switch[body_number]


def get_eyes(eye_number):
    switch = {
        0: 'Normal',
        1: 'Peep',
        2: 'Squint',
        3: 'Peer',
        4: 'Gold',
    }
    print(eye_number)
    print(switch[eye_number])
    return switch[eye_number]


def get_mouth(mouth_number):
    switch = {
        0: 'Normal',
        1: 'Grin',
        2: 'Smile',
        3: 'Ohh',
        4: 'Lips',
        5: 'Missing Tooth',
        6: 'Gold Tooth'
    }
    print(mouth_number)
    print(switch[mouth_number])
    return switch[mouth_number]

# Optional random generation to include 0 'get_<feature>'


def get_hair(hair_number):
    switch = {
        1: 'Black',
        2: 'Brown',
        3: 'Gray',
        4: 'Pink',
        5: 'Comb-Over',
        6: 'Man-Bun',
        7: 'Corn-Rows',
        8: 'Mullet'
    }
    print(hair_number)
    print(switch[hair_number])
    return switch[hair_number]


def get_facialHair(facialHair_number):
    switch = {
        1: 'Light',
        2: 'Stuble',
        3: 'Handle-Bar Beard',
        4: 'Light Handle-Bar Beard',
        5: 'Grey Beard',
        6: 'Moustache',
        7: 'Handle-Bar'
    }
    print(facialHair_number)
    print(switch[facialHair_number])
    return switch[facialHair_number]


def get_jewelry(jewelry_number):
    switch = {
        1: 'Gold Chain',
        2: 'Gold Chain & Earring',
        3: 'Diamond Chain',
        4: 'Diamond Chain, Earring & Nose Ring',
        5: 'XL Gold Chain & Diamond Earring'
    }
    print(jewelry_number)
    print(switch[jewelry_number])
    return switch[jewelry_number]


def get_smoke(smoke_number):
    switch = {
        1: 'Cigarette',
        2: 'Joint Sativa',
        3: 'Jeferey',
        4: 'Joint Indica'
    }
    print(smoke_number)
    print(switch[smoke_number])
    return switch[smoke_number]


def get_hat(hat_number):
    switch = {
        1: 'Bonzai',
        2: 'Backwards Cap',
        3: 'DuRag',
        4: 'Crown'
    }
    print(hat_number)
    print(switch[hat_number])
    return switch[hat_number]


def get_glasses(glasses_number):
    switch = {
        1: 'Carerra',
        2: 'Miami',
        3: 'Dahmer',
        4: 'Dahmer - Dark',
        5: 'Pink Stunners',
        6: 'Patch'
    }
    print(glasses_number)
    print(switch[glasses_number])
    return switch[glasses_number]


def get_mask(mask_number):
    switch = {
        1: 'Balaklava',
        2: 'Ninja',
        3: 'Doom',
        4: 'Doom 2',
        5: 'Jason'
    }
    print(mask_number)
    print(switch[mask_number])
    return switch[mask_number]


def get_special(special_number):
    switch = {
        1: 'Alien',
        2: 'Death'
    }
    print(special_number)
    print(switch[special_number])
    return switch[special_number]


def generateHomie(random, token_id, data):
    # i = 1
    # while i <= total:
    # print("Iteration: " + str(i))

    # TODO - replace with link oracle random number & modulo range %7 = 0-6, %7+1 = 1-7
    # REQUIRED
    body = (random % 6)+1  # 0-5, +1 = 1-6
    eyes = (random % 5) + 1  # 0-4, +1 = 1-5
    mouth = (random % 7) + 1  # 0-6, +1 = 1-7
    # OPTIONAL - higher range equals increase randomness, less likely to align with exisiting feature
    hair = random % 8  # 0-7#
    facialHair = random % 10  # 0-10, only 7 but 7/10 is less likely
    jewelry = random % 8  # 0-8, only 5 but 5/8 is less likely
    smoke = random % 10  # 0-10, only 4 but 4/10 is less likely
    hat = random % 25  # 0-25, only 4 but 4/25 is less likely
    glasses = random % 15  # 0-15, only 6 but 6/15 is less likely
    mask = random % 35  # 0-35, only 5 but 5/35 is less likely
    special = random % 1500  # 0-1500, only 2 but 2/1500 is less likely

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
        img0 = Image.open("Assets/Special/" + str(special) + ".png")
        data['attributes'].append(
            {
                'trait_type': 'Special',
                'value': specialMap[special]
            })
        print('Special' + str(special))
        Swag = Swag + 80
        if(0 < smoke <= 4):
            img6 = Image.open("Assets/Smoke/" + str(smoke) + ".png")
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
            img5 = Image.open("Assets/Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
                })
            if(jewelry >= 4):
                Swag = Swag + 10
            else:
                Swag = Swag + 5
    else:
        special = 0

        # Open Required pngs
        img0 = Image.open("Assets/Body/" + str(body) + ".png")
        data['attributes'].append(
            {
                'trait_type': 'Body',
                'value': bodyMap[body]
            })
        if(body > 3):
            Swag = Swag + 10
        img1 = Image.open("Assets/Eyes/" + str(eyes) + ".png")
        img2 = Image.open("Assets/Mouth/" + str(mouth) + ".png")

        # Paste Required PNGs
        img0.paste(img1, (0, 0), img1)
        data['attributes'].append(
            {
                'trait_type': 'Eyes',
                'value': eyeMap[eyes]
            })
        if(eyes == 5):
            Swag = Swag + 10
        img0.paste(img2, (0, 0), img2)
        data['attributes'].append(
            {
                'trait_type': 'Mouth',
                'value': mouthMap[mouth]
            })
        if(mouth == 7):
            Swag = Swag + 10
        # Open AND Paste Optional PNGs
        if(0 < hair <= 8):
            img3 = Image.open("Assets/Hair/" + str(hair) + ".png")
            img0.paste(img3, (0, 0), img3)
            data['attributes'].append(
                {
                    'trait_type': 'Hair',
                    'value': hairMap[hair]
                })
            if(3 < hair <= 6):
                Swag = Swag + 5
            if(hair >= 7):
                Swag = Swag + 10
        if(0 < facialHair <= 7):
            img4 = Image.open("Assets/FacialHair/" +
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
            img5 = Image.open("Assets/Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
                })
            if(jewelry >= 4):
                Swag = Swag + 10
            else:
                Swag = Swag + 5
        else:
            jewelry = 0

        # Mask - If mask, no smoke, hat or glasses added
        if(0 < mask <= 5):
            if(mask < 3 and hair != 6):
                img9 = Image.open("Assets/Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
            if(mask == 5):
                Swag = Swag + 25
            if(2 < mask < 5):
                Swag = Swag + 20
            if(mask <= 2):
                Swag = Swag + 10
        else:
            if(0 < smoke <= 4):
                img6 = Image.open("Assets/Smoke/" + str(smoke) + ".png")
                img0.paste(img6, (0, 0), img6)
                data['attributes'].append(
                    {
                        'trait_type': 'Smoke',
                        'value': smokeMap[smoke]
                    })
                Swag = Swag + 10
            else:
                smoke = 0
            if((0 < hat <= 4) and (hair != 6)):
                img7 = Image.open("Assets/Hat/" + str(hat) + ".png")
                img0.paste(img7, (0, 0), img7)
                data['attributes'].append(
                    {
                        'trait_type': 'Hat',
                        'value': hatMap[hat]
                    })
                if(hat == 4):
                    Swag = Swag + 10
                else:
                    Swag = Swag + 5
            else:
                hat = 0
            if(0 < glasses <= 6):
                img8 = Image.open("Assets/Glasses/" +
                                  str(glasses) + ".png")
                img0.paste(img8, (0, 0), img8)
                data['attributes'].append(
                    {
                        'trait_type': 'Glasses',
                        'value': glassesMap[glasses]
                    })
                if(glasses <= 3):
                    Swag = Swag + 10
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
    # Create and save data
    folder = "Assets/Homies/{}/".format(str(token_id))
    if not os.path.isdir(folder):
        os.mkdir(folder)

    # Resize image - maintain quality
    # back = Image.open("Background/backGround.png")
    # back.paste(img0, (0, 0), img0)
    resized_img = img0.resize((350, 350), resample=Image.NEAREST)
    resized_img.save(folder + str(token_id) + '.png', "PNG")

    data['image'] = 'ipfs://QmdGqDw4MuAov7wFZkmLd2H29sMcFN6kmPLranX7rUSd1i'
    with open(folder + 'data.json', 'w') as f:
        json.dump(data, f)

    img0.show()

    # IPFS upload
    image_to_upload = None
    if os.getenv("UPLOAD_IPFS") == "true":
        image_path = "{}{}/{}.png".format(folder, str(token_id), str(token_id))
        print('ImagePath' + image_path)
    image_to_upload = upload_to_ipfs(image_path)
 #  i = i+1


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(
            ipfs_url + "/api/v0/add", files={"file": image_binary})
        print(response.json())


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
        2: 'Peep',
        3: 'Squint',
        4: 'Peer',
        5: 'Gold',
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
        3: 'Handle-Bar Beard',
        4: 'Light Handle-Bar Beard',
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
        3: 'Dahmer',
        4: 'Dahmer - Dark',
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
