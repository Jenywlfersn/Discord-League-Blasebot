import json
import jsonpickle
import random


class save_class:
    def __init__(self, server_id, general_role_id, admin_role_id, category_id, game_channel_id, schedule_channel_id,
                 general_channel_id, admin_channel_id, schedule_message_id, team_channels, league_name, team_bucket,
                 league_schedule, schedule_position, member_id_list, next_bet_list, fan_vote_list):
        self.server_id = server_id
        self.general_role_id = general_role_id
        self.admin_role_id = admin_role_id
        self.category_id = category_id
        self.game_channel_id = game_channel_id
        self.schedule_channel_id = schedule_channel_id
        self.general_channel_id = general_channel_id
        self.admin_channel_id = admin_channel_id
        self.schedule_message_id = schedule_message_id
        self.team_channels = []
        self.league_name = league_name
        self.team_bucket = []
        self.league_schedule = []
        self.schedule_position = schedule_position
        self.member_id_list = []
        self.next_bet_list = []
        self.fan_vote_list = []
        self.game_start_time = 0
        self.league_active = 0
        self.gen_state = 0
        self.time_delay = 4.5

    def save(self):
        # pickify the self. Starting by copying just in case things break
        tempself = self
        pickleself = jsonpickle.encode(tempself)
        # open the save file
        jsonFile = open(str(self.server_id) + ".json", "w")
        # dump the league into a json
        json.dump(pickleself, jsonFile)

        jsonFile.close()

    def load(self):
        # open the save file
        jsonFile = open(str(self.server_id) + ".json", "r")
        # load from json file
        pickleself = json.load(jsonFile)
        # close json
        jsonFile.close()
        # depicklify
        self = jsonpickle.decode(pickleself)
        return self

    def schedule_text(self):
        message_text = "__**"+self.league_name+" Schedule:**__\n"
        # this is all done with specific markdowns to make it look good. but it is just adding to a message very strangely
        for i in range(len(self.league_schedule)):
            if i < self.schedule_position:
                message_text = message_text+"~~"+str(i+1)+": "+self.team_bucket[self.league_schedule[i].team1].name+" vs "+self.team_bucket[self.league_schedule[i].team2].name+"~~\n"
            elif i == self.schedule_position:
                message_text = message_text + "*---------*\n"
                message_text = message_text + "**Upcoming Game:**\n"
                message_text = message_text + "**" + str(i+1) + ": " + self.team_bucket[self.league_schedule[i].team1].name + " vs " + self.team_bucket[self.league_schedule[i].team2].name + "**\n"
                message_text = message_text + "*Pitchers: " + self.team_bucket[self.league_schedule[i].team1].pitchers[self.team_bucket[self.league_schedule[i].team1].pitcher_index].name + " vs " + self.team_bucket[self.league_schedule[i].team2].pitchers[self.team_bucket[self.league_schedule[i].team2].pitcher_index].name + "*\n"
                message_text = message_text + "*---------*\n"
            elif i > self.schedule_position:
                message_text = message_text + str(i+1) + ": " + self.team_bucket[self.league_schedule[i].team1].name + " vs " + self.team_bucket[self.league_schedule[i].team2].name+"\n"
        return message_text

    def team_readout(self, index):
        message_text = ""
        # name
        message_text = message_text + self.team_bucket[index].name + "\n"
        # wins
        message_text = message_text + "Wins: " + str(self.team_bucket[index].wins) + "\n"
        # losses
        message_text = message_text + "Losses: " + str(self.team_bucket[index].losses) + "\n"
        # championships
        message_text = message_text + "Championships: " + str(self.team_bucket[index].championships) + "\n"
        # begin batter list
        message_text = message_text + "\n*BATTERS*\n"
        # for loop through all the stuff
        for i in range(len(self.team_bucket[index].batters)):
            # i+1 to do funny indexing
            message_text = message_text + str(i+1) + ": " + self.team_bucket[index].batters[i].name + "\n"

        i = i+1
        # begin pitcher list
        message_text = message_text + "\n*PITCHERS*\n"

        for j in range(len(self.team_bucket[index].pitchers)):
            message_text = message_text + str(i+j+1) + ": " + self.team_bucket[index].pitchers[j].name + "\n"
        return message_text

    def player_readout(self, team_index, player_index):
        message_text = ""
        if player_index > len(self.team_bucket[team_index].batters) - 1: # a pitcher was picked
            player_index = player_index - len(self.team_bucket[team_index].batters)
            player_list = self.team_bucket[team_index].pitchers
            message_text = message_text + str(player_index+len(self.team_bucket[team_index].batters)+1) + ": " + player_list[player_index].name + "\n"
        else:
            player_list = self.team_bucket[team_index].batters
            message_text = message_text + str(player_index+1) + ": " + player_list[player_index].name + "\n"


        if player_list[player_index].position == 1:
            message_text = message_text+"Batter for the "+self.team_bucket[team_index].name+"\n\n"
        elif player_list[player_index].position == 2:
            message_text = message_text+"Pitcher for the "+self.team_bucket[team_index].name+"\n\n"
        message_text = message_text+"Stats:\n"
        message_text = message_text+"Pitching:\n"
        message_text = message_text+"   whirling: "+str(player_list[player_index].whirling)+"\n"
        message_text = message_text + "   curvitude: " + str(player_list[player_index].curvitude)+"\n"
        message_text = message_text + "   sunfloweryness: " + str(player_list[player_index].sunfloweryness)+"\n"
        message_text = message_text + "Running:\n"
        message_text = message_text + "   relativity: " + str(player_list[player_index].relativity) + "\n"
        message_text = message_text + "   electrification: " + str(player_list[player_index].electrification) + "\n"
        message_text = message_text + "   unviscosity: " + str(player_list[player_index].unviscosity) + "\n"
        message_text = message_text + "Batting:\n"
        message_text = message_text + "   bean saturation: " + str(player_list[player_index].bean_saturation) + "\n"
        message_text = message_text + "   torquiness: " + str(player_list[player_index].torquiness) + "\n"
        message_text = message_text + "   calcium density: " + str(player_list[player_index].calcium_density) + "\n"
        message_text = message_text + "Fielding:\n"
        message_text = message_text + "   springyness: " + str(player_list[player_index].springyness) + "\n"
        message_text = message_text + "   anti gravitude: " + str(player_list[player_index].anti_gravitude) + "\n"
        message_text = message_text + "   omnipresence: " + str(player_list[player_index].omnipresence) + "\n\n"
        gender_list_file = open("gender_list.txt", "r")
        gender_list_read = gender_list_file.read()  # read all of the list
        gender_list = gender_list_read.split("\n")  # cut out all of the newlines
        gender_list_file.close()
        message_text = message_text + "Zodiac: "+gender_list[player_list[player_index].zodiac]+"\n"
        message_text = message_text + "Gender: "+gender_list[player_list[player_index].gender]+"\n"
        return message_text


class team_class:
    def __init__(self, name, wins, losses, championships, channelID, roleID, batters, pitchers, pitcher_index):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.championships = championships
        self.channelID = channelID
        self.roleID = roleID
        self.batters = []
        self.pitchers = []
        self.pitcher_index = pitcher_index


class player_class:
    def __init__(self, name, position, whirling, curvitude, sunfloweryness, relativity, electrification,
                 unviscosity, springyness, anti_gravitude, omnipresence, bean_saturation, torquiness, calcium_density,
                 zodiac, gender, item, special, life, effects):
        self.name = name
        self.position = position
        self.whirling = whirling
        self.curvitude = curvitude
        self.sunfloweryness = sunfloweryness
        self.relativity = relativity
        self.electrification = electrification
        self.unviscosity = unviscosity
        self.springyness = springyness
        self.anti_gravitude = anti_gravitude
        self.omnipresence = omnipresence
        self.bean_saturation = bean_saturation
        self.torquiness = torquiness
        self.calcium_density = calcium_density
        self.zodiac = zodiac
        self.gender = gender
        self.item = item
        self.special = special
        self.life = life
        self.effects = []


class match_class:
    # each match will be part of a list of matches
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2


class game_class:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.half = 1
        self.inning = 1
        self.first = -1
        self.second = -1
        self.third = -1
        self.team_1_score = 0
        self.team_2_score = 0
        self.strikes = 0
        self.balls = 0
        self.outs = 0
        self.half_change = 0
        self.team1_batter = 0
        self.team2_batter = 0
        self.current_batter = 0
        self.message_list = []
        self.end_signal = 0
        self.heat = 0

    def change_halves(self):
        # half 1 is first half
        if self.half == 1:
            self.team1_batter = self.current_batter
            self.current_batter = self.team2_batter
            self.half = 2
        elif self.half == 2:
            self.team2_batter = self.current_batter
            self.current_batter = self.team1_batter
            self.half = 1
            self.inning = self.inning+1
        self.strikes = 0
        self.balls = 0
        self.outs = 0
        self.first = -1
        self.second = -1
        self.third = -1
        self.half_change = 0

    def new_inning(self):
        self.inning = self.inning+1

    def add_strike(self):
        self.strikes = self.strikes+1

    def add_ball(self):
        self.balls = self.balls+1

    def add_out(self):
        self.outs = self.outs+1

    def score(self):
        # in half 1, team 1 bats
        if self.half == 1:
            self.team_1_score = self.team_1_score+1
        elif self.half == 2:
            self.team_2_score = self.team_2_score+1

    def walk(self):
        # all concievable walk possablilities
        self.balls = 0
        if self.half == 1:
            self.message_list.append(self.team2.pitchers[self.team2.pitcher_index].name+" walks "+self.team1.batters[self.current_batter].name+"!")
        else:
            self.message_list.append(self.team1.pitchers[self.team1.pitcher_index].name + " walks " + self.team2.batters[self.current_batter].name + "!")
        if self.first == -1:
            self.first = self.current_batter
            if self.half == 1:
                if self.current_batter == len(self.team1.batters):
                    self.current_batter = 0
            elif self.half == 2:
                if self.current_batter == len(self.team2.batters):
                    self.current_batter = 0
        elif (self.first != -1)and(self.second == -1):
            self.second = self.first
            self.first = self.current_batter
            if self.half == 1:
                if self.current_batter == len(self.team1.batters):
                    self.current_batter = 0
            elif self.half == 2:
                if self.current_batter == len(self.team2.batters):
                    self.current_batter = 0
        elif (self.first != -1)and(self.second != -1)and(self.third == -1):
            self.third = self.second
            self.second = self.first
            self. first = self.current_batter
        elif (self.first != -1)and(self.second != -1)and(self.first != -1):
            if self.half == 1:
                self.message_list.append(self.team1.batters[self.third].name+" walks in")
            elif self.half == 2:
                self.message_list.append(self.team2.batters[self.third].name+" walks in")
            self.score()

            self.third = self.second
            self.second = self.first
            self.first = self.current_batter

        self.new_batter()

    def display_text(self):
        # init the message with the markdown
        message_text = "```"
        # init the spaces
        spaces = ""
        # gather enough spaces to put the score halfway in the name
        for i in range(int((len(self.team1.name))/2)-1):
            spaces = spaces+" "
        # message format with 4 spaces after for " vs "
        message_text = message_text+spaces+str(self.team_1_score)+spaces+"    "
        spaces = ""
        # gather enough spaces for the same reason as before
        for i in range(int((len(self.team2.name))/2)):
            spaces = spaces+" "
        # first line done
        message_text = message_text+spaces+str(self.team_2_score)+"\n"

        # second line
        message_text = message_text+self.team1.name+" vs "+self.team2.name+"\n\n"

        if self.half == 1:
            half_text = "Top"
        else:
            half_text = "Bottom"

        if self.inning == 1:
            suffix = "st"
        elif self.inning == 2:
            suffix = "nd"
        elif self.inning == 3:
            suffix = "rd"
        elif self.inning > 3:
            suffix = "th"

        message_text = message_text+half_text+" of the "+str(self.inning)+suffix+"\n\n"

        # needs to be split by halves
        if self.half == 1:
            # bases
            if self.first != -1:
                message_text = message_text+"First: "+self.team1.batters[self.first].name+"\n"
            elif self.first == -1:
                message_text = message_text + "First:\n"
            if self.second != -1:
                message_text = message_text+"Second: "+self.team1.batters[self.second].name+"\n"
            elif self.second == -1:
                message_text = message_text + "Second:\n"
            if self.third != -1:
                message_text = message_text+"Third: "+self.team1.batters[self.third].name+"\n\n"
            elif self.third == -1:
                message_text = message_text + "Third:\n\n"
            # batter and pitcher
            if self.half_change == 0:
                message_text = message_text+"Batter: "+self.team1.batters[self.current_batter].name+" (" + self.team1.name + ")\n"
            else:
                message_text = message_text+"Batter:\n"
            message_text = message_text+"Pitcher: "+self.team2.pitchers[self.team2.pitcher_index].name+" (" + self.team2.name + ")\n\n"
        elif self.half == 2:
            # bases
            if self.first != -1:
                message_text = message_text + "First: " + self.team2.batters[self.first].name + "\n"
            elif self.first == -1:
                message_text = message_text + "First:\n"
            if self.second != -1:
                message_text = message_text + "Second: " + self.team2.batters[self.second].name + "\n"
            elif self.second == -1:
                message_text = message_text + "Second:\n"
            if self.third != -1:
                message_text = message_text + "Third: " + self.team2.batters[self.third].name + "\n\n"
            elif self.third == -1:
                message_text = message_text + "Third:\n\n"
            # batter and pitcher
            if self.half_change == 0:
                message_text = message_text + "Batter: " + self.team2.batters[self.current_batter].name +" (" + self.team2.name + ")\n"
            else:
                message_text = message_text + "Batter:\n"
            message_text = message_text + "Pitcher: " + self.team1.pitchers[self.team1.pitcher_index].name +" (" + self.team1.name + ")\n\n"
        # outs, balls, strikes
        message_text = message_text+"Outs: "+str(self.outs)+"\n"
        message_text = message_text+"Balls: "+str(self.balls)+"\n"
        message_text = message_text+"Strikes: "+str(self.strikes)+"```"
        return message_text

    def new_batter(self):
        self.current_batter = self.current_batter+1
        if self.half == 1:
            if self.current_batter == len(self.team1.batters):
                self.current_batter = 0
            if self.half_change == 0:
                self.message_list.append(self.team1.batters[self.current_batter].name + " steps up to the plate")
        elif self.half ==2:
            if self.current_batter == len(self.team2.batters):
                self.current_batter = 0
            if self.half_change == 0:
                self.message_list.append(self.team2.batters[self.current_batter].name + " steps up to the plate")
        self.strikes = 0
        self.balls = 0

    def get_average_springyness(self):
        if self.half == 1:
            team = self.team2
        else:
            team = self.team1

        value = 0
        for i in range(len(team.batters)):
            value = value + team.batters[i].springyness
        for i in range(len(team.pitchers)):
            value = value + team.pitchers[i].springyness

        value = int(value/(len(team.batters)+len(team.pitchers)))
        return value

    def get_average_omnipresence(self):
        if self.half == 1:
            team = self.team2
        else:
            team = self.team1

        value = 0
        for i in range(len(team.batters)):
            value = value + team.batters[i].omnipresence
        for i in range(len(team.pitchers)):
            value = value + team.pitchers[i].omnipresence

        value = int(value/(len(team.batters)+len(team.pitchers)))
        return value

    def get_random_fielder_name(self):
        if self.half == 1:
            team = self.team2
        else:
            team = self.team1

        index = random.randint(0,len(team.batters)+len(team.pitchers)-1)
        if index > len(team.batters) - 1: # a pitcher is selected
            index = index - len(team.batters)
            return team.pitchers[index].name
        else:
            return team.batters[index].name




