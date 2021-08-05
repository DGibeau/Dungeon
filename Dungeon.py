while True:
    import random
    game_over = False
    new_monster = True
    dungeon_loop = False
    already_debuffed = False
    restart_boolean = ''
    quit_boolean = ''
    restart_once = 0
    quit_once = 0

    class Player(object):
        poisoned = False
        debuffed = False
        gold = 0
        armor = 0
        poison_resist = False
        debuff_resist = False
        inventory = []

        def __init__(self, max_hp, hp, max_ap, ap):
            self.max_hp = max_hp
            self.hp = hp
            self.max_ap = max_ap
            self.ap = ap

    player = Player(20, 20, 10, 10)


    class PlayerAttack(object):

        def __init__(self, name, min_dmg, max_dmg, ap_cost):
            self.name = name
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg
            self.ap_cost = ap_cost

    slash = PlayerAttack("Slash", 2, 3, 1)
    shredding_strike = PlayerAttack("Shredding Strike", 4, 5, 3)

    class Armor(object):

        def __init__(self, name, protection, poison_resist, debuff_resist):
            self.name = name
            self.protection = protection
            self.poison_resist = poison_resist
            self.debuff_resist = debuff_resist

    gambeson = Armor("Gambeson", 1, False, False)
    chain_mail = Armor("Chain Mail Armor", 2, True, False)
    plate_armor = Armor("Plate Armor", 3, True, True)

    # ----------------------------------------------

    class Monster(object):
    # I created a monster list to be able to get a random monster from it
        species = 'monster'
        gold_drop = 1
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

    goblin = Monster("Goblin", 8, 8, 1, 3, 1, False, False)
    spider = Monster("Giant Spider", 7, 7, 1, 2, 1, False, True)
    orc = Monster("Orc", 15, 15, 3, 5, 2, False, False)
    skeleton = Monster("Skeleton", 9, 9, 2, 3, 1, False, False)
    slime = Monster("Slime", 13, 13, 1, 1, 1, True, False)
    zombie = Monster("Zombie", 8, 8, 1, 3, 2, True, True)

    rand_index = random.randrange(len(Monster.monster_list))
    rand_monster = Monster.monster_list[rand_index]

    #print("This {} is a {} and its hp is {}.".format(rand_monster.species, rand_monster.name, rand_monster.hp))

    # Functions----------------------------------------------------------------
    def player_info():
        print("HP: {}/{}\nAP: {}/{}   Gold: {}".format(player.hp, player.max_hp, player.ap, player.max_ap, player.gold))
        alt_line()

    def monster_info():
        global new_monster

        if new_monster is True:
            print("A {} has appeared!\n".format(rand_monster.name))
            new_monster = False

        print("{} HP: {}/{}".format(rand_monster.name, rand_monster.hp, rand_monster.max_hp))

    def monster_accuracy():
        monster_acc = random.randint(1, 10)
        if monster_acc > rand_monster.accuracy:
            return True
        else:
            return False

    def monster_respawn():
        global new_monster
        global rand_monster
        global rand_index

        if rand_monster.hp <= 0 or new_monster is True:
            new_monster = True
            rand_monster.hp = rand_monster.max_hp
            rand_index = random.randrange(len(Monster.monster_list))
            rand_monster = Monster.monster_list[rand_index]

    def monster_damage():
        if rand_monster.hp > 0:
            if monster_accuracy() is True:
                monster_dmg = random.randint(rand_monster.min_dmg, rand_monster.max_dmg)
                player.hp -= monster_dmg
                print("You have taken {} damage from the {}".format(monster_dmg, rand_monster.name))
                if rand_monster.poison is True:
                    poison_acc = random.randint(1, 10)
                    # 1 + 5 makes it a 40% chance 2 + 5 = 30%
                    if poison_acc > rand_monster.accuracy + 5:
                        player.poisoned = True
                        print("The {} poisoned you (-1 hp every turn)".format(rand_monster.name))
                        poison()
                if rand_monster.debuff is True:
                    debuff_acc = random.randint(1, 10)
                    if debuff_acc > rand_monster.accuracy + 5:
                        player.debuffed = True
                        print("The {} weakened you (-1 armor and -3 max AP)".format(rand_monster.name))
                        debuff()
            else:
                print("The {}'s attack missed!".format(rand_monster.name))

    def poison():
        def poison_apply():
            player.hp -= 1
            print("You have taken 1 damage from being poisoned")

        if player.poisoned is True:
            if player.poison_resist is True:
                rand_resist = random.randint(1, 10)
                if rand_resist > 8:
                    player.poisoned = False
                    print("You resisted the poison")
                else:
                    poison_apply()
            else:
                poison_apply()


    def debuff():
        def debuff_apply():
            global already_debuffed

            if already_debuffed is False:
                already_debuffed = True
                player.max_ap -= 3
                if player.ap > player.max_ap:
                    player.ap = player.max_ap
                if player.armor <= 0:
                    print("Your max AP has been reduced to {}".format(player.max_ap))
                else:
                    player.armor -= 1
                    print("Your armor has been reduced to {}\nYour max AP has been reduced to {}"
                          .format(player.armor, player.max_ap))

        if player.debuffed is True:
            if player.debuff_resist is True:
                rand_resist = random.randint(1, 10)
                if rand_resist > 8:
                    player.debuffed = False
                    print("You resisted the weaken")
                else:
                    debuff_apply()
            else:
                debuff_apply()

    def recover():
        global already_debuffed

        if player.poisoned is True:
            rand_recover = random.randint(1,10)
            if rand_recover > 8:
                player.poisoned = False
                print("You recovered from the poison")

        if player.debuffed is True:
            rand_recover = random.randint(1, 10)
            if rand_recover > 8:
                player.debuffed = False
                already_debuffed = False
                player.max_ap = 10
                player.armor = 0
                print("You recovered from being weakened")

    def player_damage(ap_cost, min_dmg, max_dmg, attack_name):
        if player.ap >= ap_cost:
            player.ap -= ap_cost
            player_dmg = random.randint(min_dmg, max_dmg)
            rand_monster.hp -= player_dmg
            print("You used {} and did {} damage".format(attack_name, player_dmg))
        else:
            print("Not enough AP")

    def rewards():
        rand_monster.gold_drop = random.randint(1, 5)
        player.gold += rand_monster.gold_drop
        rand_hp = random.randint(2, 3)
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

    def dungeon():
        global dungeon_loop

        print("You entered the dungeon")
        while dungeon_loop is True:
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
                        dungeon_loop = False
                    elif player_input == "1":
                        continue_loop = False
                        line()
                    else:
                        invalid_option()
            else:
                monster_damage()

            recover()
            poison()
            ap_gain()

    def armor_shop():
        shop_loop = True
        while shop_loop is True:
            player_input = input("Welcome to the Armor Shop!\nWhat will you buy?\n1: Gambeson Armor\n"
                                 "2: Chain Mail Armor\n3: Plate Armor\nq: Go back to town\n> ")
            if player_input == "1":
                print("You purchased Gambeson Armor!")
            elif player_input == "2":
                print("You purchased Chain Mail Armor!")
            elif player_input == "3":
                print("You purchased Plate Armor!")
            elif player_input.lower() == "q":
                shop_loop = False
            else:
                invalid_option()

    def town():
        global dungeon_loop

        if dungeon_loop is False:
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
                    dungeon_loop = True
                    dungeon()
                elif player_input.lower() == "q":
                    quit()
                    if quit_boolean is True:
                        break
                else:
                    invalid_option()
                line()

    def restart():
        global game_over
        global dungeon_loop
        global restart_once
        global restart_boolean

        if player.hp <= 0:
            while restart_once == 0:
                player_input = input("You died\nRestart? (y/n)\n> ")
                if player_input.lower() == "n":
                    game_over = True
                    dungeon_loop = False
                    restart_boolean = False
                    restart_once = 1
                    break
                elif player_input.lower() == "y":
                    dungeon_loop = False
                    restart_boolean = True
                    restart_once = 1
                    break
                else:
                    invalid_option()
        return restart_boolean

    def quit():
        global quit_once
        global quit_boolean
        global game_over

        while quit_once == 0:
            player_input = input("Are you sure? (y/n)\n> ")
            if player_input.lower() == "y":
                game_over = True
                quit_boolean = True
                quit_once = 1
            elif player_input.lower() == "n":
                quit_boolean = False
                quit_once = 1
            else:
                invalid_option()
        quit_once = 0

    # Game Start------------------------------------------------------------------
    while game_over is False:
        if restart() is True or False:
            break
        town()
    break