import random
import math

import functions
from classes import player_class, team_class, save_class, match_class


def blank_save(serverID):
    # before I knew how stuff worked, but it works I guess
    save = save_class(serverID, 0, 0, 0, 0, 0, 0, 0, 0, [], "", [], [], 0, [], [], [])
    return save


def name_gen():
    first_name_file = open("first_name_bank.txt", "r")  # opens the first name file
    last_name_file = open("last_name_bank.txt", "r")  # opens the last name file
    general_name_file = open("general_name_bank.txt", "r")  # opens the general name file

    first_name_read = first_name_file.read()  # read all of the list
    first_name_split = first_name_read.split("\n")  # cut out all of the newlines
    first_name_amount = len(first_name_split) - 1

    last_name_read = last_name_file.read()  # read all of the list
    last_name_split = last_name_read.split("\n")  # cut out all of the newlines
    last_name_amount = len(last_name_split) - 1

    general_name_read = general_name_file.read()  # read all of the list
    general_name_split = general_name_read.split("\n")  # cut out all of the newlines
    general_name_amount = len(general_name_split) - 1

    first_name_number = first_name_amount * random.random()  # pick first name
    first_name_number = math.floor(first_name_number)
    first_name = first_name_split[first_name_number]

    last_name_number = last_name_amount * random.random()  # pick last name
    last_name_number = math.floor(last_name_number)
    last_name = last_name_split[last_name_number]

    general_name_number = general_name_amount * random.random()  # pick general name
    general_name_number = math.floor(general_name_number)
    general_name = general_name_split[general_name_number]

    choice_int = math.ceil(3 * random.random())

    if choice_int == 1:
        first_name_file.close()
        last_name_file.close()
        general_name_file.close()
        return first_name + " " + last_name
    elif choice_int == 2:
        first_name_file.close()
        last_name_file.close()
        general_name_file.close()
        return general_name + " " + last_name
    elif choice_int == 3:
        first_name_file.close()
        last_name_file.close()
        general_name_file.close()
        return first_name + " " + general_name


def stat_gen():
    stat = random.randint(0, 5)
    return stat


def player_gen(position):
    # get the list of genders
    gender_list_file = open("gender_list.txt", "r")
    gender_list_read = gender_list_file.read()  # read all of the list
    gender_list = gender_list_read.split("\n")  # cut out all of the newlines
    gender_list_file.close()

    # create a blank player
    new_player = player_class("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [])

    new_player.name = name_gen()
    new_player.position = position
    new_player.whirling = stat_gen()
    new_player.curvitude = stat_gen()
    new_player.sunfloweryness = stat_gen()
    new_player.relativity = stat_gen()
    new_player.electrification = stat_gen()
    new_player.unviscosity = stat_gen()
    new_player.springyness = stat_gen()
    new_player.anti_gravitude = stat_gen()
    new_player.omnipresence = stat_gen()
    new_player.bean_saturation = stat_gen()
    new_player.torquiness = stat_gen()
    new_player.calcium_density = stat_gen()
    new_player.zodiac = random.randint(0, len(gender_list) - 1)
    new_player.gender = random.randint(0, len(gender_list) - 1)
    new_player.special = 7
    new_player.life = 1
    new_player.effects.append(0)

    return new_player


def team_gen(team_name, team_bucket):
    # get the team index
    team_index = len(team_bucket)

    # create a blank team object
    new_team = team_class("", 0, 0, 0, 0, 0, [], [], 0)

    # get team name
    new_team.name = team_name

    # the wins, losses, championshps, and pitcher index are already 0. so the players can be generated

    # generate batters
    for i in range(9):
        new_team.batters.append(player_gen(1))

    # generate pitchers
    for i in range(5):
        new_team.pitchers.append(player_gen(2))

    return new_team


def round_robin(team_amount):
    if (team_amount % 2) == 0:
        index_list = []
        for i in range(team_amount):
            index_list.append(i)

        # init the schedule list
        schedule = []
        # x is a relevant variable for stopping the scheduler
        x = int((team_amount - 2) / 2)
        for i in range(len(index_list) - 1):
            # make the first one
            schedule.append(match_class(index_list[0], index_list[1]))
            # make the rest of them
            for j in range(x):
                # round robin majic
                schedule.append((match_class(index_list[j + 2], index_list[team_amount - 1 - j])))

            # rotate the polygon
            for j in range(team_amount):
                if j != 0:
                    index_list[j] = index_list[j] - 1
                    if index_list[j] == 0:
                        index_list[j] = team_amount - 1

        return schedule
    # in the case of odd numbered brackets
    else:
        index_list = []
        for i in range(team_amount):
            index_list.append(i)

        # init the schedule list
        schedule = []
        x = int((team_amount - 1) / 2)
        # this loop is for each rotation
        for i in range(len(index_list)):
            # this loop is to assign the things
            for j in range(x):
                schedule.append(match_class(index_list[j], index_list[team_amount - 2 - j]))

            # rotate the polygon
            for j in range(team_amount):
                index_list[j] = index_list[j] - 1
                if index_list[j] < 0:
                    index_list[j] = team_amount - 1
        return schedule


def dice_roll(stat):
    roll = random.randint(1, 20) + stat
    return roll


def out_play_text(outs):
    if outs == 1:
        return "Single Play"
    elif outs == 2:
        return "Double Play!"
    elif outs == 3:
        return "Triple Play!!!"
    elif outs == 4:
        return "*QUADRUPLE PLAY*"


def game_iteration(game):
    # start by figuring out which team is offense and which is defence
    bat_team = 0
    pit_team = 0
    if game.half == 1:
        bat_team = game.team1
        game.current_batter = game.team1_batter
        pit_team = game.team2
    elif game.half == 2:
        bat_team = game.team2
        game.current_batter = game.team2_batter
        pit_team = game.team1

    # big roll. Rolls all batting and pitching stats
    batter_roll = dice_roll(
        bat_team.batters[game.current_batter].bean_saturation + bat_team.batters[game.current_batter].torquiness +
        bat_team.batters[game.current_batter].calcium_density)
    pitcher_roll = dice_roll(
        pit_team.pitchers[pit_team.pitcher_index].whirling + pit_team.pitchers[pit_team.pitcher_index].curvitude +
        pit_team.pitchers[pit_team.pitcher_index].sunfloweryness)

    # if pitcher wins
    if pitcher_roll > batter_roll:
        # secondary roll. this determines if it is a strike or foul. calcium density vs sunfloweryness
        batter_roll = dice_roll(bat_team.batters[game.current_batter].calcium_density)
        pitcher_roll = dice_roll(pit_team.pitchers[pit_team.pitcher_index].sunfloweryness)

        # if pitcher wins again, strike
        if pitcher_roll > batter_roll:
            game.add_strike()
            game.message_list.append("Strike " + str(game.strikes) + "!")

            # if there are more than 2 strikes, add an out
            if game.strikes > 2:
                game.add_out()
                game.message_list.append(bat_team.batters[game.current_batter].name + " strikes out!")

                # if there are more than 2 outs, signal a half change
                if game.outs > 2:
                    game.half_change = 1
                else:
                    # if bases are loaded, send a special message
                    if (game.first != -1) and (game.second != -1) and (game.third != -1):
                        game.message_list.append("There's a charge in the air...")
                # get a new batter if there are more than 2 strikes
                game.new_batter()

        # if the batter wins the secondary, foul
        elif batter_roll > pitcher_roll:
            # only add a strike if there are less than 2 strikes
            if game.strikes < 2:
                game.add_strike()
            # because foul messages are strange, I need several of them. It chooses from one of them at random
            foulnum = random.randint(0, 4)
            if foulnum == 0:
                game.message_list.append("Foul!")
            elif foulnum == 1:
                game.message_list.append("Foul Ball!")
            elif foulnum == 2:
                game.message_list.append("Fooouuulllll!")
            elif foulnum == 3:
                game.message_list.append("Hit!... no it's a foul")
            elif foulnum == 4:
                game.message_list.append("The ball has been Fouled")

    # if batter wins
    elif batter_roll > pitcher_roll:
        # secondary roll. determines hit or ball. torquiness and curvitude
        batter_roll = dice_roll(bat_team.batters[game.current_batter].torquiness)
        pitcher_roll = dice_roll(pit_team.pitchers[pit_team.pitcher_index].curvitude)

        # if pitcher wins the secondary, ball
        if pitcher_roll > batter_roll:
            game.add_ball()
            game.message_list.append("Ball!")
            # if 4 balls, walk
            if game.balls > 3:
                game.walk()
                # if bases are loaded, display a special message
                if (game.first != -1) and (game.second != -1) and (game.third != -1):
                    game.message_list.append("There's a charge in the air...")

        # if batter wins again, hit
        elif batter_roll > pitcher_roll:
            # the batter has already won, so determine how hard the ball (blall?) is hit
            game.message_list.append("Hit!")
            # roll bean saturation
            power_roll = dice_roll(bat_team.batters[game.current_batter].bean_saturation)
            # some weird dice calculations don't worry about it.
            dice_size = 20
            grand_slam_signal = 0
            if power_roll < (dice_size / 2):
                max_bases = 1
            elif ((dice_size / 2) + (dice_size / 3)) > power_roll >= (dice_size / 2):
                max_bases = 2
            elif dice_size >= power_roll >= ((dice_size / 2) + (dice_size / 3)):
                max_bases = 3
            elif power_roll > dice_size:
                max_bases = 4
                # if a home run is hit with bases loaded
                if game.first != -1 and game.second != -1 and game.third != -1:
                    grand_slam_signal = 1
            new_outs = 0

            # determining base outs, assuming there is no grand slam
            if grand_slam_signal != 1:
                # since fielding is a team effort, the average values of some stuff is calculated
                average_springyness = game.get_average_springyness()
                average_omnipresence = game.get_average_omnipresence()

                # the base outs are calculated from third back for simplicity’s sake

                # start at third base
                if game.third != -1:
                    # for third, roll average omnipresence against batter's unviscosity
                    field_roll = dice_roll(average_omnipresence)
                    run_roll = dice_roll(bat_team.batters[game.third].unviscosity)
                    # if the field wins, then get out
                    if field_roll > run_roll:
                        # add an out
                        new_outs = new_outs + 1
                        # add the appropriate out messages
                        game.message_list.append(out_play_text(new_outs))
                        game.message_list.append(bat_team.batters[game.third].name + " gets caught out!")
                        game.add_out()
                        game.third = -1
                        if game.outs > 2:
                            game.half_change = 1
                    # if they don't get caught out, always score
                    else:
                        game.message_list.append(bat_team.batters[game.third].name + " scores!")
                        game.score()
                        game.third = -1


                # next is second
                if game.second != -1:
                    field_roll = dice_roll(average_omnipresence)
                    run_roll = dice_roll(bat_team.batters[game.second].unviscosity)
                    if field_roll > run_roll:
                        new_outs = new_outs + 1
                        game.message_list.append(out_play_text(new_outs))
                        game.message_list.append(bat_team.batters[game.second].name + " gets caught out!")
                        game.add_out()
                        game.second = -1
                        if game.outs > 2:
                            game.half_change = 1
                    # if they don't get caught out, then move 1 or 2 bases
                    else:
                        if game.half_change == 0:
                            if max_bases == 1:
                                game.third = game.second
                                game.second = -1
                            elif max_bases > 1:
                                game.message_list.append(bat_team.batters[game.second].name + " scores!")
                                game.score()
                                game.second = -1

                # next is first
                if game.first != -1:
                    field_roll = dice_roll(average_omnipresence)
                    run_roll = dice_roll(bat_team.batters[game.first].unviscosity)
                    if field_roll > run_roll:
                        new_outs = new_outs + 1
                        game.message_list.append(out_play_text(new_outs))
                        game.message_list.append(bat_team.batters[game.first].name + " gets caught out!")
                        game.add_out()
                        game.first = -1
                        if game.outs > 2:
                            game.half_change = 1
                    # if they don't get caught out, move 1, 2, or 3 bases
                    else:
                        if game.half_change == 0:
                            if max_bases == 1:
                                game.second = game.first
                                game.first = -1
                            elif max_bases == 2:
                                game.third = game.first
                                game.first = -1
                            elif max_bases > 2:
                                game.message_list.append(bat_team.batters[game.first].name + " scores!")
                                game.score()
                                game.first = -1

                # and lastly the batter
                field_roll = dice_roll(average_springyness)
                run_roll = dice_roll(bat_team.batters[game.current_batter].unviscosity)
                if field_roll > run_roll:
                    new_outs = new_outs + 1
                    game.message_list.append(out_play_text(new_outs))
                    game.message_list.append(bat_team.batters[game.current_batter].name + " gets caught out!")
                    game.add_out()
                else:
                    if game.half_change == 0:
                        if max_bases == 1:
                            game.first = game.current_batter
                            game.message_list.append(bat_team.batters[game.current_batter].name + " makes it to first")
                        elif max_bases == 2:
                            game.second = game.current_batter
                            game.message_list.append(bat_team.batters[game.current_batter].name + " makes it to second")
                        elif max_bases == 3:
                            game.third = game.current_batter
                            game.message_list.append(bat_team.batters[game.current_batter].name + " makes it to third")
                        elif max_bases > 3:
                            game.score()
                            game.message_list.append("HOME RUN")
                            game.message_list.append(bat_team.batters[game.current_batter].name + " scores!")
                if game.outs > 2:
                    game.half_change = 1
                game.new_batter()
                if (game.first != -1) and (game.second != -1) and (game.third != -1):
                    game.message_list.append("There's a charge in the air...")
            else:
                game.message_list.append(bat_team.batters[game.current_batter].name + " HITS A GRAND SLAM")
                game.message_list.append(game.get_random_fielder_name() + " tries to catch the ball")
                game.message_list.append("but the ball doesn't want to!")
                game.score()
                game.score()
                game.score()
                game.score()
                game.message_list.append(bat_team.batters[game.third].name + " scores!")
                game.message_list.append(bat_team.batters[game.second].name + " scores!")
                game.message_list.append(bat_team.batters[game.first].name + " scores!")
                game.message_list.append(bat_team.batters[game.current_batter].name + " scores!")
                game.third = -1
                game.second = -1
                game.first = -1
                game.new_batter()

    # if the batter and pitcher tie
    elif batter_roll == pitcher_roll:
        # determining what things happen
        # this tracks if something has happened, because it will likely re-roll a lot of times
        event_occured = 0
        while event_occured == 0:
            event_roll = random.randint(1,100)
            if 1 <= event_roll <= 50:
                # stealing
                # check if there are players with bases in front of them (can they steal)

                # start with third
                if game.third != -1:
                    # see if they want to steal. must be above a 9. stat is electrification
                    if functions.dice_roll(bat_team.batters[game.third].electrification)>9:
                        event_occured = 1
                        # if they decide to steal
                        game.message_list.append(bat_team.batters[game.third].name + " tries to steal to home!")
                        # relativity vs whirling
                        steal_role = functions.dice_roll(bat_team.batters[game.third].relativity)
                        unsteal_role = functions.dice_roll(pit_team.pitchers[pit_team.pitcher_index].whirling)

                        # if pitcher wins
                        if unsteal_role > steal_role:
                            game.message_list.append(bat_team.batters[game.third].name + " gets caught out!")
                            game.third = -1
                            game.add_out()
                        else:
                            game.message_list.append(bat_team.batters[game.third].name + " scores!")
                            game.score()
                            game.third = -1

                # if someone is on second and third is open
                elif game.second != -1 and game.third == -1:
                    # see if they want to steal
                    if functions.dice_roll(bat_team.batters[game.second].electrification)>9:
                        event_occured = 1
                        # if they decide to steal
                        game.message_list.append(bat_team.batters[game.second].name + " tries to steal to third!")
                        steal_role = functions.dice_roll(bat_team.batters[game.second].relativity)
                        unsteal_role = functions.dice_roll(pit_team.pitchers[pit_team.pitcher_index].whirling)
                        # if pitcher wins
                        if unsteal_role > steal_role:
                            game.message_list.append(bat_team.batters[game.second].name + " gets caught out!")
                            game.second = -1
                            game.add_out()
                        else:
                            game.message_list.append(bat_team.batters[game.second].name + " makes it!")
                            game.third = game.second
                            game.second = -1

                # if someone is on first and second is open
                elif game.first != -1 and game.second == -1:
                    # see if they want to steal
                    if functions.dice_roll(bat_team.batters[game.first].electrification)>9:
                        event_occured = 1
                        # if they decide to steal
                        game.message_list.append(bat_team.batters[game.first].name + " tries to steal to second!")
                        steal_role = functions.dice_roll(bat_team.batters[game.first].relativity)
                        unsteal_role = functions.dice_roll(pit_team.pitchers[pit_team.pitcher_index].whirling)
                        # if pitcher wins
                        if unsteal_role > steal_role:
                            game.message_list.append(bat_team.batters[game.first].name + " gets caught out!")
                            game.first = -1
                            game.add_out()
                        else:
                            game.message_list.append(bat_team.batters[game.first].name + " makes it!")
                            game.second = game.first
                            game.first = -1

            elif 51 <= event_roll <= 65:
                # stat changes
                event_occured = 1
                # pick that stat to change
                stat = random.randint(1, 12)
                amount = random.randint(-2, 2)
                if amount == 0:
                    amount = 1

                # pick a team
                team_pick = random.randint(0, 1)
                # pick a player
                if team_pick == 0:
                    player_index = random.randint(0, len(bat_team.batters) + len(bat_team.pitchers) - 1)
                    position_select = 0  # defaults to batter
                    if player_index > len(bat_team.batters) - 1:  # if a pitcher was selected
                        player_index = player_index - len(bat_team.batters)
                        position_select = 1
                else:
                    player_index = random.randint(0, len(pit_team.batters) + len(pit_team.pitchers) - 1)
                    position_select = 0  # defaults to batter
                    if player_index > len(pit_team.batters) - 1:  # if a pitcher was selected
                        player_index = player_index - len(pit_team.batters)
                        position_select = 1

                if stat == 1:  # whirling
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " Throws a whirligig!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It whirls into " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].whirling = bat_team.batters[player_index].whirling + amount
                        else:
                            game.message_list.append("It whirls into " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].whirling = bat_team.pitchers[player_index].whirling + amount
                    else:
                        if position_select == 0: # picks pitching team
                            game.message_list.append("It whirls into " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].whirling = pit_team.batters[player_index].whirling + amount
                        else:
                            game.message_list.append("It whirls into " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].whirling = pit_team.pitchers[player_index].whirling + amount
                elif stat == 2:  # curvitude
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " Throws a banana!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It curves into " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].curvitude = bat_team.batters[player_index].curvitude + amount
                        else:
                            game.message_list.append("It curves into " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].curvitude = bat_team.pitchers[player_index].curvitude + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("It curves into " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].curvitude = pit_team.batters[player_index].curvitude + amount
                        else:
                            game.message_list.append("It curves into " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].curvitude = pit_team.pitchers[player_index].curvitude + amount
                elif stat == 3:  # sunfloweryness
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " Throws a bag of sunflower seeds!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("The seeds shine at " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].sunfloweryness = bat_team.batters[player_index].sunfloweryness + amount
                        else:
                            game.message_list.append("The seeds shine at " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].sunfloweryness = bat_team.pitchers[player_index].sunfloweryness + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("The seeds shine at " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].sunfloweryness = pit_team.batters[player_index].sunfloweryness + amount
                        else:
                            game.message_list.append("The seeds shine at " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].sunfloweryness = pit_team.pitchers[player_index].sunfloweryness + amount
                elif stat == 4:  # relativity
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws an einsteinium ball!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It folds spacetime and hits " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].relativity = bat_team.batters[player_index].relativity + amount
                        else:
                            game.message_list.append("It folds spacetime and hits " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].relativity = bat_team.pitchers[player_index].relativity + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("It folds spacetime and hits " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].relativity = pit_team.batters[player_index].relativity + amount
                        else:
                            game.message_list.append("It folds spacetime and hits " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].relativity = pit_team.pitchers[player_index].relativity + amount
                elif stat == 5:  # electrification
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws an electricity ball!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It arcs into " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].electrification = bat_team.batters[player_index].electrification + amount
                        else:
                            game.message_list.append("It arcs into " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].electrification = bat_team.pitchers[player_index].electrification + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("It arcs into " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].electrification = pit_team.batters[player_index].electrification + amount
                        else:
                            game.message_list.append("It arcs into " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].electrification = pit_team.pitchers[player_index].electrification + amount
                elif stat == 6:  # unviscosity
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws some oobleck!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It splats(?) on " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].unviscosity = bat_team.batters[player_index].unviscosity + amount
                        else:
                            game.message_list.append("It splats(?) on " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].unviscosity = bat_team.pitchers[player_index].unviscosity + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("It splats(?) on " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].unviscosity = pit_team.batters[player_index].unviscosity + amount
                        else:
                            game.message_list.append("It splats(?) on " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].unviscosity = pit_team.pitchers[player_index].unviscosity + amount
                elif stat == 7:  # springyness
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws a spring loaded ball!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It bounces and hits " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].springyness = bat_team.batters[player_index].springyness + amount
                        else:
                            game.message_list.append("It bounces and hits " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].springyness = bat_team.pitchers[player_index].springyness + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("It bounces and hits " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].springyness = pit_team.batters[player_index].springyness + amount
                        else:
                            game.message_list.append("It bounces and hits " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].springyness = pit_team.pitchers[player_index].springyness + amount
                elif stat == 8:  # anti_gravitude
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws a gravity ball!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("The ball gravities to and hits " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].anti_gravitude = bat_team.batters[player_index].anti_gravitude + amount
                        else:
                            game.message_list.append("The ball gravities to and hits " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].anti_gravitude = bat_team.pitchers[player_index].anti_gravitude + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("The ball gravities to and hits " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].anti_gravitude = pit_team.batters[player_index].anti_gravitude + amount
                        else:
                            game.message_list.append("The ball gravities to and hits " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].anti_gravitude = pit_team.pitchers[player_index].anti_gravitude + amount
                elif stat == 9:  # omnipresence
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws an all seeing eye!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("The eye stares down " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].omnipresence = bat_team.batters[player_index].omnipresence + amount
                        else:
                            game.message_list.append("The eye stares down " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].omnipresence = bat_team.pitchers[player_index].omnipresence + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("The eye stares down " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].omnipresence = pit_team.batters[player_index].omnipresence + amount
                        else:
                            game.message_list.append("The eye stares down " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].omnipresence = pit_team.pitchers[player_index].omnipresence + amount
                elif stat == 10:  # bean_saturation
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws a loaded bean ball-rito!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("The beans mostly fall on " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].bean_saturation = bat_team.batters[player_index].bean_saturation + amount
                        else:
                            game.message_list.append("The beans mostly fall on " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].bean_saturation = bat_team.pitchers[player_index].bean_saturation + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("The beans mostly fall on " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].bean_saturation = pit_team.batters[player_index].bean_saturation + amount
                        else:
                            game.message_list.append("The beans mostly fall on " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].bean_saturation = pit_team.pitchers[player_index].bean_saturation + amount
                elif stat == 11:  # torquiness
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " launches a blayblade!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("It spins into " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].torquiness = bat_team.batters[player_index].torquiness + amount
                        else:
                            game.message_list.append("It spins into " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].torquiness = bat_team.pitchers[player_index].torquiness + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("It spins into " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].torquiness = pit_team.batters[player_index].torquiness + amount
                        else:
                            game.message_list.append("It spins into " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].torquiness = pit_team.pitchers[player_index].torquiness + amount
                elif stat == 12:  # calcium_density
                    game.message_list.append(pit_team.pitchers[pit_team.pitcher_index].name + " throws a milk carton!")
                    if team_pick == 0: #picks batting team
                        if position_select == 0: # picks a batter
                            game.message_list.append("The milk mostly splashes on " + bat_team.batters[player_index].name + "!")
                            bat_team.batters[player_index].calcium_density = bat_team.batters[player_index].calcium_density + amount
                        else:
                            game.message_list.append("The milk mostly splashes on " + bat_team.pitchers[player_index].name + "!")
                            bat_team.pitchers[player_index].calcium_density = bat_team.pitchers[player_index].calcium_density + amount
                    else:
                        if position_select == 0:  # picks pitching team
                            game.message_list.append("The milk mostly splashes on " + pit_team.batters[player_index].name + "!")
                            pit_team.batters[player_index].calcium_density = pit_team.batters[player_index].calcium_density + amount
                        else:
                            game.message_list.append("The milk mostly splashes on " + pit_team.pitchers[player_index].name + "!")
                            pit_team.pitchers[player_index].calcium_density = pit_team.pitchers[player_index].calcium_density + amount

            # player deaths get more after each increase in heat
            elif 66 <= event_roll <= (66 + (10 * game.heat)):
                # player deaths
                if game.heat != 0:
                    event_occured = 1
                    # pick a team
                    team_pick = random.randint(0, 1)
                    # pick a player
                    if team_pick == 0:
                        player_index = random.randint(0, len(bat_team.batters) + len(bat_team.pitchers) - 1)
                        position_select = 0  # defaults to batter
                        if player_index > len(bat_team.batters) - 1:  # if a pitcher was selected
                            player_index = player_index - len(bat_team.batters)
                            position_select = 1
                    else:
                        player_index = random.randint(0, len(pit_team.batters) + len(pit_team.pitchers) - 1)
                        position_select = 0  # defaults to batter
                        if player_index > len(pit_team.batters) - 1:  # if a pitcher was selected
                            player_index = player_index - len(pit_team.batters)
                            position_select = 1

                    # riv
                    game.message_list.append("'I SAID HURRY UP'")
                    if team_pick == 0:
                        game.message_list.append("The heat gathers around the " + bat_team.name)
                        if position_select == 0: # batters
                            game.message_list.append(bat_team.batters[player_index].name + " catches on fire!")
                            game.message_list.append("Rest in Violence")
                            bat_team.batters[player_index] = player_gen(1)
                            game.message_list.append(bat_team.batters[player_index].name + " steps in to help!")
                            if player_index == game.third:
                                game.third = -1
                            elif player_index == game.second:
                                game.second = -1
                            elif player_index == game.first:
                                game.first = -1
                            elif player_index == game.current_batter:
                                game.new_batter()
                        else:
                            game.message_list.append(bat_team.pitchers[player_index].name + " catches on fire!")
                            game.message_list.append("Rest in Violence")
                            bat_team.pitchers[player_index] = player_gen(2)
                            game.message_list.append(bat_team.pitchers[player_index].name + " steps in to help!")
                    else:
                        game.message_list.append("The heat gathers around the " + pit_team.name)
                        if position_select == 0:  # batters
                            game.message_list.append(pit_team.batters[player_index].name + " catches on fire!")
                            game.message_list.append("Rest in Violence")
                            pit_team.batters[player_index] = player_gen(1)
                            game.message_list.append(pit_team.batters[player_index].name + " steps in to help!")
                        else:
                            game.message_list.append(pit_team.pitchers[player_index].name + " catches on fire!")
                            game.message_list.append("Rest in Violence")
                            pit_team.pitchers[player_index] = player_gen(2)
                            game.message_list.append(pit_team.pitchers[player_index].name + " steps in to help!")




    if game.half == 1:
        game.team1 = bat_team
        game.team1_batter = game.current_batter
        game.team2 = pit_team
    elif game.half == 2:
        game.team2 = bat_team
        game.team2_batter = game.current_batter
        game.team1 = pit_team
    return game
