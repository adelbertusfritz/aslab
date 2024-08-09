from random import shuffle

baseAggro = {
    "The Hunt": 3,
    "Erudition": 3,
    "Harmony": 4,
    "Nihility": 4,
    "Abundance": 4,
    "Destruction": 5,
    "Preservation": 6,
}

database = {
    "Jingliu": {
        "path": "Destruction",
    },
    "Jing Yuan": {
        "path": "Erudition",
    },
    "Yingxin": {
        "path": "Destruction",
    },
    "Dan Heng": {
        "path": "The Hunt",
    },
}

party = []

charAggro = lambda path,m: baseAggro[path] * (1+m)

def hitProbability(target, party):
    Ak = charAggro(database[target["name"]]["path"], target["mod"])
    Ap = sum(charAggro(database[member["name"]]["path"], member["mod"]) for member in party)
    return Ak/Ap

member1 = input("Input the name of the main character: ")
print(f'{member1} is a character that follows the path of {database[member1]["path"]}')
mod1 = int(input("Input the 'Mukjizat' that the main character obtained: "))
print(f"{'#'*10} {member1} has received {mod1*100}% Mukjizat {'#'*10}")

member2 = input("Input the name of the 2nd character: ")
print(f'{member2} is a character that follows the path of {database[member2]["path"]}')
mod2 = int(input("Input the 'Mukjizat' that the 2nd character obtained: "))
print(f"{'#'*10} {member2} has received {mod2*100}% Mukjizat {'#'*10}")

member3 = input("Input the name of the 3rd character: ")
print(f'{member3} is a character that follows the path of {database[member3]["path"]}')
mod3 = int(input("Input the 'Mukjizat' that the 3rd character obtained: "))
print(f"{'#'*10} {member3} has received {mod3*100}% Mukjizat {'#'*10}")

member4 = input("Input the name of the 4th character: ")
print(f'{member4} is a character that follows the path of {database[member4]["path"]}')
mod4 = int(input("Input the 'Mukjizat' that the 4th character obtained: "))
print(f"{'#'*10} {member4} has received {mod4*100}% Mukjizat {'#'*10}")

party.append({ "name": member1, "mod": mod1 })
party.append({ "name": member2, "mod": mod2 })
party.append({ "name": member3, "mod": mod3 })
party.append({ "name": member4, "mod": mod4 })

for member in party:
    member["hitProb"] = hitProbability(member, party)
    member["hits"] = 0

for member in party:
    print(f"The chance {member['name']} get targeted is: {round(member['hitProb']*100, 3)}%")

breakpoints = [sum([party[i]["hitProb"] for i in range(j)]) for j in range(len(party))]
breakpoints.append(1)

monsterAttacks = int(input("Input the number of monster attacks: "))

attacks = [i for i in range(int(10*monsterAttacks))]
shuffle(attacks)
attacks = attacks[:monsterAttacks]
attacks = [attack/10/monsterAttacks for attack in attacks]

for attack in attacks:
    i = 0
    while breakpoints[i] < attack:
        i += 1
    i -= 1
    party[i]["hits"] += 1

print(f'Simulation of {monsterAttacks} monster attacks')
for member in party:
    print(f'{member["name"]} got hit {member["hits"]} times.')




bonus = 'Gimana jika bukan high cloud quintet'