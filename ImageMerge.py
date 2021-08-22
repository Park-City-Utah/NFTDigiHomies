from PIL import Image
import numpy as np

rng = np.random.default_rng()

i = 0
while i < 5000:

    # REQUIRED
    # generate random from 1-6
    base = rng.integers(low=1, high=6, size=1)
    print(base[0])

    # generate random from 1-5
    eyes = rng.integers(low=1, high=5, size=1)
    print(eyes[0])

    # generate random from 1-7
    mouth = rng.integers(low=1, high=7, size=1)
    print(mouth[0])

    # OPTIONAL
    # generate random from 1-5, (include 0)
    hair = rng.integers(low=0, high=8, size=1)
    print(hair[0])

    # generate random from 1-6, (include 0)
    facialHair = rng.integers(low=0, high=10, size=1)
    print(facialHair[0])

    # generate random from 1-5, (include 0)
    jewelry = rng.integers(low=0, high=8, size=1)
    print(jewelry[0])

    # generate random from 1-4, (include 0) make rare
    smoke = rng.integers(low=0, high=10, size=1)
    print(smoke[0])

    # generate random from 1-5, (include 0)
    hat = rng.integers(low=0, high=25, size=1)
    print(hat[0])

    # generate random from 1-7, (include 0)
    glasses = rng.integers(low=0, high=15, size=1)
    print(glasses[0])

    # generate random from 1-3, (include 0) make rare
    mask = rng.integers(low=0, high=50, size=1)
    print(mask[0])

    # generate random from 1-3, (include 0) make rare
    special = rng.integers(low=0, high=1000, size=1)
    print(special[0])

    # Open & paste to base if not 0
    base = Image.open("Base/" + str(base[0]) + ".png")
    # base.show()

    img1 = Image.open("Eyes/" + str(eyes[0]) + ".png")
    base.paste(img1, (0, 0), img1)
    # base.show()

    img2 = Image.open("Mouth/" + str(mouth[0]) + ".png")
    base.paste(img2, (0, 0), img2)
    # base.show()

    if(0 < hair[0] <= 6):
        img3 = Image.open("Hair/" + str(hair[0]) + ".png")
        base.paste(img3, (0, 0), img3)
    # base.show()

    if(0 < facialHair[0] <= 7):
        img4 = Image.open("FacialHair/" + str(facialHair[0]) + ".png")
        base.paste(img4, (0, 0), img4)
        # base.show()

    if(0 < jewelry[0] <= 5):
        img5 = Image.open("Jewelry/" + str(jewelry[0]) + ".png")
        base.paste(img5, (0, 0), img5)
        # base.show()

# If no mask
    if(mask[0] > 5):
        if(0 < smoke[0] <= 4):
            img6 = Image.open("Smoke/" + str(smoke[0]) + ".png")
            base.paste(img6, (0, 0), img6)
            # base.show()
        if(0 < hat[0] <= 4):
            img7 = Image.open("Hat/" + str(hat[0]) + ".png")
            base.paste(img7, (0, 0), img7)
        # base.show()
        if(0 < glasses[0] <= 7):
            img8 = Image.open("Glasses/" + str(glasses[0]) + ".png")
            base.paste(img8, (0, 0), img8)
            # base.show()

    if(0 < mask[0] <= 5):
        img9 = Image.open("Mask/" + str(mask[0]) + ".png")
        base.paste(img9, (0, 0), img9)
        # base.show()

    if(0 < special[0] <= 3):
        img10 = Image.open("Special/" + str(special[0]) + ".png")
        base.paste(img10, (0, 0), img10)
        # base.show()
        if(0 < smoke[0] <= 4):
            img6 = Image.open("Smoke/" + str(smoke[0]) + ".png")
            base.paste(img6, (0, 0), img6)
            # base.show()
        if(0 < jewelry[0] <= 5):
            img5 = Image.open("Jewelry/" + str(jewelry[0]) + ".png")
            base.paste(img5, (0, 0), img5)
        # base.show()

    # base.show()
    # Generate Image
    base.save("Homies/DigiHome" + str(i) + '.png', "PNG")
    i = i+1
