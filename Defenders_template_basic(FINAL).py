#S10243373
#Tan Ching Heng

import random
import math
import os
MAX_HEATH = 3
MAX_TURN = 10
SPAWN_CHANCE = 100
maxMonsters=1

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 3,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    "threat": 0,
    "danger_level": 0,
    "maxMonsters":1
}



field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

defender_dictionary={
    "archer" : {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 2,
          'max_damage': 5,
          'price': 5
          },
    "wall" : {'shortform': 'WALL',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3
        },
    "mine" : {'shortform': 'MINE',
        'name': 'Mine',
        'maxHP': 0,
        'min_damage': 0,
        'max_damage': 0,
        'price': 8
        }
    
    }


monster_dictionary={"zombie" : {'shortform': 'ZOMBI',
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 2
          },
                    "werewolf" : {'shortform': 'WWOLF',
          'name': 'Werewolf',
          'maxHP': 10,
          'min_damage': 2,
          'max_damage': 4,
          'moves' : 2,
          'reward': 3},
                    "skeleton" : {'shortform': 'SKELE',
          'name': 'Skeleton',
          'maxHP': 10,
          'min_damage': 1,
          'max_damage': 3,
          'moves' : 1,
          'reward': 3}
                                  }
#def sortDictionary

#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field(field,monster_dictionary,defender_dictionary):
    letters=["A","B","C","D","E"]
    rmonster=random.choice(list(monster_dictionary))
    for i in range(3):
        if i==0:                                     #if the loop is the first
            print("    ",end="")
        print("{:<6}".format(i+1),end="")              #prints the numbers on the very first row
        if i==2:                                     #if the loop reaches the last iteration of
            print()
    for i in range(5):                             
        print("",end=" ")                           #makes a spacing at the very front
        for ii in range(7):
            print("+-----",end="")
            if ii==6:
                print("+")
        print("{}".format(letters[i]),end="")
        for iii in range(7):
            if field[i][iii]==None:
                print("|     ",end="")
            else:
                if field[i][iii][2]=="defender_dictionary":
                    print("|{:^5}".format("{}".format(defender_dictionary["{}".format(field[i][iii][0])]["shortform"])),end="")
                else:
                    print("|{}".format(monster_dictionary["{}".format(field[i][iii][0])]["shortform"]),end="")        ################################
            if iii==6:
                print("|")
        print(" ",end="")
        for iiii in range(7):
            if field[i][iiii]==None:
                print("|     ",end="")
            else:
                if field[i][iiii][2]=="defender_dictionary":
                    print("|{:^5}".format("{}/{}".format(field[i][iiii][1],defender_dictionary["{}".format(field[i][iiii][0])]["maxHP"])),end="")
                else:   
                    print("|{:^5}".format("{}/{}".format(field[i][iiii][1],field[i][iiii][3])),end="")      ###############################
                
                
            if iiii==6:
                print("|")
        if i==4:
            print("",end=" ")
            for ii in range(7):
                print("+-----",end="")
            print("+",end="")
    print()
    
        
        
            
    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(field, game_vars,monster_dictionary):
    while True:
        print("1. Buy unit     2. End turn")
        print("3. Save game    4. Quit")
        menuopt=input("Your Choice?")
        try:
            int(menuopt)# checks if the user inputs a number
        except ValueError as e:
            print('"{}"'.format(menuopt), "is not a number")
        else:
            menuopt=int(menuopt)
            if not (menuopt>=1 and menuopt<=4):
                print("Invalid Option: Enter number between 1 and 4")
            elif menuopt==4:
                print("Exiting to Main Menu...")
                return True
            elif menuopt==1:
                buy_unit(field, game_vars,defender_dictionary)
                return
            elif menuopt==2:
                return
            elif menuopt==3:
                save_game()
            #elif menuopt==3
            #elif menuopt==4:
                

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")
    global field
    global game_vars
    global monster_dictionary
    global defender_dictionary
    while True:
        menuopt=input("Your choice?")
        try:
            int(menuopt)
        except ValueError as e:
            print('"{}"'.format(menuopt), "is not a number")
        else:
            menuopt=int(menuopt)
            if not (menuopt>=1 and menuopt<=4):
                print("Invalid Option")
            elif menuopt==1:
                print("starting new game")
                initialize_game()
                break
            elif menuopt==2:
                if "save.txt" in os.listdir():
                    print("Loading Saved Game.....")
                    field,game_vars,monster_dictionary,defender_dictionary=load_game()
                    print("Gmae Loaded")
                    break
            
                else:
                    print("You do not have any saved games")
            elif menuopt==3:
                print("Ending game, See you soon!")
                return "exit"
        
        
    
    

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    return True

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars,defender_dictionary):
    def getDefenders(defender_dictionary):
        defenderList=sorted(defender_dictionary)
        return defenderList
    
    def numToDefenderName(menuopt2,defenderList):
        defender_name=defenderList[menuopt2-1]
        return defender_name
    
    def checkGold(defender_name,defender_dictionary,game_vars):
        currentGold=game_vars["gold"]
        defenderPrice=defender_dictionary["{}".format(defender_name)]["price"]
        if currentGold>=defenderPrice:
            return "enoughGold"

    def computeplacement(string):
        letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        row=letters.index(string[:1])
        column=int(string[1:])-1
        
        return [row,column]
    def checkValid(pos,field):
        ###################################################################
        # This function checks if the position entered for the placement of tower is
        # Within the field or occupied with a monster or defender
        # Returns True if all conditions are satisfied to spawn the defender unit or if the player wants to replace a defender
        # Returns False if position is not valid or player does not want to replace a defender
        if pos[0]>len(field) and pos[0]<=0:
            print("Invalid Choice: ROW OUT OF RANGE")
            return False
        elif pos[1]>len(field[pos[0]]) and pos[0]>=0:
            print("Invalid Choice: COLUMN OUT OF RANGE")
            return False
        elif pos[1]<=0 and pos[1]>=3:
            print("Invalid Choice: CHOICE NOT WITHIN COLUMNS 1 TO 3")
            return False
        elif field[pos[0]][pos[1]]!=None:
            if field[pos[0]][pos[1]][2]=="defender_dictionary":
                print("There seems to be a tower already there, do you wish to replace it?")
                print("1. Yes\n2. No")
                while True:
                    opt=input("Your Choice: ")
                    try:
                        int(opt)
                    except ValueError as v:
                        print(opt, "is not a number... enter either 1 or 2")
                    else:
                        opt=int(opt)
                        if opt>2 or opt<1:
                            print(opt," is not valid, enter either 1 or 2")
                        elif opt==1:
                            return True
                        else:
                            return False
            elif field[pos[0]][pos[1]][2]=="monster_dictionary":
                print("Invalid Choice: There is an enemy on the grid")
                return False
        elif field[pos[0]][pos[1]]==None:
            return True
                
                
                
    #This function prints the prints out all the towers available for the player to buy
    def printSelection(defenderList,defender_dictionary):
        print("Which Unit do you wish to buy?")
        for i in range(len(defenderList)):
            if i==len(defenderList)-1:
                print("{:>1}. {:<2}".format(i+1,defenderList[i]))
            else:  
                print("{:<1}. {:<10}({:<1} gold)".format(i+1,defenderList[i].capitalize(),defender_dictionary["{}".format(defenderList[i])]["price"]))
    defenderList=getDefenders(defender_dictionary)
    defenderList.append("Don't buy")
    
      
    letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    printSelection(defenderList,defender_dictionary)
    while True:
        menuopt2=input("Your choice? ")
        try:
            int(menuopt2)
        except ValueError as e:
            print('"{}"'.format(menuopt2), "is not a number")
        else:
            menuopt2=int(menuopt2)
            if menuopt2==len(defenderList):
                return
            if menuopt2<1 or menuopt2>len(defenderList):
                print("Invalid Option")
            else:
                break
    

    
    defender_name=numToDefenderName(menuopt2,defenderList)
    
    if checkGold(defender_name,defender_dictionary,game_vars)=="enoughGold":
        # This function checks if the position entered for the placement of tower is
        # Within the field or occupied with a monster or defender
        # Returns True if all conditions are satisfied to spawn the defender unit or if the player wants to replace a defender
        # Returns False if position is not valid or player does not want to replace a defender
        
        while True:
            while True:
                menuopt3=input("Place where? ").lower() #prompts user
                if len(menuopt3)<2 or len(menuopt3)>2:# check that the input only has 2 characters
                    print("INVALID FORMAT: Enter ONLY 2 characters (Letter followed by number) ")
                    continue

                try:
                    int(menuopt3[1])#check if the second character is a number
                except ValueError:
                    print("INVALID FORMAT: Letter followed by number eg.a1/b2/c3 ")
                else:# if second character is a number
                    if not menuopt3[0].isalpha():# check if the first character is not an alphabet
                        print("INVALID FORMAT: Letter followed by number eg.a1/b2/c3")
                    else:# if the first charact is an alphabet
                        if int(menuopt3[1])>len(field[0]) or int(menuopt3[1])<=0:# check if the column chosen is out of range
                            print("Invalid Option: Column out of range")
                        else:             # if the column is not out of range,
                            Letters=["A","B","C","D","E"]
                            if menuopt3[0].upper() not in Letters:# check if the letter given for row is in range
                                print("Invalid Option: Row out of range")
                            else: #break the loop if the option is valid
                                break
                
            pos=computeplacement(menuopt3)
            Validity=checkValid(pos,field)
            if Validity==True:
                field[pos[0]][pos[1]]=[defender_name,defender_dictionary["{}".format(defender_name)]["maxHP"],"defender_dictionary"]
                game_vars["gold"]-=defender_dictionary["{}".format(defender_name)]["price"]
                break
            
            
            
            
            
    else:
        print("Insufficient Gold")
        print()
    
    

    
            
        
        
        
        ##########
    return

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(game_vars,field, defender_dictionary,monster_dictionary):
    # This function detects all the monsters on the same row as the defender
    def getEnemies(row):
        enemyList=[]
        for i in range(len(field[row])):  
            if field[row][i]!=None:
                if field[row][i][2]=="monster_dictionary":
                    enemyList.append([field[row][i][0],row,i])
        return enemyList
    #This function will do damage to the monster infront a given defender
    def doDmg(defender_name,defender_dictionary):
        minDmg=defender_dictionary["{}".format(defender_name)]["min_damage"] # gets the min damage of the defender
        maxDmg=defender_dictionary["{}".format(defender_name)]["max_damage"] # gets the max damage of the defender
        actualDmg=random.randint(minDmg,maxDmg+1) #randomises the damage of the defender that will be done
        if defender_name=="archer" and field[row][enemyList[0][2]][0]=="skeleton": # if the defender is an archer and the monster is a skeleton, it halfs the damage
            actualDmg/=2
            actualDmg=int(math.ceil(actualDmg/2))
            
        if enemyList==None or len(enemyList)==0: # if there is no enemy on the row, this function will not run
            return
        field[row][enemyList[0][2]][1]-=actualDmg # does damage to the monster that is closest to the city
        Letters="ABCDE"
        print(f"{defender_name.capitalize()} at {Letters[row]}{column+1} did {actualDmg} damage to {field[row][enemyList[0][2]][0]} at {Letters[enemyList[0][1]]}{enemyList[0][2]+1}")
    #checks if an enemy has died on that row and rewards the player
    def killOrNot(game_vars,row,enemyList):
        if enemyList==None or len(enemyList)==0:
            return
        monster_name=enemyList[0][0]
        if field[row][enemyList[0][2]][1]<=0:
            field[row][enemyList[0][2]]=None
            game_vars["gold"]+=monster_dictionary["{}".format(monster_name)]["reward"]# increases gold by the reward of the monster
            game_vars["threat"]+=monster_dictionary["{}".format(monster_name)]["reward"]# increases threat by the reward of the monster
            game_vars["monsters_killed"]+=1 #increases the number of monsters kills
            if game_vars["threat"]>=10:
                game_vars["threat"]-=10
                game_vars["maxMonsters"]+=1
                
                
    def endGameOrNot(game_vars):
        if game_vars["monsters_killed"]>=game_vars["monster_kill_target"]:
            return "reachedKillTarget"
        
        return
    for row in range(len(field)):
        for column in range(len(field[row])):
            if field[row][column]!=None:
                if field[row][column][0]=="mine":
                    continue
                if field[row][column][2]=="defender_dictionary":
                    defender_name=field[row][column][0]
                    enemyList=getEnemies(row)
                    if enemyList==[]:
                        continue
                    doDmg(defender_name,defender_dictionary)
                    killOrNot(game_vars,row,enemyList)
                    gameEndOrNot=endGameOrNot(game_vars)
                    if gameEndOrNot=="reachedKillTarget":
                        print("You have Won the Game!")
                        return True
                    

                    
                
                

    ###########################################################
    return

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(field):
    #does damage to the monster at a given row and column
    #row: the index of the row the monster is at
    #column: the index of the column the monster is at
    def doDmg(row,column):
        monster_name=field[row][column][0] #gets the name of the monster at the current position
        minDmg=monster_dictionary["{}".format(monster_name)]["min_damage"]# gets the min damage of the monster
        maxDmg=monster_dictionary["{}".format(monster_name)]["max_damage"]# gets the max damage of the monster
        actualDmg=random.randint(minDmg,maxDmg+1)# randomises the damage that will be done to the defender
        print("doing Damage to defender")
        field[row][column-1][1]-=actualDmg# does damage to the defender infront of the monster
    #checks if the defender has no health left after damage has been done to it, and deletes it off the field
    def killOrNot(row,column): 
        if field[row][column-1][1]<=0:
            field[row][column-1]=None
    # checks if the position infront of the mosnter is at the end of the row, if it is, the game will end
    def endGameOrNot(row,column):
        if column-currentMoves<0:
            return "end"
    # This function will activate when a monster steps on a mine
    # This is used along with getExplodedPositions()
    def explode(mine_row, mine_col, dmg = 10):
        #checks if the position is not off the map
        def validPosition(mine_row, mine_col):
            if mine_row < 0 or mine_row >= len(field):
                return False
            if mine_col < 0 or mine_col >= len(field[0]):
                return False
            return True
        #creates a list of all the positions around the mine that is on the map and not off the map
        def getExplodedPositions(mine_row, mine_col):
            global game_vars
            exploded_positions = [] 
            if validPosition(mine_row - 1, mine_col - 1):
                exploded_positions.append((mine_row - 1, mine_col - 1))
            if validPosition(mine_row - 1, mine_col):
                exploded_positions.append((mine_row - 1, mine_col))
            if validPosition(mine_row - 1, mine_col + 1):
                exploded_positions.append((mine_row - 1, mine_col + 1))
            if validPosition(mine_row, mine_col - 1):
                exploded_positions.append((mine_row, mine_col - 1))
            if validPosition(mine_row, mine_col):
                exploded_positions.append((mine_row, mine_col))
            if validPosition(mine_row, mine_col + 1):
                exploded_positions.append((mine_row, mine_col + 1))
            if validPosition(mine_row + 1, mine_col - 1):
                exploded_positions.append((mine_row + 1, mine_col - 1))
            if validPosition(mine_row + 1, mine_col):
                exploded_positions.append((mine_row + 1, mine_col))
            if validPosition(mine_row + 1, mine_col + 1):
                exploded_positions.append((mine_row + 1, mine_col + 1))
            return exploded_positions


        exploded_positions = getExplodedPositions(mine_row, mine_col) # gets all valid postions around the mind that is on the map
        for row,col in exploded_positions: # loops through each of the position in exploded_positions
            if field[row][col] is None: # checks if the position is None and will skip through the current iteration if it is
                continue
            if field[row][col][2] == "monster_dictionary":# if the position is not none, it checks if it is a monster and will do damage to it if it is
                currentHP = field[row][col][1] - dmg
                if currentHP<=0: #Checks if the monster has no health left and removes it from field if that is the case
                    game_vars["gold"]+=monster_dictionary["{}".format(field[row][col][0])]["reward"]#rewards the player with gold
                    game_vars["monsters_killed"]+=1#increases the number of monsters killed
                    game_vars["threat"]+=monster_dictionary["{}".format(field[row][col][0])]["reward"]#Increases the threat level
                    field[row][col] = None
                else: #if the monster has HP left, it will update the monster's HP on the field
                    field[row][col][1] =  currentHP
        
        field[mine_row][mine_col]=None #removes the mine off the field

    
    for row in range(len(field)):
        for column in range(len(field[row])):
            if field[row][column]!=None: # checks if the position has either a defender or a monster on it
                if field[row][column][2]=="monster_dictionary":##########     If the element in field is a monster then...
                    for i in range(1,monster_dictionary["{}".format(field[row][column][0])]["moves"]+1,1): #loops through the number of moves the monster can take
                        if field[row][column-i]!=None: # checks if the position infront of the monster is not empty, if it were to move
                            if field[row][column-i][2]=="monster_dictionary":#if the postion is not empty, checks if the position infront is a monster
                                if i==1:# if the monster is right infront of the monster about to be moved, the monster will not move
                                    currentMoves=0 #
                                else:
                                    currentMoves=i-1# if not, the number of grids the monster can move will be i-1
                                break
                            elif field[row][column-i][2]=="defender_dictionary":# if the row infront is a defender
                                if i==1:#if the defender is right infront of the monster about to be moved, the monster will not move
                                    if field[row][column-i][0]=="mine":# if the defender infront is a mine, the mine detonates
                                        explode(row, column-i, dmg = 10)
                                        currentMoves=0
                                        if field[row][column]==None:#checks if the monster has died, if it has died, the loop breaks
                                            break
                                    else:# if the defender infront is a regular defender, the monster will do damage to it
                                        currentMoves=0
                                        doDmg(row,column)#does damage to the defender
                                        killOrNot(row,column)#removes the defender if it has no health left after the monster did damage
                                    
                                else:
                                    currentMoves=i-1 # if the defender is not infront, the zombie moves
                                break
                        elif field[row][column-i]==None:
                            currentMoves=i
                    if currentMoves!=0: # if currentMoves is not equal to 0, the mosnter is moved by the value of currentMoves
                        endOrNot=endGameOrNot(row,column)#checks if the monster reached the city
                        if endOrNot=="end":
                            print("The Zombies have breached the city, game has ended")
                            return True
                        else:
                            field[row][column-currentMoves]=field[row][column]
                            field[row][column]=None
    return

            


#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------


def spawn_monster(field,game_vars, percentChanceToSpawn):
    # spawns a monster based on a probability
    def spawn(percentSpawn):
        percent = random.random()*100
        return percent<=percentSpawn
    #counts the number of monsters in the field 
    def countMonsters(field):
        noOfMonsters=0
        for row in range(len(field)):
            for column in range(len(field[row])):
                if field[row][column]!=None:
                    if field[row][column][2]=="monster_dictionary":
                        noOfMonsters+=1
        return noOfMonsters
    # Makes a list of numbers that correspond to a row in the field but in a shuffled form
    # This makes it so that when the program loops through the field, it will spawn monsters in random positions 
    #instead of starting from the first row
    def shufflefield(field):
        shuffledField=[]
        for i in range(len(field)):
            shuffledField.append(i)
        random.shuffle(shuffledField)
        return shuffledField
    
    noOfMonsters=countMonsters(field) #gets the number of monsters in the field
    shuffledField=shufflefield(field)# gets the list of the shuffled indexes of the field
    for pos in shuffledField: 
        if noOfMonsters>=game_vars["maxMonsters"]:# checks if the number of monsters if more than maxMonsters everytime it tries to spawn
            return field #breaks out of spawn_monster() if there is at max allowed amount
        if spawn(percentChanceToSpawn): # if spawn True, which is based on a percentage chance, it will move on to spawn
            monster=random.choice(list(monster_dictionary))# chooses a random monster in the monster dictionary to spawn
            if field[pos][-1]==None:# checks if the chosen position on the field is empty, else it will not attempt to spawn monster
                field[pos][-1]=[monster,monster_dictionary[monster]["maxHP"],"monster_dictionary",monster_dictionary[monster]["maxHP"]] #spawns the monster at the random row
                noOfMonsters+=1  #if a monster is spawned, it will update the number of monsters in noOfMonsters
                
    noOfMonsters=countMonsters(field) #counts the number of monsters again
    return field




#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
     with open("save.txt","w") as f:
        # store the field
        fieldString=""
        for row in range(len(field)):
            for column in range(len(field[row])):
                fieldString+="{}".format(field[row][column])
                if column!=len(field[row])-1:
                        fieldString+="@"
            if row!=len(field)-1:
                fieldString+=";"
        
        #Store the variables        
        variableString=""
        variableString+="{}".format(game_vars)
        
        #store the monster stats
        monster_dictionary_String="{}".format(monster_dictionary)
        #store the defender stats
        defender_dictionary_String="{}".format(defender_dictionary)
        
        
        #writes all the stats into the file
        f.write(fieldString+"\n")
        f.write(variableString+"\n")
        f.write(monster_dictionary_String+"\n")
        f.write(defender_dictionary_String)      
        print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game():
    #read all the lines in the file as f

    with open("save.txt","r") as f:
        lines=f.readlines()
    import ast
    
    #Get all the lines containing the data and store them into a unique String
    for i in range(len(lines)):
        lines[i]=lines[i].replace("\n","")
        if i==0:
            fieldString=lines[i]
        elif i==1:
            variableString=lines[i]
        elif i==2:
            monster_dictionary_String=lines[i]
        elif i==3:
            defender_dictionary_String=lines[i]
    #converts the fieldString into usable field 
    fieldString=fieldString.split(";")
    fieldString[0]=fieldString[0].split("@")
    fieldString[1]=fieldString[1].split("@")
    fieldString[2]=fieldString[2].split("@")
    fieldString[3]=fieldString[3].split("@")
    fieldString[4]=fieldString[4].split("@")
    for row in range(len(fieldString)):
        for column in range(len(fieldString[row])):
            if fieldString[row][column]=="None":
                fieldString[row][column]=None
            else:
                fieldString[row][column]=ast.literal_eval(fieldString[row][column])
    #Converts the game_var in string form into usable game_var dictionary         
    field=fieldString
    #Converts the game_var in string form into usable game_var dictionary
    game_vars=ast.literal_eval(variableString)
    #Converts the monster_dictionary in string form to usable dictionary
    monster_dictionary=ast.literal_eval(monster_dictionary_String)
    #Converts the defender_dictionary in string form to usable dictionary
    defender_dictionary=ast.literal_eval(defender_dictionary_String)

    
    return field,game_vars,monster_dictionary,defender_dictionary
#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 100000000000
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars["maxMonsters"] = 1
    game_vars["threat"]=0
    game_vars["danger_level"]=0
    for row in range(len(field)):
        for column in range(len(field[row])):
            field[row][column]=None
    
#-----------------------------------------------------
# update_field()
# 
#updates the field according to the position and health of the defenders
#and the zombies
def update_field():
    currentmonsters




def show_stats(game_vars):
    def makeThreatString(game_vars):
        ThreatString=""
        print("Threat is", game_vars["threat"])
        for i in range(game_vars["threat"]):
            ThreatString+="-"
        for i in range(10-game_vars["threat"]):
            ThreatString+=" "
        return "[{}]".format(ThreatString)
    ThreatString=makeThreatString(game_vars)
    turns=game_vars["turn"]
    gold=game_vars["gold"]
    monsters_killed=game_vars["monsters_killed"]
    killTarget=game_vars['monster_kill_target']
    danger_level=game_vars['danger_level']
    print("Turn {:^5} Threat = {:^15}  Danger Level {}".format(turns,ThreatString,danger_level+1))
    print("Gold = {}   Monsters Killed = {}/{}".format(gold,monsters_killed,killTarget))
    
#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

def main():
    print("Desperate Defenders")
    print("-------------------")
    print("Defend the city from undead monsters!")
    print()
    showMenu=True

    while True:
        if showMenu==True:
            showMenu=False
            exitOrNot=show_main_menu()
            if exitOrNot=="exit":
                break

        game_vars["turn"]+=1
        spawn_monster(field,game_vars, percentChanceToSpawn = SPAWN_CHANCE)
        draw_field(field,monster_dictionary,defender_dictionary)
        show_stats(game_vars)
        showMenu=show_combat_menu(field, game_vars,game_vars)
        if showMenu!=True:
            showMenu=defender_attack(game_vars,field, defender_dictionary,monster_dictionary)
            if showMenu!=True:
                showMenu=monster_advance(field)
        if game_vars["turn"]!=0 and game_vars["turn"]%12==0:
            game_vars["danger_level"]+=1
            print("Reached Turn 12, Danger Level increases...")
            for monster in monster_dictionary:

                monster_dictionary["{}".format(monster)]["maxHP"]+=1
                monster_dictionary["{}".format(monster)]["min_damage"]+=1
                monster_dictionary["{}".format(monster)]["max_damage"]+=1
                monster_dictionary["{}".format(monster)]["reward"]+=1
        game_vars["threat"]+=random.randint(1,game_vars["danger_level"]+1)
        game_vars["gold"]+=1
        if game_vars["threat"]>=10:
            game_vars["maxMonsters"]+=1
            game_vars["threat"]-=10

if __name__ == "__main__"   : 
    main()    
    
# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
    

