while True:
    import random

    class Game:
        game_over = False
        new_monster = True
        dungeon_loop = False
        already_poisoned = False
        already_debuffed = False
        restart_boolean = ''
        quit_boolean = ''
        restart_once = 0
        quit_once = 0

    class Player(object):
        poisoned = False
        debuffed = False
        gold = 0
        inventory = []

        def __init__(self, max_hp, hp, max_ap, ap, weapon, armor):
            self.max_hp = max_hp
            self.hp = hp
            self.max_ap = max_ap
            self.ap = ap
            self.weapon = weapon
            self.armor = armor

    class PlayerAttack(object):

        def __init__(self, name, min_dmg, max_dmg, crit_chance, ap_cost):
            self.name = name
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg
            self.crit_chance = crit_chance
            self.ap_cost = ap_cost

    class Armor(object):

        def __init__(self, name, protection, cost, poison_resist, debuff_resist):
            self.name = name
            self.protection = protection
            self.cost = cost
            self.poison_resist = poison_resist
            self.debuff_resist = debuff_resist

    # Armor types
    cloth = Armor("Cloth", 1, 0, False, False)
    gambeson = Armor("Gambeson", 0.92, 15, False, False)
    chain_mail = Armor("Chain Mail Armor", 0.9, 30, True, False)
    plate_armor = Armor("Plate Armor", 0.88, 50, True, True)

    class Weapon(object):

        def __init__(self, name, bonus_dmg, cost, crit_dmg1, crit_dmg2, crit_chance):
            self.name = name
            self.bonus_dmg = bonus_dmg
            self.cost = cost
            self.crit_dmg1 = crit_dmg1
            self.crit_dmg2 = crit_dmg2
            self.crit_chance = crit_chance

    # weapon types
    dagger = Weapon("Dagger", 0, 0, 1, 3, 10)
    short_sword = Weapon("Short Sword", 3, 20, 3, 5, 10)
    battle_axe = Weapon("Battle Axe", 5, 40, 7, 9, 10)
    long_sword = Weapon("Long Sword", 9, 60, 9, 11, 10)

    # ----------------------------------------------

    class Monster(object):
    # I created a monster list to be able to get a random monster from it
        species = 'monster'
        gold_drop = 1
        min_poison = 7
        max_poison = 10
        monster_list = []

        def __init__(self, name, max_hp, hp, min_dmg, max_dmg, accuracy, poison, debuff):
            self.name = name
            self.max_hp = max_hp
            self.hp = hp
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg
            self.accuracy = accuracy
            self.poison = poison
            self.debuff = debuff
            __class__.monster_list.append(self)

    # Monster types
    goblin = Monster("Goblin", 80, 80, 10, 30, 90, False, False)
    spider = Monster("Giant Spider", 70, 70, 10, 20, 90, False, True)
    orc = Monster("Orc", 110, 110, 25, 40, 85, False, False)
    skeleton = Monster("Skeleton", 90, 90, 20, 30, 90, False, False)
    slime = Monster("Slime", 105, 105, 10, 15, 90, True, False)
    zombie = Monster("Zombie", 80, 80, 10, 30, 80, True, True)

    rand_index = random.randrange(len(Monster.monster_list))
    rand_monster = Monster.monster_list[rand_index]

    player = Player(120, 120, 10, 10, dagger, cloth)

    # Attack types
    slash = PlayerAttack("Slash", 15, 25, 10, 1)
    shredding_strike = PlayerAttack("Shredding Strike", 30, 40, 5, 3)

    #print("This {} is a {} and its hp is {}.".format(rand_monster.species, rand_monster.name, rand_monster.hp))

    # Functions----------------------------------------------------------------
    def player_info():
        print("HP: {}/{}  Armor: {}%\nAP: {}/{}    Gold: {}".format(player.hp, player.max_hp,
                                                                    int((1 - player.armor.protection) * 100)
                                                            ,player.ap, player.max_ap, player.gold))
        alt_line()

    def player_damage(ap_cost, min_dmg, max_dmg, attack_name):
        if player.ap >= ap_cost:
            player.ap -= ap_cost
            crit_check = random.randint(1, 100)
            if crit_check <= player.weapon.crit_chance:
                crit_dmg = random.randint(player.weapon.crit_dmg1, player.weapon.crit_dmg2)
                player_dmg = random.randint(min_dmg, max_dmg) + player.weapon.bonus_dmg + crit_dmg
                rand_monster.hp -= player_dmg
                print("************************\nCRITICAL HIT!\n************************\n"
                      "You used {} and did {} damage".format(attack_name, player_dmg))
            else:
                player_dmg = random.randint(min_dmg, max_dmg) + player.weapon.bonus_dmg
                rand_monster.hp -= player_dmg
                print("You used {} and did {} damage".format(attack_name, player_dmg))
        else:
            print("Not enough AP")

    def monster_info():
        if Game.new_monster is True:
            print("A {} has appeared!\n".format(rand_monster.name))
            Game.new_monster = False

        print("{} HP: {}/{}".format(rand_monster.name, rand_monster.hp, rand_monster.max_hp))

    def monster_accuracy():
        monster_acc = random.randint(1, 100)
        if monster_acc <= rand_monster.accuracy:
            return True
        else:
            return False

    def monster_respawn():
        global rand_monster
        global rand_index

        if rand_monster.hp <= 0 or Game.new_monster is True:
            Game.new_monster = True
            rand_monster.hp = rand_monster.max_hp
            rand_index = random.randrange(len(Monster.monster_list))
            rand_monster = Monster.monster_list[rand_index]

    def monster_damage():
        if rand_monster.hp > 0:
            if monster_accuracy() is True:
                monster_dmg = round(random.randint(rand_monster.min_dmg, rand_monster.max_dmg) * player.armor.protection)
                player.hp -= monster_dmg
                print("You have taken {} damage from the {}".format(monster_dmg, rand_monster.name))
                if rand_monster.poison is True:
                    poison_acc = random.randint(1, 100)
                    # 90 - 55 = 35% | 80 - 55 = 25%
                    if poison_acc <= rand_monster.accuracy - 55:
                        player.poisoned = True
                        print("The {} poisoned you (-{} to {} HP every turn)".format(rand_monster.name,
                                                    rand_monster.min_poison, rand_monster.max_poison))
                        poison_func()
                if rand_monster.debuff is True:
                    debuff_acc = random.randint(1, 100)
                    if debuff_acc <= rand_monster.accuracy - 55:
                        player.debuffed = True
                        debuff_func()
            else:
                print("The {}'s attack missed!".format(rand_monster.name))

    def poison_func():
        def poison_apply():
            if Game.already_poisoned is False:
                Game.already_poisoned = True
                poison_dmg = random.randint(rand_monster.min_poison, rand_monster.max_poison)
                player.hp -= poison_dmg
                print("You have taken {} damage from being poisoned".format(poison_dmg))

        if player.poisoned is True:
            if player.armor.poison_resist is True:
                rand_resist = random.randint(1, 100)
                # 20% chance
                if rand_resist <= 20:
                    player.poisoned = False
                    print("You resisted the poison")
                else:
                    poison_apply()
            else:
                poison_apply()


    def debuff_func():
        def debuff_apply():
            if Game.already_debuffed is False:
                Game.already_debuffed = True
                ap_loss = 3
                armor_loss = 0.08
                player.max_ap -= ap_loss
                player.armor.protection += armor_loss
                print("The {} weakened you (-{}% Armor and -{} Max AP)"
                      .format(rand_monster.name, int(armor_loss * 100), ap_loss))
                if player.ap > player.max_ap:
                    player.ap = player.max_ap

        if player.debuffed is True:
            if player.armor.debuff_resist is True:
                rand_resist = random.randint(1, 100)
                if rand_resist <= 20:
                    player.debuffed = False
                    print("You resisted the weaken")
                else:
                    debuff_apply()
            else:
                debuff_apply()

    def recover():
        if player.poisoned is True:
            rand_recover = random.randint(1, 100)
            if rand_recover <= 20:
                player.poisoned = False
                Game.already_poisoned = False
                print("You recovered from the poison")

        if player.debuffed is True:
            rand_recover = random.randint(1, 100)
            if rand_recover <= 20:
                player.debuffed = False
                Game.already_debuffed = False
                player.max_ap = 10
                player.armor.protection += 0.08
                print("You recovered from being weakened")

    def rewards():
        rand_monster.gold_drop = random.randint(1, 5)
        player.gold += rand_monster.gold_drop
        rand_hp = random.randint(5, 20)
        player.hp += rand_hp
        rand_ap = random.randint(0, 1)
        player.ap += rand_ap
        print("You gained {} gold".format(rand_monster.gold_drop))
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        if player.ap > player.max_ap:
            player.ap = player.max_ap
        print("You recovered {} HP and {} AP".format(rand_hp, rand_ap))
        line()

    def ap_gain():
        if player.hp > 0:
            if player.ap > player.max_ap:
                player.ap = player.max_ap
            else:
                rand_ap = random.randint(0, 2)
                if rand_ap != 0:
                    player.ap += rand_ap
                    print("You regained {} AP".format(rand_ap))
                    if player.ap > player.max_ap:
                        player.ap = player.max_ap
                    line()

    def line():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def alt_line():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")

    def invalid_option():
        print("************************\nChoose a valid option\n************************")

    def no_gold():
        line()
        print("Not enough gold")
        line()

    def dungeon():
        print("You entered the dungeon")
        while Game.dungeon_loop is True:
            while True:
                monster_info()
                alt_line()
                player_info()
                player_input = input("What will you do?\n1: {} ({} AP, {}-{} dmg)".format(slash.name, slash.ap_cost,
                            slash.min_dmg, slash.max_dmg) + "\n2: {} ({} AP, {}-{} dmg)".format(shredding_strike.name,
                            shredding_strike.ap_cost, shredding_strike.min_dmg, shredding_strike.max_dmg)
                            + "\n> ")
                line()
                if player_input == "1":
                    player_damage(slash.ap_cost, slash.min_dmg, slash.max_dmg, slash.name)
                    break
                elif player_input == "2":
                    player_damage(shredding_strike.ap_cost, shredding_strike.min_dmg, shredding_strike.max_dmg,
                                  shredding_strike.name)
                    break
                else:
                    invalid_option()

            restart()

            if restart() is True or False:
                break

            if rand_monster.hp <= 0:
                print("You defeated the {}!".format(rand_monster.name))
                rewards()
                player_info()
                monster_respawn()
                continue_loop = True
                while continue_loop is True:
                    player_input = input("1: Continue in the dungeon\n2: Go back to town\n> ")
                    if player_input == "2":
                        continue_loop = False
                        Game.dungeon_loop = False
                    elif player_input == "1":
                        continue_loop = False
                        line()
                    else:
                        invalid_option()
            else:
                monster_damage()

            recover()
            poison_func()
            ap_gain()

    def armor_shop():
        while True:
            player_info()
            # ADD PRICES ##################################
            player_input = input("Welcome to the Armor Shop!\nWhat will you buy?\n1: Gambeson Armor\n"
                                 "2: Chain Mail Armor\n3: Plate Armor\nq: Go back to town\n> ")
            if player_input == "1":
                if player.gold >= gambeson.cost:
                    if player.armor >= gambeson.protection:
                        print("You can't purchase this")
                    else:
                        player.armor = gambeson.protection
                        print("You purchased Gambeson Armor!\n+1 Armor")
                else:
                    no_gold()
            elif player_input == "2":
                if player.gold >= chain_mail.cost:
                    if player.armor >= chain_mail.protection:
                        print("You can't purchase this")
                    else:
                        player.armor = chain_mail.protection
                        print("You purchased Chain Mail Armor!")
                else:
                    no_gold()
            elif player_input == "3":
                if player.gold >= plate_armor.cost:
                    if player.armor >= plate_armor.protection:
                        print("You can't purchase this")
                    else:
                        player.armor = plate_armor.protection
                        print("You purchased Plate Armor!")
                else:
                    no_gold()
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def weapon_shop():
        while True:
            player_info()
            player_input = input("Welcome to the Weapon Shop!\nWhat will you buy?\n1: Gambeson Armor\n"
                                 "2: Chain Mail Armor\n3: Plate Armor\nq: Go back to town\n> ")
            if player_input == "1":
                if player.gold >= short_sword.cost:
                    if player.armor >= gambeson.protection:
                        print("You can't purchase this")
                    else:
                        player.armor = gambeson.protection
                        print("You purchased Gambeson Armor!\n+1 Armor")
                else:
                    no_gold()
            elif player_input == "2":
                if player.gold >= chain_mail.cost:
                    if player.armor >= chain_mail.protection:
                        print("You can't purchase this")
                    else:
                        player.armor = chain_mail.protection
                        print("You purchased Chain Mail Armor!")
                else:
                    no_gold()
            elif player_input == "3":
                if player.gold >= plate_armor.cost:
                    if player.armor >= plate_armor.protection:
                        print("You can't purchase this")
                    else:
                        player.armor = plate_armor.protection
                        print("You purchased Plate Armor!")
                else:
                    no_gold()
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def town():
        if Game.dungeon_loop is False:
            town_loop = True
            while town_loop is True:
                player_input = input("Welcome to the small village of Seronia!\nWhere will you go?\n1: Armor Shop\n"
                                     "2: Weapon Shop\n3: Potion Shop\n4: Dungeon\nq: Quit\n> ")
                line()
                if player_input == "1":
                    armor_shop()
                elif player_input == "2":
                    print("Welcome to the Weapon Shop!")
                elif player_input == "3":
                    print("Welcome to the Potion Shop")
                elif player_input == "4":
                    town_loop = False
                    Game.dungeon_loop = True
                    dungeon()
                elif player_input.lower() == "q":
                    quit_func()
                    if Game.quit_boolean is True:
                        break
                else:
                    invalid_option()
                line()

    def restart():
        if player.hp <= 0:
            while Game.restart_once == 0:
                player_input = input("You died\nRestart? (y/n)\n> ")
                if player_input.lower() == "n":
                    Game.game_over = True
                    Game.dungeon_loop = False
                    Game.restart_boolean = False
                    Game.restart_once = 1
                    break
                elif player_input.lower() == "y":
                    Game.dungeon_loop = False
                    Game.restart_boolean = True
                    Game.restart_once = 1
                    break
                else:
                    invalid_option()
        return Game.restart_boolean

    def quit_func():
        while Game.quit_once == 0:
            player_input = input("Are you sure? (y/n)\n> ")
            if player_input.lower() == "y":
                Game.game_over = True
                Game.quit_boolean = True
                Game.quit_once = 1
            elif player_input.lower() == "n":
                Game.quit_boolean = False
                Game.quit_once = 1
            else:
                invalid_option()
        Game.quit_once = 0

    # Game Start------------------------------------------------------------------
    while Game.game_over is False:
        if restart() is True or False:
            break
        town()
    break

"""Ideas
-monsters drop treasure that you can sell in town
-after a certain amount of defeated enemies, player is able to choose a different path
-passive money making building to purchase in town
-merchant who can upgrade your max hp and ap
-Rob the shop but can't use shops for a certain period of time
-Add a tavern where you can gamble
"""