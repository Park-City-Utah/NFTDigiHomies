from PIL import Image
import numpy as np


def generateRandomNumber(lowIn, highIn):
    rng = np.random.default_rng()
    ranNumberArray = rng.integers(low=lowIn, high=highIn, size=1)
    return ranNumberArray[0]


def generateHomie(total):
    i = 1
    while i <= total:
        print("Iteration: " + str(i))

        # REQUIRED
        # generate random from 1-6
        base = generateRandomNumber(1, 5)

        # generate random from 1-5
        eyes = generateRandomNumber(1, 5)

        # generate random from 1-7
        mouth = generateRandomNumber(1, 7)

        # OPTIONAL
        # generate random from 1-7, (include 0)
        hair = generateRandomNumber(0, 7)

        # generate random from 1-6, (include 0)
        facialHair = generateRandomNumber(0, 10)

        # generate random from 1-5, (include 0)
        jewelry = generateRandomNumber(0, 8)

        # generate random from 1-4, (include 0) make rare
        smoke = generateRandomNumber(0, 10)

        # generate random from 1-5, (include 0)
        hat = generateRandomNumber(0, 25)

        # generate random from 1-7, (include 0)
        glasses = generateRandomNumber(0, 15)

        # generate random from 1-3, (include 0) make rare
        mask = generateRandomNumber(0, 50)

        # generate random from 1-3, (include 0) make rare
        special = generateRandomNumber(0, 1000)

        # Open & paste to base if not 0
        base = Image.open("Base/" + str(base) + ".png")
        # base.show()

        img1 = Image.open("Eyes/" + str(eyes) + ".png")
        base.paste(img1, (0, 0), img1)
        # base.show()

        img2 = Image.open("Mouth/" + str(mouth) + ".png")
        base.paste(img2, (0, 0), img2)
        # base.show()

        if(0 < hair <= 7):
            img3 = Image.open("Hair/" + str(hair) + ".png")
            base.paste(img3, (0, 0), img3)
            # base.show()

            if(0 < facialHair <= 7):
                img4 = Image.open("FacialHair/" + str(facialHair) + ".png")
                base.paste(img4, (0, 0), img4)
                # base.show()

            if(0 < jewelry <= 5):
                img5 = Image.open("Jewelry/" + str(jewelry) + ".png")
                base.paste(img5, (0, 0), img5)
                # base.show()

        # If no mask
            if(mask > 5):
                if(0 < smoke <= 4):
                    img6 = Image.open("Smoke/" + str(smoke) + ".png")
                    base.paste(img6, (0, 0), img6)
                    # base.show()
                if(0 < hat <= 4):
                    img7 = Image.open("Hat/" + str(hat) + ".png")
                    base.paste(img7, (0, 0), img7)
                # base.show()
                if(0 < glasses <= 7):
                    img8 = Image.open("Glasses/" + str(glasses) + ".png")
                    base.paste(img8, (0, 0), img8)
                    # base.show()

            if(0 < mask <= 5):
                img9 = Image.open("Mask/" + str(mask) + ".png")
                base.paste(img9, (0, 0), img9)
                # base.show()

            if(0 < special <= 3):
                img10 = Image.open("Special/" + str(special) + ".png")
                base.paste(img10, (0, 0), img10)
                # base.show()
                if(0 < smoke <= 4):
                    img6 = Image.open("Smoke/" + str(smoke) + ".png")
                    base.paste(img6, (0, 0), img6)
                    # base.show()
                if(0 < jewelry <= 5):
                    img5 = Image.open("Jewelry/" + str(jewelry) + ".png")
                    base.paste(img5, (0, 0), img5)
                # base.show()

            # base.show()
            # Generate Image
            base.save("Homies/" + str(i) + '.png', "PNG")

        i = i+1
