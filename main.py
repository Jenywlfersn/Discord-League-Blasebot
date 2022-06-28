import math
import discord
import asyncio
import classes
import time
import os

import functions

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="BLA help"))
    print("Bot is Ready")


@client.event
async def on_guild_join(guild):
    # when the bot joins a server, it creates a save file
    saveInfo = functions.blank_save(guild.id)
    saveInfo.save()


@client.event
async def on_message(message):
    # this first thing is the starting of the game
    # if the bot detects that it sent the start message, then it will run a game
    if message.author == client.user:
        if message.content == "Starting Next Game...":
            #get the guild
            guild = message.guild
            # create a blank save
            saveInfo = functions.blank_save(guild.id)
            # fill the blank save
            saveInfo = saveInfo.load()
            # create the game object
            game = classes.game_class(saveInfo.team_bucket[saveInfo.league_schedule[saveInfo.schedule_position].team1],
                                      saveInfo.team_bucket[saveInfo.league_schedule[saveInfo.schedule_position].team2])

            # find the game channel using saved id (will likely have to make a case if it can't be found)
            game_channel = guild.get_channel(saveInfo.game_channel_id)
            # create a recap file
            # this also serves to blank out an existing file, should it have previously broken
            message_file = open(str(guild.id) + "game" + str(saveInfo.schedule_position) + ".txt", "w")
            message_file.write("")
            message_file.close()

            # this time open recap file in append mode
            message_file = open(str(guild.id) + "game" + str(saveInfo.schedule_position) + ".txt", "a")

            # send the first message
            await game_channel.send(game.team1.name + " vs " + game.team2.name)
            message_file.write(game.team1.name + " vs " + game.team2.name + "\n")
            await asyncio.sleep(saveInfo.time_delay + 1)

            # initialize the readout
            message_text = game.display_text()
            readout_message = await game_channel.send(message_text)
            message_text = message_text.replace("```", "")
            message_file.write(message_text + "\n")

            # initialize the ticker
            ticker_message = await game_channel.send(
                "`" + game.team2.pitchers[game.team2.pitcher_index].name + " pitching for the " + game.team2.name + "`")
            message_file.write(
                game.team2.pitchers[game.team2.pitcher_index].name + " pitching for the " + game.team2.name + "\n")
            # delay for the amount of time
            await asyncio.sleep(saveInfo.time_delay)

            # message before the game actually starts
            await ticker_message.edit(
                content="`" + game.team1.batters[0].name + " batting for the " + game.team1.name + "`")
            message_file.write(game.team1.batters[0].name + " batting for the " + game.team1.name)
            await asyncio.sleep(saveInfo.time_delay)
            await ticker_message.edit(content="Play Blall!")

            # loop this until the game object says to stop
            while game.end_signal == 0:
                # game iteration
                game = functions.game_iteration(game)

                # take all of the game messages and display them
                message_file.write("\n----------\n")
                for i in range(len(game.message_list)):
                    await asyncio.sleep(saveInfo.time_delay)
                    await ticker_message.edit(content="`" + game.message_list[i] + "`")
                    message_file.write(game.message_list[i] + "\n")
                message_file.write("\n----------\n")
                # clear the message list
                game.message_list = []
                # if the half changes, then display the new readout, otherwise print the readout like normal
                if game.half_change == 1:
                    # send the modified display message with no batter
                    message_text = game.display_text()
                    await readout_message.edit(content=message_text)
                    message_text = message_text.replace("```", "")
                    message_file.write(message_text + "\n")
                    await asyncio.sleep(saveInfo.time_delay)
                    # then change the halves
                    game.change_halves()

                    # if the game needs to go into overtime
                    if (game.inning > 9) and (game.half == 1):
                        if game.team_1_score == game.team_2_score:
                            # display spooke messages
                            await ticker_message.edit(content="`'Tie game?'`")
                            message_file.write("'Tie game?'" + "\n")
                            await asyncio.sleep(saveInfo.time_delay)
                            await ticker_message.edit(content="`'Unacceptable'`")
                            message_file.write("'Unacceptable'" + "\n")
                            await asyncio.sleep(saveInfo.time_delay)
                            await ticker_message.edit(content="`'Turning up the heat'`")
                            message_file.write("'Turning up the heat'" + "\n")
                            await asyncio.sleep(saveInfo.time_delay)
                            # display the batter up message
                            if game.half == 1:
                                await ticker_message.edit(
                                    content="`" + game.team1.batters[
                                        game.current_batter].name + " steps up to the plate`")
                                message_file.write(
                                    game.team1.batters[game.current_batter].name + " steps up to the plate\n")
                            else:
                                await ticker_message.edit(
                                    content="`" + game.team2.batters[
                                        game.current_batter].name + " steps up to the plate`")
                                message_file.write(
                                    game.team2.batters[game.current_batter].name + " steps up to the plate\n")
                            # turn up the heat so that players can be killed
                            game.heat = game.heat + 1
                            await asyncio.sleep(saveInfo.time_delay)
                        else:
                            # if the game does not need to go into overtime then give a win and a loss and finish the game
                            if game.team_1_score > game.team_2_score:
                                await ticker_message.edit(content="`The " + game.team1.name + " win!`")
                                message_file.write("The " + game.team1.name + " win!" + "\n----------\n")
                                # give win and loss
                                saveInfo.team_bucket[saveInfo.league_schedule[saveInfo.schedule_position].team1].wins = \
                                    saveInfo.team_bucket[
                                        saveInfo.league_schedule[saveInfo.schedule_position].team1].wins + 1
                                saveInfo.team_bucket[
                                    saveInfo.league_schedule[saveInfo.schedule_position].team2].losses = \
                                    saveInfo.team_bucket[
                                        saveInfo.league_schedule[saveInfo.schedule_position].team2].losses + 1
                            else:
                                await ticker_message.edit(content="`The " + game.team2.name + " win!`")
                                message_file.write("The " + game.team2.name + " win!" + "\n----------\n")
                                # give win and loss
                                saveInfo.team_bucket[saveInfo.league_schedule[saveInfo.schedule_position].team2].wins = \
                                    saveInfo.team_bucket[
                                        saveInfo.league_schedule[saveInfo.schedule_position].team2].wins + 1
                                saveInfo.team_bucket[
                                    saveInfo.league_schedule[saveInfo.schedule_position].team1].losses = \
                                    saveInfo.team_bucket[
                                        saveInfo.league_schedule[saveInfo.schedule_position].team1].losses + 1
                            # init a final readout message
                            message_text = "```"
                            # init the spaces
                            spaces = ""
                            # gather enough spaces to put the score halfway in the name
                            for i in range(int((len(game.team1.name)) / 2) - 1):
                                spaces = spaces + " "
                            # message format with 4 spaces after for " vs "
                            message_text = message_text + spaces + str(game.team_1_score) + spaces + "    "
                            spaces = ""
                            # gather enough spaces for the same reason as before
                            for i in range(int((len(game.team2.name)) / 2)):
                                spaces = spaces + " "
                            # first line done
                            message_text = message_text + spaces + str(game.team_2_score) + "\n"

                            # second line
                            message_text = message_text + game.team1.name + " vs " + game.team2.name + "```"
                            await readout_message.edit(content=message_text)
                            message_text = message_text.replace("```", "")
                            message_file.write(message_text + "\n----------\n")

                            # end the actual game
                            game.end_signal = 1

                            # close the message file
                            message_file.close()
                            # format the message file so that discord can send it
                            sending_File = discord.File(
                                str(guild.id) + "game" + str(saveInfo.schedule_position) + ".txt")
                            # change the name of the formatted file
                            sending_File.filename = saveInfo.league_name + " game " + str(
                                saveInfo.schedule_position) + ".txt"
                            # send the text file
                            await game_channel.send("Game Recap!", file=sending_File)
                            # delete the message from my hardrive
                            os.remove(str(guild.id) + "game" + str(saveInfo.schedule_position) + ".txt")
                            # advance pitchers
                            # team 1 pitcher
                            if game.team1.pitcher_index == len(game.team1.pitchers)-1:
                                game.team1.pitcher_index = 0
                            else:
                                game.team1.pitcher_index = game.team1.pitcher_index + 1
                            # team 2 pitcher
                            if game.team2.pitcher_index == len(game.team2.pitchers)-1:
                                game.team2.pitcher_index = 0
                            else:
                                game.team2.pitcher_index = game.team2.pitcher_index + 1
                            # save for good measure
                            saveInfo.save()
                            # this reaction will trigger the countdown and game advancement
                            await ticker_message.add_reaction("\u2705")
                    else:
                        # if the half changes
                        # send the changing half message
                        await ticker_message.edit(content="`Changing Halves`")
                        message_file.write("\n----------\n" + "Changing Halves\n")
                        await asyncio.sleep(saveInfo.time_delay)
                        # display the thing
                        message_text = game.display_text()
                        await readout_message.edit(content=message_text)
                        message_text = message_text.replace("```", "")
                        message_file.write(message_text + "\n")
                        # display the batter up message
                        if game.half == 1:
                            await ticker_message.edit(
                                content="`" + game.team1.batters[game.current_batter].name + " steps up to the plate`")
                            message_file.write(
                                game.team1.batters[game.current_batter].name + " steps up to the plate\n")
                        else:
                            await ticker_message.edit(
                                content="`" + game.team2.batters[game.current_batter].name + " steps up to the plate`")
                            message_file.write(
                                game.team2.batters[game.current_batter].name + " steps up to the plate\n")
                else:
                    # if nothing special happens, do a regular readout
                    message_text = game.display_text()
                    await readout_message.edit(content=message_text)
                    message_text = message_text.replace("```", "")
                    message_file.write(message_text + "\n")
            # ensure the teams are placed back correctly
            saveInfo.team_bucket[saveInfo.league_schedule[saveInfo.schedule_position].team1] = game.team1
            saveInfo.team_bucket[saveInfo.league_schedule[saveInfo.schedule_position].team2] = game.team2
            saveInfo.save()

    if message.author.bot == True:
        return

    # if the message meets the context for a command, then split it up and execute it
    if len(message.content)>2:
        if message.content[0] + message.content[1] + message.content[2] == "BLA":
            # take the message and split it by spaces
            message_list = message.content.split()

            # handy to have the guild as a variable
            guild = message.guild
            # create a blank save
            saveInfo = functions.blank_save(guild.id)
            # fill the blank save
            saveInfo = saveInfo.load()
            admin_permission = 0

            # determine admin permission
            if saveInfo.gen_state == 0:
                if message.author.guild_permissions.administrator == 1:
                    admin_permission = 1
            else:
                for i in range(len(message.author.roles)):
                    if (message.author.roles[
                            i].id == saveInfo.admin_role_id) or message.author.guild_permissions.administrator == 1:
                        admin_permission = 1

            # the command to change the league name
            # if the league has been generated
            if saveInfo.gen_state == 1:
                if message_list[1] == "league" and message_list[2] == "name":
                    if admin_permission == 1:
                        # get all of the words
                        LeagueName = ""
                        for i in range(len(message_list)):
                            if i > 2:
                                if i == len(message_list) - 1:
                                    LeagueName = LeagueName + message_list[i]
                                else:
                                    LeagueName = LeagueName + message_list[i] + " "
                        # send a confirmation
                        await message.channel.send(saveInfo.league_name + " is now " + LeagueName)
                        # make the change
                        saveInfo.league_name = LeagueName
                        # save
                        saveInfo.save()
                    else:
                        await message.channel.send("Permission required to use this command")

                # new submenu
                if message_list[1] == "new":
                    if admin_permission == 1:
                        # new team script
                        if message_list[2] == "team":
                            if saveInfo.league_active == 0:
                                # it takes a sec to make a team so do a please wait thing
                                confirmation_message = await message.channel.send("Please wait...")
                                # get the words for the team name
                                teamName = ""
                                # this block fills it in with correct formatting
                                for i in range(len(message_list)):
                                    if i > 2:
                                        if i == len(message_list) - 1:
                                            teamName = teamName + message_list[i]
                                        else:
                                            teamName = teamName + message_list[i] + " "
                                # generated and add a new team to the team bucket
                                saveInfo.team_bucket.append(functions.team_gen(teamName, saveInfo.team_bucket))
                                # create a new role
                                new_role = await guild.create_role(name=teamName)
                                saveInfo.team_bucket[len(saveInfo.team_bucket) - 1].roleID = new_role.id
                                # find category
                                cat_list = guild.categories
                                for i in range(len(cat_list)):
                                    if cat_list[i].id == saveInfo.category_id:
                                        j = i
                                # make new channel
                                new_channel = await guild.create_text_channel(name=teamName, category=guild.categories[j])
                                # save the channel's id
                                saveInfo.team_bucket[len(saveInfo.team_bucket) - 1].channelID = new_channel.id
                                # set all permissions
                                # the new role can send and read messages
                                await new_channel.set_permissions(target=new_role, read_messages=True, send_messages=True)
                                # @everyone cannot read
                                await new_channel.set_permissions(target=guild.default_role, read_messages=False)
                                # the bot can read and send
                                await new_channel.set_permissions(target=guild.self_role, read_messages=True,
                                                                  send_messages=True)
                                # general role cannot see
                                await new_channel.set_permissions(target=guild.get_role(saveInfo.general_role_id),
                                                                  read_messages=False)
                                # admin can see and read
                                await new_channel.set_permissions(target=guild.get_role(saveInfo.admin_role_id),
                                                                  read_messages=True,
                                                                  send_messages=True)

                                # create and send confirmation
                                returnMessage = teamName + " has been added"
                                await confirmation_message.edit(content=returnMessage)
                                # save the league info
                                saveInfo.save()
                            else:
                                await message.channel.send("The league is currently active")

                        if message_list[2] == "schedule":
                            if len(saveInfo.team_bucket) > 1:
                                # run the schedule generator and put it in the saveinfo
                                saveInfo.league_schedule = functions.round_robin(len(saveInfo.team_bucket))
                                # if there is no message saved
                                if saveInfo.schedule_message_id == 0:
                                    # send a new message using the league schedule formatter
                                    schedule_message = await guild.get_channel(saveInfo.schedule_channel_id).send(
                                        saveInfo.schedule_text())
                                    # save the ID for the schedule message
                                    saveInfo.schedule_message_id = schedule_message.id
                                    saveInfo.save()
                                    await message.channel.send("Schedule created")
                                # it there is a message saved
                                else:
                                    # if a message has already been sent
                                    # get the schedule channel
                                    schedule_channel = guild.get_channel(saveInfo.schedule_channel_id)
                                    # then get the message
                                    schedule_message = await schedule_channel.fetch_message(saveInfo.schedule_message_id)
                                    # update the schedule
                                    await schedule_message.edit(content=saveInfo.schedule_text())
                                    saveInfo.save()
                                    # send confirmation
                                    await message.channel.send("Schedule updated")
                            else:
                                await message.channel.send("There must be at least 2 teams to make a schedule")

                    else:
                        await message.channel.send("Permission required to use this command")

                # read out the team names as well as their indexes
                if message_list[1] == "teams":
                    # this is mostly formatting
                    returnMessage = "The " + saveInfo.league_name + " teams!\n"
                    if len(saveInfo.team_bucket) != 0:
                        # it displays one higher than the index to make it more convienient to look at
                        for i in range(len(saveInfo.team_bucket)):
                            returnMessage = returnMessage + str(i+1) + ": " + saveInfo.team_bucket[i].name + "\n"
                    else:
                        returnMessage = "There are no teams yet"
                    await message.channel.send(returnMessage)

                if message_list[1] == "join":
                    # if the user tries to join the league
                    check = 0
                    for i in range(len(message.author.roles)):
                        # if any of the member's roles are the general role, then do nothing
                        if message.author.roles[i].id == saveInfo.general_role_id:
                            check = 1
                    if check == 1:
                        await message.channel.send("You already have this role")
                    else:
                        # if they do not have the role, then give it to them using the saved role ID
                        await message.author.add_roles(
                            guild.get_role(saveInfo.general_role_id))
                        # send confirmation
                        await message.channel.send("Hope you enjoy yourself!")

                if message_list[1] == "leave":
                    # the inverse of join
                    check = 0
                    for i in range(len(message.author.roles)):
                        if message.author.roles[i].id == saveInfo.general_role_id:
                            check = 1
                    if check == 1:
                        await message.author.remove_roles(
                            guild.get_role(saveInfo.general_role_id))
                    else:
                        await message.channel.send("You already do not have this role")

                if message_list[1] == "delay":
                    # if an admin tries to change the delay between messages
                    if admin_permission == 1:
                        # the time can be no longer than 10 seconds and no less than 3
                        if 10 >= float(message_list[2]) >= 3:
                            saveInfo.time_delay = float(message_list[2])
                            saveInfo.save()
                            await message.channel.send("Delay changed to " + message_list[2] + " seconds")
                        else:
                            await message.channel.send("Delay cannot be larger than 10 seconds")
                    else:
                        await message.channel.send("Permission required to use this command")

                # team management submenu message_list[2] will be the index number
                if message_list[1] == "team":
                    # to compensate for the altered indexing, lower the value by 1 (I did this late, so it is kinda skuffed)
                    message_list[2] = str(int(message_list[2])-1)
                    # check to see if the team exists
                    if 0 <= int(message_list[2]) < len(saveInfo.team_bucket):
                        # team info prints the name, wins, losses, championships, and lists the batters and pitchers
                        if message_list[3] == "info":
                            await message.channel.send(str(saveInfo.team_readout(int(message_list[2]))))

                        # player info prints the stats of a player
                        if message_list[3] == "player":
                            # if the user tries to look up a player, then compensate for indexing
                            message_list[4] = str(int(message_list[4]) - 1)
                            # translation: If the selection is greater than the number of batters + pitchers, or less than 0
                            if (int(message_list[4]) >= (len(saveInfo.team_bucket[int(message_list[2])].batters) + len(saveInfo.team_bucket[int(message_list[2])].pitchers))) or (int(message_list[4]) < 0):
                                await message.channel.send("This player does not exist")
                            else:
                                await message.channel.send(saveInfo.player_readout(int(message_list[2]), int(message_list[4])))

                        # team specific role stuff
                        if message_list[3] == "role":
                            # if the user wants to add a new team role to themself
                            if message_list[4] == "add":
                                check = 0
                                # check if they have the role
                                for i in range(len(message.author.roles)):
                                    if message.author.roles[i].id == saveInfo.team_bucket[int(message_list[2])].roleID:
                                        check = 1
                                if check == 1:
                                    await message.channel.send("You already have this role")
                                else:
                                    await message.author.add_roles(
                                        guild.get_role(saveInfo.team_bucket[int(message_list[2])].roleID))
                                    await message.channel.send("Welcome to the " + saveInfo.team_bucket[int(message_list[2])].name + "!")
                                    # same for remove
                            elif message_list[4] == "remove":
                                check = 0
                                for i in range(len(message.author.roles)):
                                    if message.author.roles[i].id == saveInfo.team_bucket[int(message_list[2])].roleID:
                                        check = 1
                                if check == 1:
                                    await message.author.remove_roles(
                                        guild.get_role(saveInfo.team_bucket[int(message_list[2])].roleID))
                                    await message.channel.send("Role Removed")
                                else:
                                    await message.channel.send("You already do not have this role")

                        # if an admin
                        if message_list[3] == "remove":
                            # if the league is active, a team cannot be removed
                            if saveInfo.league_active == 0:
                                # delete the role
                                team_role = guild.get_role(saveInfo.team_bucket[int(message_list[2])].roleID)
                                await team_role.delete()
                                # delete the channel
                                team_channel = guild.get_channel(saveInfo.team_bucket[int(message_list[2])].channelID)
                                await team_channel.delete()
                                # delete from the file
                                await message.channel.send(saveInfo.team_bucket[int(message_list[2])].name + " has been removed")
                                saveInfo.team_bucket.pop(int(message_list[2]))
                                saveInfo.save()
                            else:
                                message.channel.send("A team cannot be removed while a league is in progress")
                    else:
                        await message.channel.send("Invalid input: This team does not exist")

                    # team edit submenu
                    if message_list[3] == "edit":
                        if admin_permission == 1:
                            # check if a team exists
                            if 0 <= int(message_list[2]) < len(saveInfo.team_bucket):
                                # team x edit name [name]
                                if message_list[4] == "name":
                                    # block of code to format the team name properly
                                    teamName = ""
                                    for i in range(len(message_list)):
                                        if i > 4:
                                            if i == len(message_list) - 1:
                                                teamName = teamName + message_list[i]
                                            else:
                                                teamName = teamName + message_list[i] + " "
                                    # finalize formatting and send confirmation
                                    returnMessage = saveInfo.team_bucket[int(message_list[2])].name + " is now " + teamName
                                    await message.channel.send(returnMessage)
                                    # make the change and save
                                    saveInfo.team_bucket[int(message_list[2])].name = teamName
                                    await guild.get_channel(saveInfo.team_bucket[int(message_list[2])].channelID).edit(
                                        name=teamName)
                                    saveInfo.save()
                                # BLA team x edit player y [name]
                                if message_list[4] == "player":
                                    # block of code to format the team name properly
                                    message_list[5] = str(int(message_list[5]) - 1)
                                    playerName = ""
                                    for i in range(len(message_list)):
                                        if i > 5:
                                            if i == len(message_list) - 1:
                                                playerName = playerName + message_list[i]
                                            else:
                                                playerName = playerName + message_list[i] + " "
                                    if int(message_list[5]) > len(saveInfo.team_bucket[int(message_list[2])].batters):
                                        i = int(message_list[5]) - len(saveInfo.team_bucket[int(message_list[2])].batters)
                                        # finalize formatting and send confirmation
                                        returnMessage = saveInfo.team_bucket[int(message_list[2])].pitchers[
                                                            i].name + " is now " + playerName
                                        await message.channel.send(returnMessage)
                                        # make the change and save
                                        saveInfo.team_bucket[int(message_list[2])].pitchers[i].name = playerName
                                    else:
                                        i = int(message_list[5])
                                        # finalize formatting and send confirmation
                                        returnMessage = saveInfo.team_bucket[int(message_list[2])].batters[
                                                            i].name + " is now " + playerName
                                        await message.channel.send(returnMessage)
                                        # make the change and save
                                        saveInfo.team_bucket[int(message_list[2])].batters[i].name = playerName

                                    saveInfo.save()
                            else:
                                message.channel.send("Invalid input: This team does not exist")
                        else:
                            await message.channel.send("Permission required to use this command")


                if message_list[1] == "playLeague":
                    if admin_permission == 1:
                        if len(saveInfo.league_schedule) == 0:
                            await message.channel.send("You must have a schedule to start a game")
                        else:
                            # activate the league
                            if saveInfo.league_active == 0:
                                # the league will start at this time every day
                                saveInfo.game_start_time = int(time.time())
                                saveInfo.league_active = 1
                                saveInfo.save()
                                await guild.get_channel(saveInfo.game_channel_id).send(guild.get_role(saveInfo.general_role_id).mention + " the first game is about to start!")
                                # send the game activation
                                await message.channel.send("Starting Next Game...")
                            else:
                                await message.channel.send("League is currently active")
                    else:
                        await message.channel.send("Permission required to use this command")

                if message_list[1] == "waitFix" and saveInfo.league_active == 1:
                # if something happens and the countdown breaks
                    if admin_permission == 1:
                        # send a blue checkmark to the send message
                        await message.add_reaction("\u2611")
                    else:
                        await message.channel.send("Permission required to use this command")

                # if a game stops, an admin can restart it
                if message_list[1] == "restartGame":
                    if admin_permission == 1:
                        if saveInfo.league_active == 1:
                            watch_channel = guild.get_channel(saveInfo.game_channel_id)
                            await watch_channel.send("An admin has issed a command to restart a stopped game")
                            await message.channel.send("Starting Next Game...")
                        else:
                            await message.channel.send("The League is not active")
                    else:
                        await message.channel.send("Permission required to use this command")
            elif message_list[1] != "generate" and message_list[1] != "help":
                await message.channel.send("A league must be generated before this command can be executed")

            # generate the blaseball infrastructure in a server
            if message_list[1] == "generate":
                if message.author.guild_permissions.administrator == 1:
                    # it will also create 2 roles. one for general blaseball, the other for blaseball admins
                    confirmation_message = await message.channel.send("Please wait...")

                    server_ID = guild.id

                    # if the bot joins the server, it looks for an existing save file. If it can't find it, then it it will generate
                    # one and also generate relevant roles and channels

                    # create/empty a save file with the server ID as the name
                    save_file = open(str(server_ID) + ".json", "w")
                    save_file.close()

                    # throughout, the save info object is being populated
                    # create a blank save
                    saveInfo = functions.blank_save(server_ID)

                    # create general blaseball role
                    general_role = await guild.create_role(name="Blaseball Fan", color=0x944f20)
                    saveInfo.general_role_id = general_role.id

                    # create admin blaseball role
                    admin_role = await guild.create_role(name="Blaseball Admin", color=0x44A9AA)
                    saveInfo.admin_role_id = admin_role.id

                    # create a category
                    category = await guild.create_category(name="Blaseball")
                    saveInfo.category_id = category.id

                    # set the self role to view the category
                    await category.set_permissions(target=guild.self_role, read_messages=True, send_messages=True)
                    # Set the everyone role to not be able to read messages
                    await category.set_permissions(target=guild.default_role, read_messages=False)
                    # set the general role to read messages
                    await category.set_permissions(target=general_role, read_messages=True)
                    # set the admin role to read messages
                    await category.set_permissions(target=admin_role, read_messages=True)

                    # create game channel
                    game_channel = await guild.create_text_channel(name="watch-the-game", category=category)
                    await game_channel.set_permissions(target=guild.default_role, read_messages=False,
                                                       send_messages=False)
                    await game_channel.set_permissions(target=general_role, read_messages=True, send_messages=False)
                    await game_channel.set_permissions(target=admin_role, read_messages=True, send_messages=False)
                    saveInfo.game_channel_id = game_channel.id

                    # create league schedule channel
                    schedule_channel = await guild.create_text_channel(name="league-schedule", category=category)
                    await schedule_channel.set_permissions(target=guild.default_role, read_messages=False,
                                                           send_messages=False)
                    await game_channel.set_permissions(target=general_role, read_messages=True, send_messages=False)
                    await game_channel.set_permissions(target=admin_role, read_messages=True, send_messages=False)
                    saveInfo.schedule_channel_id = schedule_channel.id

                    # create a general channel
                    general_channel = await guild.create_text_channel(name="blaseball-general", category=category)
                    saveInfo.general_channel_id = general_channel.id

                    # create an admin channel
                    admin_channel = await guild.create_text_channel(name="admin-channel", category=category)
                    await admin_channel.set_permissions(target=general_role, read_messages=False)
                    saveInfo.admin_channel_id = admin_channel.id

                    # name of the league
                    saveInfo.league_name = guild.name + " League"

                    # the league is generated
                    saveInfo.gen_state = 1

                    # save the info
                    saveInfo.save()
                    await confirmation_message.edit(content="The Bot is successfully configured for the " + saveInfo.league_name + "!")

                    # send a first help message in admin channel
                    await admin_channel.send(
                        "`Bot Successfully configured! Welcome to the " + saveInfo.league_name + "\nType 'BLA help' for a commands list`")
                    await general_channel.send(
                        "`Bot Successfully configured! Welcome to the " + saveInfo.league_name + "\nType 'BLA help' for a commands list`")
                else:
                    await message.channel.send("You must be a server Admin to use this command")


            # help fp,,and
            if message_list[1] == "help":
                helpMessage = "SERVER LEAGUE BLASEBOT V: ALPHA 1\nTo start the bot, type 'BLA generate'\n*Each game starts 24 hours after the last one*\n"
                helpMessage = helpMessage + "This bot is in a very early state. It can currently only create a league, give some roles, create and lightly manage teams and can " \
                                            "also run some games I guess. If there are any problems, let me know!\nMy discord is Jenywlfersn#0797. Hope to hear from you!"
                await message.author.send(helpMessage)
                helpMessage = "**DISCORD LEAGUE BLASEBOT HELP**\n\n"
                helpMessage = helpMessage + "`BLA join`\n"
                helpMessage = helpMessage + "  -When sent in a server, lets you watch blaseball!"
                helpMessage = helpMessage + "`BLA leave`\n"
                helpMessage = helpMessage + "  -When sent in a server, stops letting you see blaseball"
                helpMessage = helpMessage + "`BLA teams`\n"
                helpMessage = helpMessage + "  -When sent in a server, lists the names of the teams in the server\n"
                helpMessage = helpMessage + "`BLA team [x] info`\n"
                helpMessage = helpMessage + "  -When sent in a server, lists the names of the players on a team. (do not include the brackets)\n"
                helpMessage = helpMessage + "`BLA team [x] player [y]`\n"
                helpMessage = helpMessage + "  -When sent in a server, lists the stats of a player. (do not include the brackets)\n"
                helpMessage = helpMessage + "`BLA team [x] role add`\n"
                helpMessage = helpMessage + "  -When sent in a server, gives you the role of team [x]. (do not include the brackets)\n"
                helpMessage = helpMessage + "`BLA team [x] role remove`\n"
                helpMessage = helpMessage + "  -When sent in a server, removes the role of team [x] from you. (do not include the brackets)\n"
                await message.author.send(helpMessage)
                if admin_permission == 1:
                    helpMessage = "**DISCORD LEAGUE BLASEBOT ADMIN HELP**\n\n"
                    helpMessage = helpMessage + "`BLA generate`\n"
                    helpMessage = helpMessage + "  -When sent in a server, this command will generate a new category and roles as well as delete all teams. Any old categories or roles will have to be manually deleted.\n"
                    helpMessage = helpMessage + "`BLA new team [name]`\n"
                    helpMessage = helpMessage + "  -When sent in a server, creates a new team with randomly generated players. (name can be multiple words)\n"
                    helpMessage = helpMessage + "`BLA new schedule`\n"
                    helpMessage = helpMessage + "  -creates a round robin schedule and puts it in the schedule channel\n"
                    helpMessage = helpMessage + "`BLA team [x] edit name [name]`\n"
                    helpMessage = helpMessage + "  -When sent in a server, changes the name of a team\n"
                    helpMessage = helpMessage + "`BLA team [x] edit player [y] [name]`\n"
                    helpMessage = helpMessage + "  -When sent in a server, the player's name will be changed. (name can be multiple words)\n"
                    helpMessage = helpMessage + "`BLA team [x] remove`\n"
                    helpMessage = helpMessage + "  -When sent in a server, the team is removed\n"
                    helpMessage = helpMessage + "`BLA league name [name]`\n"
                    helpMessage = helpMessage + "  -When sent in a server, changes the leagues name\n"
                    helpMessage = helpMessage + "`BLA playleague`\n"
                    helpMessage = helpMessage + "  -When sent in a server, starts the league (CANNOT CURRENTLY BE STOPPED)\n"
                    helpMessage = helpMessage + "`BLA waitFix`\n"
                    helpMessage = helpMessage + "  -To only be used if the time till counter breaks\n"
                    helpMessage = helpMessage + "`BLA delay [x]`\n"
                    helpMessage = helpMessage + "  -Will change the delay between messages in blaseball games\n"
                    helpMessage = helpMessage + "`BLA restartGame`\n"
                    helpMessage = helpMessage + "  -If a game crashes, this will restart it. WARNING: DOES NOT STOP THE PREVIOUS GAME IF IT IS STILL RUNNING"
                    await message.author.send(helpMessage)
                await message.channel.send("Help has been sent to your DM's")

                # this event will be for keeping track of the thing


@client.event
async def on_raw_reaction_add(payload):
    # there are two circumstances this will be used. If a game is ending, or if a wait is being fixed
    # test if bot and if a valid emoji
    if (client.get_guild(payload.guild_id).get_member(
            payload.user_id) == client.user) and (payload.emoji.name == "\u2705" or payload.emoji.name == "\u2611"):
        # create a blank save
        saveInfo = functions.blank_save(payload.guild_id)
        # fill the blank save
        saveInfo = saveInfo.load()

        guild = client.get_guild(payload.guild_id)

        # this is to fix earlier mistakes
        # There was an error that occurred if the wait broke before the last game. If a waitfix happened, then it would display the championship results
        # this wait check is to avoid that
        wait_check = 1

        # if the emoji is the blue check, then it is for waiting
        if payload.emoji.name == "\u2611":
            wait_check = 0

        if saveInfo.schedule_position <= len(saveInfo.league_schedule)-1 and wait_check == 0:
            # if the check is green, then advance the league and get a new time
            if payload.emoji.name == "\u2705":
                # advance the league
                saveInfo.schedule_position = saveInfo.schedule_position + 1
                # update the schedule message
                schedule_channel = guild.get_channel(saveInfo.schedule_channel_id)
                schedule_message = await schedule_channel.fetch_message(saveInfo.schedule_message_id)
                await schedule_message.edit(content=saveInfo.schedule_text())
                # get the time since last game (new time is old time + 86400)
                new_time = saveInfo.game_start_time + 86400
                saveInfo.game_start_time = new_time
                # send the wait message
                message = await client.get_guild(payload.guild_id).get_channel(saveInfo.game_channel_id).send(str(math.ceil((new_time - int(time.time())) / (3600))) + " hours till next game")
                # wait an hour to check the message again to save on memory
                await asyncio.sleep(60*60)
            else:
                # if the check is blue, then do not advance
                new_time = saveInfo.game_start_time
                # this message is the confirmation message in this case
                message = await client.get_guild(payload.guild_id).get_channel(saveInfo.game_channel_id).send("An error occured and an admin has issued a fix")

            # signal to control the loop
            time_signal = 0
            saveInfo.save()
            # empty these variables to save on memory
            saveInfo = 0
            guild = 0
            fiveMin_signal = 0
            while time_signal == 0:
                # while the game is waiting
                # if the game is more than an hour away, display an hours message
                if new_time - int(time.time()) > 3600:
                    await message.edit(
                        content=str(math.ceil((new_time - int(time.time())) / (3600))) + " hours till next game")
                    # wait 10 minutes between these
                    await asyncio.sleep(60*10)
                # if the game is less than an hour away, display a minutes message
                elif new_time - int(time.time()) <= 3600:
                    await message.edit(
                        content=str(math.ceil((new_time - int(time.time())) / (60))) + " minutes till next game")
                    # wait a minute between these
                    await asyncio.sleep(60)

                # this is for sending a ping to watchers 5 minutes before the game starts
                if new_time - int(time.time()) <= 300 and fiveMin_signal == 0:
                    # don't send this message again
                    fiveMin_signal = 1
                    saveInfo = functions.blank_save(payload.guild_id)
                    # fill the blank save
                    saveInfo = saveInfo.load()
                    guild = client.get_guild(payload.guild_id)
                    # ping people
                    await client.get_guild(payload.guild_id).get_channel(saveInfo.game_channel_id).send(guild.get_role(saveInfo.general_role_id).mention + " the next game is about to start!")
                    # blank stuff out again
                    saveInfo = 0
                    guild = 0
                # if time is up:
                if int(time.time()) >= new_time:
                    time_signal = 1
                    await message.edit(content="Beginning the next game!")

            guild = client.get_guild(payload.guild_id)
            # create a blank save
            saveInfo = functions.blank_save(payload.guild_id)
            # fill the blank save
            saveInfo = saveInfo.load()
            saveInfo.game_start_time = new_time
            admin_channel = guild.get_channel(saveInfo.admin_channel_id)
            saveInfo.save()
            # send the start signal
            await admin_channel.send("Starting Next Game...")
            # delete the timer message after a few seconds
            await message.delete(delay=5)
        # if the league is over
        elif saveInfo.schedule_position == len(saveInfo.league_schedule)-1 and wait_check == 1:
            guild = client.get_guild(payload.guild_id)
            saveInfo.league_active = 0
            # get the team with the most wins
            most_wins_team = -1
            most_wins_amount = -1
            for i in range(len(saveInfo.team_bucket)):
                if saveInfo.team_bucket[i].wins > most_wins_amount:
                    most_wins_team = i
                    most_wins_amount = saveInfo.team_bucket[i].wins
            # add a championship to them
            saveInfo.team_bucket[most_wins_team].championships = saveInfo.team_bucket[most_wins_team].championships + 1
            # empty the schedule
            saveInfo.league_schedule = []
            # league is not active
            saveInfo.league_active = 0
            # clear wins and losses
            for i in range(len(saveInfo.team_bucket)):
                saveInfo.team_bucket[i].wins = 0
                saveInfo.team_bucket[i].losses = 0
            # send messages
            await client.get_channel(saveInfo.game_channel_id).send(
                saveInfo.team_bucket[most_wins_team].name + " win the championship with " + str(most_wins_amount) + " wins!")
            await asyncio.sleep(saveInfo.time_delay)
            await client.get_channel(saveInfo.game_channel_id).send("congratulations!")
            await asyncio.sleep(saveInfo.time_delay)
            await client.get_channel(saveInfo.game_channel_id).send("This concludes a test Blaseball league! Thank you all so much for watching! Be sure to give Jeny any feedback to make this better!")

            schedule_channel = guild.get_channel(saveInfo.schedule_channel_id)
            schedule_message = await schedule_channel.fetch_message(saveInfo.schedule_message_id)
            await schedule_message.edit(content=saveInfo.schedule_text() + "\n Season is finished!")
            saveInfo.save()


@client.event
async def on_guild_remove(guild):
    # if the bot leaves a server, delete the save file
    os.remove(str(guild.id) + ".json")




client.run("")
