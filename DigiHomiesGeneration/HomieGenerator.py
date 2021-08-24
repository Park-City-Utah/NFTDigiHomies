from PIL import Image
import numpy as np
import os as os
import json as json
from GenerateFeatureMap import *


def generateRandomNumber(lowIn, highIn):
    rng = np.random.default_rng()
    ranNumberArray = rng.integers(low=lowIn, high=highIn, size=1)
    return int(ranNumberArray[0])


def generateHomie(total):
    i = 1
    while i <= total:
        print("Iteration: " + str(i))

        # TODO - replace with link oracle random number & modulo range %7 = 0-6, %7+1 = 1-7
        # REQUIRED
        body = generateRandomNumber(1, 6)
        eyes = generateRandomNumber(1, 5)
        mouth = generateRandomNumber(1, 7)
        # OPTIONAL - higher range equals increase randomness, less likely to align with exisiting feature
        hair = generateRandomNumber(0, 8)
        facialHair = generateRandomNumber(0, 10)
        jewelry = generateRandomNumber(0, 8)
        smoke = generateRandomNumber(0, 10)
        hat = generateRandomNumber(0, 25)
        glasses = generateRandomNumber(0, 15)
        mask = generateRandomNumber(0, 35)
        special = generateRandomNumber(0, 1500)

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
        data = createDataMap(i)

        # Special characteristic - Allow smoke & jewelry only
        if(0 < special <= 2):
            img0 = Image.open("Special/" + str(special) + ".png")
            data['attributes'].append(
                {
                    'trait_type': 'Special',
                    'value': specialMap[special]
                })
            print('Special' + str(i))
            if(0 < smoke <= 4):
                img6 = Image.open("Smoke/" + str(smoke) + ".png")
                img0.paste(img6, (0, 0), img6)
                data['attributes'].append(
                    {
                        'trait_type': 'Smoke',
                        'value': smokeMap[smoke]
                    })
            else:
                smoke = 0

            if(0 < jewelry <= 5):
                img5 = Image.open("Jewelry/" + str(jewelry) + ".png")
                img0.paste(img5, (0, 0), img5)
                data['attributes'].append(
                    {
                        'trait_type': 'Jewelry',
                        'value': jewelryMap[jewelry]
                    })
            img0.show()
        else:
            special = 0

            # Open Required pngs
            img0 = Image.open("Body/" + str(body) + ".png")
            data['attributes'].append(
                {
                    'trait_type': 'Body',
                    'value': bodyMap[body]
                })
            img1 = Image.open("Eyes/" + str(eyes) + ".png")
            img2 = Image.open("Mouth/" + str(mouth) + ".png")

            # Paste Required PNGs
            img0.paste(img1, (0, 0), img1)
            data['attributes'].append(
                {
                    'trait_type': 'Eyes',
                    'value': eyeMap[eyes]
                })
            img0.paste(img2, (0, 0), img2)
            data['attributes'].append(
                {
                    'trait_type': 'Mouth',
                    'value': mouthMap[mouth]
                })

            # Open AND Paste Optional PNGs
            if(0 < hair <= 8):
                img3 = Image.open("Hair/" + str(hair) + ".png")
                img0.paste(img3, (0, 0), img3)
                data['attributes'].append(
                    {
                        'trait_type': 'Hair',
                        'value': hairMap[hair]
                    })
            if(0 < facialHair <= 7):
                img4 = Image.open("FacialHair/" + str(facialHair) + ".png")
                img0.paste(img4, (0, 0), img4)
                data['attributes'].append(
                    {
                        'trait_type': 'Facial Hair',
                        'value': facialHairMap[facialHair]
                    })
            else:
                facialHair = 0
            if(0 < jewelry <= 5):
                img5 = Image.open("Jewelry/" + str(jewelry) + ".png")
                img0.paste(img5, (0, 0), img5)
                data['attributes'].append(
                    {
                        'trait_type': 'Jewelry',
                        'value': jewelryMap[jewelry]
                    })
            else:
                jewelry = 0

            # Mask - If mask, no smoke, hat or glasses added
            if(0 < mask <= 5):
                img9 = Image.open("Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
            else:
                if(0 < smoke <= 4):
                    img6 = Image.open("Smoke/" + str(smoke) + ".png")
                    img0.paste(img6, (0, 0), img6)
                    data['attributes'].append(
                        {
                            'trait_type': 'Smoke',
                            'value': smokeMap[smoke]
                        })
                else:
                    smoke = 0
                if(0 < hat <= 4):
                    img7 = Image.open("Hat/" + str(hat) + ".png")
                    img0.paste(img7, (0, 0), img7)
                    data['attributes'].append(
                        {
                            'trait_type': 'Hat',
                            'value': hatMap[hat]
                        })
                else:
                    hat = 0
                if(0 < glasses <= 6):
                    img8 = Image.open("Glasses/" + str(glasses) + ".png")
                    img0.paste(img8, (0, 0), img8)
                    data['attributes'].append(
                        {
                            'trait_type': 'Glasses',
                            'value': glassesMap[glasses]
                        })
                else:
                    glasses = 0
                mask = 0        # img0.show()

        # Resize image - maintain quality
        resized_img = img0.resize((350, 350), resample=Image.NEAREST)

        # Create and save data
        folder = "Homies/" + str(i) + "/"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        resized_img.save(folder + str(i) + '.png', "PNG")

        with open(folder + 'data.json', 'w') as f:
            json.dump(data, f)

        i = i+1
