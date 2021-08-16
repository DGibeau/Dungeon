# Current bugs: coming soon
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
        turns_staggered = 0

    class Player(object):
        poisoned = False
        debuffed = False
        temp_armor = False
        stagger_value = 15
        gold = 0
        max_inventory = 3
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
    gambeson = Armor("Gambeson", 0.92, 25, False, False)
    chain_mail = Armor("Chain Mail Armor", 0.9, 50, True, False)
    plate_armor = Armor("Plate Armor", 0.88, 90, True, True)

    class Weapon(object):

        def __init__(self, name, bonus_dmg, cost, crit_mult, crit_chance):
            self.name = name
            self.bonus_dmg = bonus_dmg
            self.cost = cost
            self.crit_mult = crit_mult
            self.crit_chance = crit_chance

    # weapon types
    dagger = Weapon("Dagger", 0, 0, 1.4, 10)
    short_sword = Weapon("Short Sword", 2, 25, 1.5, 10)
    battle_axe = Weapon("Battle Axe", 4, 50, 1.6, 10)
    long_sword = Weapon("Long Sword", 6, 80, 1.7, 10)

    class Potion(object):

        def __init__(self, name, short_name, effect_value, cost):
            self.name = name
            self.short_name = short_name
            self.effect_value = effect_value
            self.cost = cost

    hp_potion = Potion("HP Potion", "HP", 40, 10)
    ap_potion = Potion("AP Potion", "AP", 4, 10)
    dmg_potion = Potion("Blast Potion", "dmg", 25, 10)

    # ------------------------------------------------------------------------------------

    class Monster(object):
    # I created a monster list to be able to get a random monster from it
        staggered = False
        gold_drop = 1
        min_poison = 5
        max_poison = 10
        monster_list = []

        def __init__(self, name, max_hp, hp, min_dmg, max_dmg, accuracy, stagger_resist, poison, debuff):
            self.name = name
            self.max_hp = max_hp
            self.hp = hp
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg
            self.accuracy = accuracy
            self.stagger_resist = stagger_resist
            self.poison = poison
            self.debuff = debuff
            __class__.monster_list.append(self)

    # Monster types
    goblin = Monster("Goblin", 80, 80, 10, 30, 90, 35, False, False)
    spider = Monster("Giant Spider", 70, 70, 10, 20, 90, 40, False, True)
    orc = Monster("Orc", 115, 115, 25, 40, 85, 70, False, False)
    skeleton = Monster("Skeleton", 90, 90, 20, 30, 90, 35, False, False)
    slime = Monster("Slime", 110, 110, 10, 15, 90, 70, True, False)
    zombie = Monster("Zombie", 80, 80, 10, 30, 85, 40, True, True)

    rand_index = random.randrange(len(Monster.monster_list))
    rand_monster = Monster.monster_list[rand_index]

    player = Player(120, 120, 12, 12, dagger, cloth)

    # Attack types
    slash = PlayerAttack("Slash", 15, 25, 5, 1)
    shredding_strike = PlayerAttack("Shredding Strike", 30, 40, 0, 3)
    stagger_stab = PlayerAttack("Stagger Stab", 12, 15, 10, 2)
    critical_cleave = PlayerAttack("Critical Cleave", 15, 20, 30, 5)


    class TavernOption(object):
        temp_effect = 3

        def __init__(self, name, cost, effect1, effect2):
            self.name = name
            self.cost = cost
            self.effect1 = effect1
            self.effect2 = effect2


    drink = TavernOption("Drink", 5, 2, 0.03)
    meal = TavernOption("Meal", 10, 40, 2)
    sleep = TavernOption("Sleep", 25, player.max_hp, player.max_ap)

    # Functions----------------------------------------------------------------
    def player_info():
        if player.poisoned is True:
            print("HP: {}/{}▼  Armor: {}%\nAP: {}/{}    Gold: {}".format(player.hp, player.max_hp,
                                                                        int((1 - player.armor.protection) * 100)
                                                                        , player.ap, player.max_ap, player.gold))
        else:
            print("HP: {}/{}✚  Armor: {}%♜\nAP: {}/{}►    Gold: {}Ⓖ".format(player.hp, player.max_hp,
                                                            int((1 - player.armor.protection) * 100)
                                                            ,player.ap, player.max_ap, player.gold))
        for item in player.inventory:
            print(item.name, end = " | ")
        if len(player.inventory) != 0:
            print("")
        alt_line()

    def player_damage(ap_cost, min_dmg, max_dmg, attack_name, attack_crit):
        if player.ap >= ap_cost:
            player.ap -= ap_cost
            crit_check = random.randint(1, 100)
            if crit_check <= player.weapon.crit_chance + attack_crit:
                if attack_name == critical_cleave.name and rand_monster.hp > 99:
                        player_dmg = round(
                            (random.randint(min_dmg, max_dmg) + player.weapon.bonus_dmg) * (2 + player.weapon.crit_mult))
                        rand_monster.hp -= player_dmg
                        print("************************\nSUPER CRITICAL HIT!\n************************\n"
                              "You used {} and did {} damage".format(attack_name, player_dmg))
                else:
                    player_dmg = round((random.randint(min_dmg, max_dmg) + player.weapon.bonus_dmg)
                                       * player.weapon.crit_mult)
                    rand_monster.hp -= player_dmg
                    print("************************\nCRITICAL HIT!\n************************\n"
                          "You used {} and did {} damage".format(attack_name, player_dmg))
            else:
                player_dmg = random.randint(min_dmg, max_dmg) + player.weapon.bonus_dmg
                rand_monster.hp -= player_dmg
                print("You used {} and did {} damage".format(attack_name, player_dmg))
        else:
            print("************************\nNot enough AP\n************************")

    def inventory_func():
        def item_choice(slot):
            if player.inventory[slot] == hp_potion:
                player.hp += hp_potion.effect_value
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                del player.inventory[slot]
                line()
                print("You drank the {} and gained {} HP".format(hp_potion.name, hp_potion.effect_value))
                if player.poisoned is True:
                    player.poisoned = False
                    Game.already_poisoned = False
                    print("You cured the poison")
                line()
            elif player.inventory[slot] == ap_potion:
                line()
                if player.debuffed is True:
                    player.debuffed = False
                    Game.already_debuffed = False
                    player.max_ap = 12
                    player.armor.protection -= 0.08
                    print("You cured the weaken")
                player.ap += ap_potion.effect_value
                del player.inventory[slot]
                print("You drank the {} and gained {} AP".format(ap_potion.name, ap_potion.effect_value))
                line()
                if player.ap > player.max_ap:
                    player.ap = player.max_ap
            elif player.inventory[slot] == dmg_potion:
                rand_monster.hp -= dmg_potion.effect_value
                del player.inventory[slot]
                line()
                print("You used the {} and did {} damage to the {}".format(dmg_potion.name,
                                                                dmg_potion.effect_value, rand_monster.name))
                line()

        item_num = 1
        while True:
            for item in player.inventory:
                print(str(item_num) + ": " + item.name + " | {} {}".format(item.effect_value, item.short_name))
                item_num += 1
            item_num = 1
            player_input = input("q: go back\n> ")
            if player_input == "1":
                item_choice(0)
                break
            elif player_input == "2":
                if len(player.inventory) >= 2:
                    item_choice(1)
                    break
                else:
                    invalid_option()
            elif player_input == "3":
                if len(player.inventory) >= 3:
                    item_choice(2)
                    break
                else:
                    invalid_option()
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def temp_effects():
        if player.temp_armor is True:
            drink.temp_effect -= 1
            if drink.temp_effect <= 0:
                player.armor.protection += 0.03
                player.temp_armor = False
                drink.temp_effect = 3
                print("The drink wore off")


    def stagger_func():
        rand_stagger = random.randint(1, 100)
        if rand_stagger >= rand_monster.stagger_resist:
            if rand_monster.staggered is False:
                rand_monster.staggered = True
                rand_monster.accuracy -= player.stagger_value
                print("The {} has been staggered".format(rand_monster.name))
            elif rand_monster.staggered is True:
                print("The {} is already staggered".format(rand_monster.name))
        else:
            print("The {} resisted the stagger ({}s have a {}% chance to resist)".format(
                    rand_monster.name, rand_monster.name, rand_monster.stagger_resist))

    def stagger_recover():
        if rand_monster.staggered is True:
            Game.turns_staggered += 1
            if Game.turns_staggered >= 3:
                rand_monster.staggered = False
                rand_monster.accuracy += player.stagger_value
                Game.turns_staggered = 0
                print("The {} recovered from being staggered".format(rand_monster.name))

    def monster_info():
        if Game.new_monster is True:
            print("A {} has appeared!\n".format(rand_monster.name))
            Game.new_monster = False

        if rand_monster.staggered is True:
            print("{} HP: {}/{}".format(rand_monster.name, rand_monster.hp, rand_monster.max_hp), end=" ")
            print("-{}% Acc".format(player.stagger_value))
        elif rand_monster.staggered is False:
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
            if rand_monster.staggered is True:
                rand_monster.accuracy += 20
                rand_monster.staggered = False
                Game.turns_staggered = 0
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
                    # 90 - 55 = 35% | 85 - 55 = 30%
                    if poison_acc <= rand_monster.accuracy - 55 and Game.already_poisoned is False:
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
        if player.poisoned is True:
            if player.armor.poison_resist is True:
                rand_resist = random.randint(1, 100)
                # 20% chance
                if rand_resist <= 20:
                    player.poisoned = False
                    print("You resisted the poison")
                else:
                    Game.already_poisoned = True
            else:
                Game.already_poisoned = True


    def poison_dmg_func():
        if Game.already_poisoned is True:
            poison_dmg = random.randint(rand_monster.min_poison, rand_monster.max_poison)
            player.hp -= poison_dmg
            print("You have taken {} damage from being poisoned".format(poison_dmg))

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

    def recover(chance):
        if player.poisoned is True:
            rand_recover = random.randint(1, 100)
            if rand_recover <= chance:
                player.poisoned = False
                Game.already_poisoned = False
                print("You recovered from the poison")

        if player.debuffed is True:
            rand_recover = random.randint(1, 100)
            if rand_recover <= chance:
                player.debuffed = False
                Game.already_debuffed = False
                player.max_ap = 12
                player.armor.protection -= 0.08
                print("You recovered from being weakened")

    def rewards():
        rand_monster.gold_drop = random.randint(8, 15)
        player.gold += rand_monster.gold_drop
        rand_hp = random.randint(20, 30)
        player.hp += rand_hp
        rand_ap = random.randint(1, 2)
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
                rand_ap = random.randint(1, 2)
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
        def inventory_option():
            if len(player.inventory) != 0:
                print("e: Use items")

        print("You entered the dungeon")
        while Game.dungeon_loop is True:
            stagger_recover()
            poison_dmg_func()
            recover(20)
            temp_effects()
            while True:
                monster_info()
                alt_line()
                player_info()
                print("What will you do?\n1: {} ({} AP, {}-{} dmg)\n"
                                    "2: {} ({} AP, {}-{} dmg)\n"
                                    "3: {} ({} AP, {}-{} dmg & -{}% enemy accuracy)\n"
                                    "4: {} ({} AP, {}-{} dmg & {}% crit chance & 3x crit vs 100+ HP enemies)"
                    .format(slash.name, slash.ap_cost, slash.min_dmg, slash.max_dmg,
                    shredding_strike.name, shredding_strike.ap_cost, shredding_strike.min_dmg, shredding_strike.max_dmg,
                    stagger_stab.name, stagger_stab.ap_cost, stagger_stab.min_dmg, stagger_stab.max_dmg, player.stagger_value,
                    critical_cleave.name, critical_cleave.ap_cost, critical_cleave.min_dmg, critical_cleave.max_dmg,
                            critical_cleave.crit_chance + player.weapon.crit_chance))
                inventory_option()
                player_input = input("> ")
                line()
                if player_input == "1":
                    player_damage(slash.ap_cost, slash.min_dmg, slash.max_dmg, slash.name, slash. crit_chance)
                    break
                elif player_input == "2":
                    player_damage(shredding_strike.ap_cost, shredding_strike.min_dmg, shredding_strike.max_dmg,
                                  shredding_strike.name, shredding_strike.crit_chance)
                    break
                elif player_input == "3":
                    player_damage(stagger_stab.ap_cost, stagger_stab.min_dmg, stagger_stab.max_dmg,
                                  stagger_stab.name, stagger_stab.crit_chance)
                    stagger_func()
                    break
                elif player_input == "4":
                    player_damage(critical_cleave.ap_cost, critical_cleave.min_dmg, critical_cleave.max_dmg,
                                  critical_cleave.name, critical_cleave.crit_chance)
                    break
                elif player_input.lower() == "e":
                    if len(player.inventory) != 0:
                        inventory_func()
                        if rand_monster.hp <= 0:
                            break
                    else:
                        invalid_option()
                else:
                    invalid_option()

            if rand_monster.hp <= 0:
                print("You defeated the {}!".format(rand_monster.name))
                rewards()
                player_info()
                monster_respawn()
                continue_loop = True
                while continue_loop is True:
                    player_input = input("1: Continue in the dungeon\nq: Go back to town\n> ")
                    if player_input.lower() == "q":
                        continue_loop = False
                        Game.dungeon_loop = False
                    elif player_input == "1":
                        continue_loop = False
                        line()
                    else:
                        invalid_option()
            else:
                monster_damage()

            restart()
            if Game.restart_boolean is True or False:
                break

            ap_gain()

    def armor_shop():
        while True:
            player_info()
            player_input = input("Welcome to the Armor Shop!\nWhat will you buy?\n"
                                 "1: Gambeson | {} Gold (+{}% Armor)\n"
                                 "2: Chain Mail Armor | {} Gold (+{}% Armor & +20% poison resistance)\n"
                                 "3: Plate Armor | {} Gold (+{}% Armor & +20% poison & weaken resistance)\n"
                                 "q: Go back to town\n> ".format(gambeson.cost, int((1 - gambeson.protection) * 100),
                                                            chain_mail.cost, int((1 - chain_mail.protection) * 100),
                                                            plate_armor.cost, int((1 - plate_armor.protection) * 100)))
            if player_input == "1":
                if player.gold >= gambeson.cost:
                    if player.armor.protection <= gambeson.protection:
                        line()
                        print("You can't purchase this")
                        line()
                    else:
                        player.gold -= gambeson.cost
                        player.armor = gambeson
                        if player.debuffed is True:
                            player.armor.protection += 0.08
                        line()
                        print("You purchased {}!".format(gambeson.name))
                        line()
                else:
                    no_gold()
            elif player_input == "2":
                if player.gold >= chain_mail.cost:
                    if player.armor.protection <= chain_mail.protection:
                        line()
                        print("You can't purchase this")
                        line()
                    else:
                        player.gold -= chain_mail.cost
                        player.armor = chain_mail
                        if player.debuffed is True:
                            player.armor.protection += 0.08
                        line()
                        print("You purchased {}!".format(chain_mail.name))
                        line()
                else:
                    no_gold()
            elif player_input == "3":
                if player.gold >= plate_armor.cost:
                    if player.armor.protection <= plate_armor.protection:
                        line()
                        print("You can't purchase this")
                        line()
                    else:
                        player.gold -= plate_armor.cost
                        player.armor = plate_armor
                        if player.debuffed is True:
                            player.armor.protection += 0.08
                        line()
                        print("You purchased {}!".format(plate_armor.name))
                        line()
                else:
                    no_gold()
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def weapon_shop():
        while True:
            player_info()
            player_input = input("Welcome to the Weapon Shop!\nWhat will you buy?\n"
                                 "1: Short Sword | {} Gold (+{} dmg, x{} crit multiplier)\n"
                                 "2: Battle Axe | {} Gold (+{} dmg, x{} crit multiplier)\n"
                                 "3: Long Sword | {} Gold (+{} dmg, x{} crit multiplier)\n"
                                 "q: Go back to town\n> ".format(short_sword.cost, short_sword.bonus_dmg,
                                                                 short_sword.crit_mult,
                                                        battle_axe.cost, battle_axe.bonus_dmg, battle_axe.crit_mult,
                                                        long_sword.cost, long_sword.bonus_dmg, long_sword.crit_mult))
            if player_input == "1":
                if player.gold >= short_sword.cost:
                    if player.weapon.bonus_dmg >= short_sword.bonus_dmg:
                        line()
                        print("You can't purchase this")
                        line()
                    else:
                        player.gold -= short_sword.cost
                        player.weapon = short_sword
                        line()
                        print("You purchased a {}!".format(short_sword.name))
                        line()
                else:
                    no_gold()
            elif player_input == "2":
                if player.gold >= battle_axe.cost:
                    if player.weapon.bonus_dmg >= battle_axe.bonus_dmg:
                        line()
                        print("You can't purchase this")
                        line()
                    else:
                        player.gold -= battle_axe.cost
                        player.weapon = battle_axe
                        line()
                        print("You purchased a {}!".format(battle_axe.name))
                        line()
                else:
                    no_gold()
            elif player_input == "3":
                if player.gold >= long_sword.cost:
                    if player.weapon.bonus_dmg >= long_sword.bonus_dmg:
                        line()
                        print("You can't purchase this")
                        line()
                    else:
                        player.gold -= long_sword.cost
                        player.weapon = long_sword
                        line()
                        print("You purchased a {}!".format(long_sword.name))
                        line()
                else:
                    no_gold()
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def potion_shop():
        while True:
            player_info()
            player_input = input("Welcome to the Potion Shop!\nWhat will you buy?\n"
                                 "1: {} | {} Gold (+{} HP on use & cures poison)\n"
                                 "2: {} | {} Gold (+{} AP on use & cures weaken)\n"
                                 "3: {} | {} Gold ({} dmg on use)\n"
                                 "q: Go back to town\n> "
                                 .format(hp_potion.name, hp_potion.cost, hp_potion.effect_value,
                                    ap_potion.name, ap_potion.cost, ap_potion.effect_value,
                                    dmg_potion.name, dmg_potion.cost, dmg_potion.effect_value))
            if player_input == "1":
                if player.gold >= hp_potion.cost:
                    if len(player.inventory) >= player.max_inventory:
                        line()
                        print("Your inventory is full")
                        line()
                    else:
                        player.gold -= hp_potion.cost
                        player.inventory.append(hp_potion)
                        line()
                        print("You purchased an {}!".format(hp_potion.name))
                        line()
                else:
                    no_gold()
            elif player_input == "2":
                if player.gold >= ap_potion.cost:
                    if len(player.inventory) >= player.max_inventory:
                        line()
                        print("Your inventory is full")
                        line()
                    else:
                        player.gold -= ap_potion.cost
                        player.inventory.append(ap_potion)
                        line()
                        print("You purchased an {}!".format(ap_potion.name))
                        line()
                else:
                    no_gold()
            elif player_input == "3":
                if player.gold >= dmg_potion.cost:
                    if len(player.inventory) >= player.max_inventory:
                        line()
                        print("Your inventory is full")
                        line()
                    else:
                        player.gold -= dmg_potion.cost
                        player.inventory.append(dmg_potion)
                        line()
                        print("You purchased a {}!".format(dmg_potion.name))
                        line()
                else:
                    no_gold()
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def tavern():
        while True:
            player_info()
            player_input = input("You arrive at the Tavern\nWhat will you do?\n"
                                 "1: Enter\n"
                                 "2: Enter the alleyway\n"
                                 "q: Go back to town\n> ")
            if player_input == "1":
                while True:
                    player_info()
                    player_input = input("Welcome to the Tavern!\nWhat will you do?\n"
                                    "1: Buy a Drink | 5 gold (+2 AP +3% Armor temporarily)\n"
                                    "2: Buy a Meal | 10 gold (+40 HP +2 AP)\n"
                                    "3: Buy a room for the night | 25 gold (restores HP & AP & removes debuffs)\n"
                                    "q: Go back to the tavern\n> ")
                    if player_input == "1":
                        if player.gold >= drink.cost:
                            player.gold -= drink.cost
                            player.ap += drink.effect1
                            if player.temp_armor is False:
                                player.armor.protection -= drink.effect2
                            player.temp_armor = True
                            if player.ap > player.max_ap:
                                player.ap = player.max_ap
                            print("You purchased and drank the {}".format(drink.name))
                        else:
                            no_gold()
                    elif player_input == "2":
                        if player.gold >= meal.cost:
                            player.gold -= meal.cost
                            player.hp += meal.effect1
                            player.ap += meal.effect2
                            if player.hp > player.max_hp:
                                player.hp = player.max_hp
                            if player.ap > player.max_ap:
                                player.ap = player.max_ap
                            print("You purchased and ate the {}".format(meal.name))
                        else:
                            no_gold()
                    elif player_input == "3":
                        if player.gold >= sleep.cost:
                            player.gold -= sleep.cost
                            recover(100)
                            player.hp = sleep.effect1
                            player.ap = sleep.effect2
                            print("You purchased a room and went to {}\nYou wake up feeling great".format(sleep.name))
                        else:
                            no_gold()
                    elif player_input.lower() == "q":
                        break
                    else:
                        invalid_option()
                    line()
            elif player_input == "2":
                print("Welcome to my special shop, stranger")
            elif player_input.lower() == "q":
                break
            else:
                invalid_option()

    def inspect_gear():
        print("Armor: {} (+{}% Armor, Poison Resist: {}, Weaken Resist: {})\n"
              "Weapon: {} (+{} dmg, x{} crit multiplier)"
              .format(player.armor.name, int((1 - player.armor.protection) * 100), player.armor.poison_resist,
                player.armor.debuff_resist,
                player.weapon.name, player.weapon.bonus_dmg, player.weapon.crit_mult))

    def town():
        if Game.dungeon_loop is False:
            town_loop = True
            while town_loop is True:
                player_input = input("Welcome to the small village of Seronia!\nWhere will you go?\n1: Armor Shop\n"
                                     "2: Weapon Shop\n3: Potion Shop\n4: Tavern\ne: Dungeon\nw: Inspect Gear\nq: Quit\n> ")
                line()
                if player_input == "1":
                    armor_shop()
                elif player_input == "2":
                    weapon_shop()
                elif player_input == "3":
                    potion_shop()
                elif player_input == "4":
                    tavern()
                elif player_input.lower() == "e":
                    town_loop = False
                    Game.dungeon_loop = True
                    dungeon()
                elif player_input.lower() == "w":
                    inspect_gear()
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
                elif player_input.lower() == "y":
                    Game.dungeon_loop = False
                    Game.restart_boolean = True
                    Game.game_over = False
                    Game.restart_once = 1
                else:
                    invalid_option()

    def quit_func():
        if player.hp > 0:
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
        if Game.restart_boolean is True or False:
            break
        town()
    if Game.restart_boolean is False or Game.quit_boolean is True:
        break

"""Ideas
-monsters drop treasure that you can sell in town
-after a certain amount of defeated enemies, player is able to choose a different path
-passive money making building to purchase in town
-merchant who can upgrade your max hp and ap
-Rob the shop but can't use shops for a certain period of time
-Add a tavern where you can gamble
-Sleep for free but less effective
-buy a house
-add save feature
"""