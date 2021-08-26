# Mappings for feature and data (json file)

def createDataMap(i):
    dataMap = {
        'name': 'DigiHomie #' + str(i),
        'description': 'An Eternal Etherium Digital Homie!',
        'image': 'ipfs://<hash>',
        'background_color': '0F7CB3',
        'attributes': []
    }
    return dataMap


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
