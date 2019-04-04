import random
import datetime

standardPets = ['Wolf 🐺', 'Tiger 🐯', 'Panda 🐼', 'Lion 🦁', 'Fox 🦊',
    'Flying Pig ✈️🐷', 'Dragon 🐲', 'Cactus 🌵', 'Bear 🐻']
questPets = ['Gryphon 🦅🦁', 'Hedgehog 🦔', 'Deer 🦌',
    'Egg 🥚 / Egg Basket 🥚🧺', 'Rat 🐀', 'Octopus 🐙', 'Seahorse 🌊🐎',
    'Parrot 🦜', 'Rooster 🐓', 'Spider 🕷️', 'Owl 🦉', 'Penguin 🐧',
    'Tyrannosaur 🦖', 'Rock 💎', 'Bunny 🐰', 'Marshmallow Slime 🍢', 'Sheep 🐑',
    'Cuttlefish 🐙🐟', 'Whale 🐋', 'Cheetah 🐆', 'Horse 🐎', 'Frog 🐸',
    'Snake 🐍', 'Unicorn / Winged Unicorn 🦄', 'Sabretooth Tiger 🦷🐅',
    'Monkey 🐒', 'Snail 🐌', 'Falcon 🦅', 'Treeling 🌳', 'Axolotl 🐡',
    'Sea Turtle / Giant Sea Turtle 🌊🐢', 'Armadillo', 'Cow 🐮', 'Beetle 🐞',
    'Ferret', 'Sloth 🦥', 'Triceratops 🦕🦏', 'Guinea Pig 🌊🐷', 'Peacock 🦚',
    'Caterpillar 🐛 / Butterfly 🦋', 'Nudibranch 🐟', 'Hippo 🦛',
    'Yarn / Flying Carpet 🧶', 'Pterodactyl 🦕🦇', 'Badger 🦡', 'Squirrel 🐿️',
    'Sea Serpent 🌊🐉', 'Kangaroo 🦘', 'Alligator 🐊', 'Velociraptor 🦕🐦']
specialPets = ['Veteran Wolf 🐺', 'Cerberus Pup 🐕', 'Hydra 🐉', 'Turkey 🦃',
    'Polar Bear Cub ☃️🐻', 'Mantis Shrimp 🦐', 'Jack-o-Lantern 🎃',
    'Wooly Mammoth 🐘', 'Veteran Tiger 🐯', 'Phoenix 🔥🐦', 'Gilded Turkey 🦃',
    'Magical Bee 🐝', 'Veteran Lion 🦁', 'Royal Purple Gryphon 🦅🦁',
    'Ghost Jack-o-Lantern 👻🎃', 'Royal Purple Jackalope 🐰🦌',
    'Orca 🐋', 'Veteran Bear 🐻', 'Hopeful Hippogriff 🦅🐎', 'Veteran Fox 🦊',
    'Glow-in-the-Dark Jack-o-Lantern 🎃']
specialMounts = ['Polar Bear ☃️🐻', 'Ethereal Lion 🦁', 'Mantis Shrimp 🦐',
    'Turkey 🦃', 'Wooly Mammoth 🐘', 'Orca 🐋', 'Royal Purple Gryphon 🦅🦁',
    'Phoenix 🔥🐦', 'Jack-o-Lantern 🎃', 'Magical Bee 🐝', 'Gilded Turkey 🦃',
    'Royal Purple Jackalope 🐰🦌', 'Invisible Aether',
    'Ghost Jack-o-Lantern 👻🎃', 'Hopeful Hippogriff 🦅🐎']
standardColours = ['Base', 'White', 'Desert', 'Red', 'Shade', 'Skeleton',
    'Zombie', 'Pink', 'Blue', 'Golden']
magicPotions = ['Royal Purple', 'Cupid', 'Shimmer', 'Fairy', 'Floral',
    'Aquatic', 'Ember', 'Thunderstorm', 'Spooky', 'Ghost', 'Holly',
    'Peppermint', 'Starry Night', 'Rainbow', 'Glass', 'Glow-in-the-Dark',
    'Frost', 'Icy Snow', 'Rose Quartz', 'Celestial']
petOrMount = ['Pet', 'Mount']

today = datetime.datetime.now().strftime('**%A %e')
if today.endswith('1'):
    today = today + datetime.datetime.now().strftime('st of %B:**\n')
elif today.endswith('2'):
    today = today + datetime.datetime.now().strftime('nd of %B:**\n')
elif today.endswith('3'):
    today = today + datetime.datetime.now().strftime('rd of %B:**\n')
else:
    today = today + datetime.datetime.now().strftime('th of %B:**\n')

print(today)

print("**Demonic beast:", random.choice(standardColours),
    random.choice(standardPets),
    random.choice(petOrMount), '**\n')

angelType = random.choice(specialPets + specialMounts + questPets + standardPets)
angelSize = "(pet or mount!)"
if angelType in standardPets:
    angelColor = random.choice(magicPotions)
elif angelType in questPets:
    angelColor = random.choice(standardColours)
else:
    angelColor = ''
    if angelType not in specialPets:
        angelSize = "(Mount!)"
    elif angelType not in specialMounts:
        angelSize = "(Pet!)"

print("**Angelic beast:", angelColor, angelType, angelSize, '**')
