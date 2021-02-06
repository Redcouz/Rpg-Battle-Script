from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random

# Create Black Magic----------------------------------------------------
fire = Spell("Fire", 6, 60, "black")
thunder = Spell("Thunder", 7, 70, "black")
blizzard = Spell("Blizzard", 5, 50, "black")
meteor = Spell("Meteor", 8, 80, "black")
quake = Spell("Quake", 10, 100, "black")

# Create White Magic----------------------------------------------------
cure = Spell("Cure", 5, 100, "white")
cura = Spell("Cura", 10, 250, "white")

# Create Some Items------------------------------------------------------
potion = Item("Potion", "potion", "Heals 50 hp", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MEGAELIXER", "elixer", "Fully restores party HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 Damage", 500)

# Put magic and items in player----------------------------------------------
player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"items": potion, "quantity": 15}, {"items": hipotion, "quantity": 5},
                {"items": superpotion, "quantity": 1}, {"items": elixer, "quantity": 2},
                {"items": hielixer, "quantity": 1}, {"items": grenade, "quantity": 2}]

# Instantiate People--------------------------------------------------------
player1 = Person("Tank ", 3600, 65, 100, 100, player_magic, player_items)
player2 = Person("DPS  ", 2000, 100, 300, 50, player_magic, player_items)
player3 = Person("Wizz ", 1250, 300, 50, 25, player_magic, player_items)

enemy1 = Person("ETank ", 9000, 65, 45, 125, player_magic, player_items)
enemy2 = Person("EDPS  ", 4000, 100, 150, 25, player_magic, player_items)
enemy3 = Person("EWizz ", 1000, 65, 300, 25, player_magic, player_items)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


running = True
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

# Initiate Battle Loop--------------------------------------------------------
while running:
    # Choose Action and print HP/MP Bars
    print("===========================")
    print("NAME                            HP                                          MP           ")

    # Update HP/MP Bars

    for player in players:
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.enemy_get_stats()

    for player in players:
        player.choose_action()
        index = int(input("Choose Action: ")) - 1

        # Checking input for actions----------------------------
        if index == 0:
            print("------------------------------------")
            print(bcolors.FAIL + "You choose", str(player.actions[index]) + bcolors.ENDC)
            enemy_choice = player.choose_target(enemies)

            # Basic attack---------------------------------------
            dmg = player.generate_damage()

            enemies[enemy_choice].take_damage(dmg)
            print(bcolors.OKGREEN + "You Deal", dmg, "Points of Damage", "To", enemies[enemy_choice].name + bcolors.ENDC)
            print("------------------------------------")
            if enemies[enemy_choice].get_hp() == 0:
                print(enemies[enemy_choice].name + " has died.")
                del enemies[enemy_choice]

        if index == 1:

            # Choose Magic----------------------------------------
            print("------------------------------------")
            print(bcolors.OKBLUE + "You Choose " + str(player.actions[index]) + bcolors.ENDC)

            player.choose_magic()
            magic_choice = int(input("Choose Spell: ")) - 1
            print("------------------------------------")

            # Go back to menu choice------------------------------
            if magic_choice == -1:
                continue

            # Recognize damage and name for the spell chosen----------------------
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            # Checking mana cost-------------------------------------------------
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not Enough MP" + bcolors.ENDC)
                continue

            # Reduce MP------------------------------------------
            player.reduce_mp(spell.cost)

            # Checking type of spell, if white heals, if black hits-------------------------
            if spell.type == "white":

                player.heal(magic_dmg)

                if player.get_hp() > player.get_hp_max():
                    player.put_hp_max()
                print(bcolors.OKBLUE + spell.name + " Heals for", str(magic_dmg), "HP" + bcolors.ENDC)
                print("------------------------------------")
            elif spell.type == "black":

                enemy_choice = player.choose_target(enemies)
                enemies[enemy_choice].take_damage(magic_dmg)

                print(bcolors.OKBLUE + spell.name + " deals", str(magic_dmg), "Points of damage" +
                     " To " + enemies[enemy_choice].name + bcolors.ENDC)

                if enemies[enemy_choice].get_hp() == 0:
                    print(enemies[enemy_choice].name + " has died.")
                    del enemies[enemy_choice]

        elif index == 2:

            # Choose Items------------------------------------------
            print("------------------------------------")
            player.choose_item()
            item_choice = int(input("Choose Item: ")) - 1
            print("------------------------------------")

            # Go back to menu choice--------------------------------------
            if item_choice == -1:
                continue

            # Recognize item chosen-----------------------------
            item = player.items[item_choice]["items"]

            # Reduce Items Quantity, prevent negative quantities------------------------------
            if player.items[item_choice]["quantity"] <= 0:

                player.items[item_choice]["quantity"] = 0
                print(bcolors.FAIL + "You don´t have more " + str(item.name) + bcolors.ENDC)
                continue

            else:
                player.items[item_choice]["quantity"] -= 1

            # Recognize item type. If potion cure HP, elixer cure hp and mp, attack do damage---------
            if item.type == "potion":
                player.heal(item.props)

                if player.get_hp() > player.get_hp_max():
                    player.put_hp_max()
                print(bcolors.OKBLUE + "You drink a " + item.name + " and Heals for", str(item.props),
                      "HP" + bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "Elixer":
                    player.put_hp_max()
                    player.put_mp_max()
                    print(bcolors.HEADER + "You healed your HP and your MP completely with an " + item.name + bcolors.ENDC)

                elif item.name == "MEGAELIXER":

                    for player in players:
                        player.put_hp_max()
                        player.put_mp_max()
                    print(bcolors.HEADER + "You healed your Party HP and your MP completely with an " + item.name + bcolors.ENDC)

            elif item.type == "attack":

                enemy_choice = player.choose_target(enemies)
                enemies[enemy_choice].take_damage(item.props)
                print(bcolors.WARNING + "You throw a " + item.name + " and you dealt " + str(item.props) +
                      " Damage" + " To " + enemies[enemy_choice].name  + bcolors.ENDC)

                if enemies[enemy_choice].get_hp() == 0:
                    print(enemies[enemy_choice].name + " has died.")
                    del enemies[enemy_choice]

        # For wrong input----------------------------------------------------
        elif index != 0 & index != 1 & index != 2:
            print("Choose correct Action")

            continue


        # Win or loose condition--------------------------------------
        defeated_enemies = 0
        defeated_players = 0

        for enemy in enemies:
            if enemy.get_hp() == 0:
                defeated_enemies += 1

        for player in players:
            if player.get_hp() == 0:
                defeated_players += 1

        if defeated_players == 3:
            print(bcolors.FAIL + "You Loose" + bcolors.ENDC)
            running = False
        if defeated_enemies == 3:
            print(bcolors.OKGREEN + "You Win" + bcolors.ENDC)
            running = False


        # Enemy Attack Phase------------------------------
        for enemy in enemies:
            e_choice = random.randrange(0, 3)
            percentage_hp = (enemy.hp / enemy.get_hp_max()) * 100

            if percentage_hp < 30:
                e_choice = 1
            elif percentage_hp < 10:
                e_choice = 2
            if e_choice == 0:
                enemy_dmg = enemy.generate_damage()
                target = random.randrange(0, 3)
                players[target].take_damage(enemy_dmg)
                print(bcolors.WARNING + enemy.name + " attacks for " +
                      str(enemy_dmg) + " to " + players[target].name + bcolors.ENDC)

                print("------------------------------------")

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]


            elif e_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                enemy.reduce_mp(spell.cost)

                if percentage_hp < 30:
                    spell = enemy.magic[6]

                if spell.type == "white":

                    enemy.heal(magic_dmg)

                    if enemy.get_hp() > enemy.get_hp_max():
                        enemy.put_hp_max()
                    print(bcolors.OKBLUE + enemy.name+ " use " + spell.name + ". Heals for", str(magic_dmg), "HP" + bcolors.ENDC)
                    print("------------------------------------")

                elif spell.type == "black":
                    target = random.randrange(0, 3)
                    players[target].take_damage(magic_dmg)

                    print(bcolors.OKBLUE + enemy.name + " use " + spell.name + " and deals", str(magic_dmg), "Points of damage" +
                          " To " + players[target].name + bcolors.ENDC)
                    print("------------------------------------")
                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]

            elif e_choice == 2:
                item, item_props, item_choice = enemy.choose_enemy_item()
                if percentage_hp < 10:
                    item = enemy.items[4]
                enemy.items[item_choice]["quantity"] -= 1

                # Recognize item type. If potion cure HP, elixer cure hp and mp, attack do damage---------
                if item["items"].type == "potion":
                    enemy.heal(item_props)

                    if enemy.get_hp() > enemy.get_hp_max():
                        enemy.put_hp_max()
                    print(bcolors.OKBLUE + "The enemy " + enemy.name + " drink a " + item["items"].name + " and Heals for",
                          str(item["items"].props),
                          "HP" + bcolors.ENDC)
                    print("------------------------------------")

                elif item["items"].type == "elixer":

                    if item["items"].name == "Elixer":
                        enemy.put_hp_max()
                        enemy.put_mp_max()
                        print(bcolors.HEADER + "Enemy " + enemy.name + " healed his HP and MP completely with an " + item["items"].name
                              + bcolors.ENDC)
                        print("------------------------------------")

                    elif item["items"].name == "MEGAELIXER":

                        for enemy in enemies:
                            enemy.put_hp_max()
                            enemy.put_mp_max()
                        print(bcolors.HEADER + "The enemy " +
                              enemy.name + "healed his Party HP and MP completely with an " + item["items"].name + bcolors.ENDC)
                        print("------------------------------------")
                elif item["items"].type == "attack":

                    target = random.randrange(0, 3)
                    players[target].take_damage(item_props)
                    print(bcolors.WARNING + enemy.name + "throw a " + item["items"].name + " and dealt " + str(item["items"].props) +
                          " Damage" + " To " + players[target].name + bcolors.ENDC)
                    print("------------------------------------")
                    if players[target].get_hp() == 0:
                        print(players[target].name + " has died.")
                        del players[target]









