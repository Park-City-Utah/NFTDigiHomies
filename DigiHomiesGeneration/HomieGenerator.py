from PIL import Image
import numpy as np
import os as os
import json as json


def generateRandomNumber(lowIn, highIn):
    rng = np.random.default_rng()
    ranNumberArray = rng.integers(low=lowIn, high=highIn, size=1)
    return ranNumberArray[0]


def generateHomie(total):
    i = 1
    while i <= total:
        print("Iteration: " + str(i))

        # REQUIRED
        body = generateRandomNumber(1, 6)
        eyes = generateRandomNumber(1, 5)
        mouth = generateRandomNumber(1, 7)
        # OPTIONAL - higher range equals increase randomness, less likely to align with exisiting feature
        hair = generateRandomNumber(0, 7)
        print(str(hair))
        facialHair = generateRandomNumber(0, 10)
        jewelry = generateRandomNumber(0, 8)
        smoke = generateRandomNumber(0, 10)
        hat = generateRandomNumber(0, 25)
        glasses = generateRandomNumber(0, 15)
        mask = generateRandomNumber(0, 35)
        special = generateRandomNumber(0, 750)

        # Open Required pngs
        img0 = Image.open("Body/" + str(body) + ".png")
        img1 = Image.open("Eyes/" + str(eyes) + ".png")
        img2 = Image.open("Mouth/" + str(mouth) + ".png")

        # Pase Required PNGs
        img0.paste(img1, (0, 0), img1)
        img0.paste(img2, (0, 0), img2)

        # Open AND Paste Optional PNGs
        if(0 < hair <= 7):
            img3 = Image.open("Hair/" + str(hair) + ".png")
            img0.paste(img3, (0, 0), img3)

            if(0 < facialHair <= 7):
                img4 = Image.open("FacialHair/" + str(facialHair) + ".png")
                img0.paste(img4, (0, 0), img4)
            else:
                facialHair = 0
            if(0 < jewelry <= 5):
                img5 = Image.open("Jewelry/" + str(jewelry) + ".png")
                img0.paste(img5, (0, 0), img5)
            else:
                jewelry = 0

            if(0 < mask <= 5):
                img9 = Image.open("Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
            else:
                if(0 < smoke <= 3):
                    img6 = Image.open("Smoke/" + str(smoke) + ".png")
                    img0.paste(img6, (0, 0), img6)
                else:
                    smoke = 0
                if(0 < hat <= 4):
                    img7 = Image.open("Hat/" + str(hat) + ".png")
                    img0.paste(img7, (0, 0), img7)
                else:
                    hat = 0
                if(0 < glasses <= 7):
                    img8 = Image.open("Glasses/" + str(glasses) + ".png")
                    img0.paste(img8, (0, 0), img8)
                else:
                    glasses = 0
                mask = 0

            if(0 < special <= 3):
                img10 = Image.open("Special/" + str(special) + ".png")
                img0.paste(img10, (0, 0), img10)
                if(0 < smoke <= 3):
                    img6 = Image.open("Smoke/" + str(smoke) + ".png")
                    img0.paste(img6, (0, 0), img6)
                else:
                    smoke = 0
                if(0 < jewelry <= 5):
                    img5 = Image.open("Jewelry/" + str(jewelry) + ".png")
                    img0.paste(img5, (0, 0), img5)
            else:
                special = 0
        else:
            hair = 0

        attributes = {
            'body': body,
            'eyes': eyes,
            'mouth': mouth,
            'hair': hair,
            'facialHair': facialHair,
            'jewelry': jewelry,
            'smoke': smoke,
            'hat': hat,
            'glasses': glasses,
            'mask': mask,
            'special': special,
        }
        homieAttrString = str(attributes)
        # print(homieAttrString)
        # print(json.dumps(homieAttrString))

        # Generate Image
        img0.show()
        folder = "Homies/" + str(i) + "/"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        img0.save(folder + str(i) + '.png', "PNG")
        with open(folder + 'data.json', 'w') as f:
            json.dump(homieAttrString, f)

        i = i+1
