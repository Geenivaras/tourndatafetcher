import json
import sys

user_id = 0

class Tournament:
    def __init__(self, key, entrants, online, rank, placing, name, date):
        self.key = key
        self.entrants = entrants
        self.online = online
        self.rank = rank
        self.placing = placing
        self.name = name
        self.date = date
        self.sets = []

    def addSet(self, set):
        self.sets.append(Set(set))

    def toString(self):
        print("key: " + self.key + " entrants: " + self.entrants + " online: " + self.online + " rank: " + self.rank + " placing: " + self.placing + " name: " + self.name + " date: " + self.date)
        for set in self.sets:
            set.toString()

class Set:
    def __init__(self, set):
        self.bracket_order = set['bracket_order']
        self.characters = set['characters']
        self.games = []
        self.location = set['location']
        self.opponent = set['opponent']
        self.opponent_id = set['opponent_id']
        self.ranking = set['ranking']
        self.score = set['score']
        self.set_order = set['set_order']
        self.tournament = set['tournament']
        self.use_id = set['use_id']
        self.won = set['won']
        for game in set['games']:
            self.games.append(Game(game))

    def toString(self):
        print(self.score)
        for game in self.games:
            game.toString()

class Game:
    def __init__(self, game):
        self.loser_char = game['loser_char']
        self.loser_id = game['loser_id']
        self.stage = game['stage']
        self.winner_char = game['winner_char']
        self.winner_id = game['winner_id']
        self.won = True if (self.winner_id == user_id) else False
        self.opponent_char = self.loser_char if(self.won) else self.winner_char

    def toString(self):
        print(self.stage)

def tournDataToClasses(json_filename, html_filename):
    tournaments = []
    sets = []
    games = []

    with open(json_filename, encoding="utf8") as jsonfile:
        data = json.load(jsonfile)

    global user_id 

    index = 0
    while True:
        if(len(data[index]['games']) == 0):
            index += 1
            continue

        opp_id = data[index]['opponent_id']
        winner_id = data[index]['games'][0]['winner_id']
        loser_id = data[index]['games'][0]['loser_id']

        user_id = winner_id if(int(winner_id) != int(opp_id)) else loser_id
        break

    with open(html_filename,  encoding="utf8") as textfile:
        index = 0

        while True:
            line = textfile.readline()
            if not line:
                break

            if(len(line.split()) < 2):
                continue
            elif(line.split()[1] == "class=\"tournament-listing\""):
                key = textfile.readline().split('\"')[1]
                entrants = textfile.readline().split('\"')[1]
                online = textfile.readline().split('\"')[1]
                rank = textfile.readline().split('\"')[1]
                textfile.readline()
                placing = textfile.readline().split('\"')[1]
                name = textfile.readline().split('\"')[1]
                for i in range(7):
                    textfile.readline()
                date = textfile.readline().split('>')[1][:8]
                tournaments.append(Tournament(key, entrants, online, rank, placing, name, date))

            elif(len(line.split()) < 3):
                continue
            
            elif(line.split()[2] == "class=\"tournament-sets"):
                for i in range(9):
                    textfile.readline()

                while True:
                    set_index = textfile.readline().split('\"')[7]
                    tournaments[index].addSet(data[int(set_index)])
                    sets.append(Set(data[int(set_index)]))
                    for game in data[int(set_index)]['games']:
                        games.append(Game(game))

                    for i in range(17):
                        textfile.readline()

                    if not (textfile.readline().strip() == ''):
                        index += 1
                        break
                        
                    for i in range(2):
                        textfile.readline()
    
    return tournaments, sets, games

def stageWinRate(stagename, data):
    games = 0
    wins = 0
    for game in data:
        if(game.stage == stagename):
            games += 1
            if(game.won):
                wins += 1
    if(games != 0):
        print("{}: {} {} {}".format(stagename, wins, games, round(wins/games, 2)))
    else:
        print("{}: No games".format(stagename))

def characterWinRate(charactername, data):
    games = 0
    wins = 0
    for game in data:
        if(game.opponent_char == charactername):
            games += 1
            if(game.won):
                wins += 1
    if(games != 0):
        print("{}: {} {} {}".format(charactername[9:].capitalize(), wins, games, round(wins/games, 2)))
    else:
        print("{}: No games against".format(charactername[9:].capitalize()))

def characterNameSet(data):
    character_name_set = set()

    for game in data:
        character_name_set.add(game.loser_char)
        character_name_set.add(game.winner_char)

    return character_name_set

def stageNameSet(data):
    stage_name_set = set()

    for game in data:
        stage_name_set.add(game.stage)

    return stage_name_set

def main(argv):
    # global user_id
    # user_id = argv[2]
    tournaments, sets, games = tournDataToClasses(argv[0], argv[1])
    
    stage_name_set = stageNameSet(games)
    for stage in stage_name_set:
        if(stage != None):
            stageWinRate(stage, games)

    character_name_set = characterNameSet(games)
    for character in character_name_set:
        if(character != None):
            characterWinRate(character, games)

if __name__ == "__main__":
    main(sys.argv[1:])

'''
function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}
download(JSON.stringify(data), 'playertag.json', 'text/plain');
'''