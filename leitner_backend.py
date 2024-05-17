import csv
import json
import os
import sys

#### ideas for improvement
#### - option to "flip" questions and answers

#### dropdowns for selecting files instead of typing

#### the option to import CSVs of flashcards

#### front end display

#### make it work on a


def main():

  print("Hello Friends! Welcome to the Leichter System Program!\n")

  user_settings_file_name = ""
  ### get the filename for the user_settings, keep looping until they enter one that exits
  while os.path.exists(user_settings_file_name) == False:
    print("What is the name of the file where your settings are stored?\n")
    ## see what csv files exist in our filepath
    current_directory = os.path.dirname(__file__)
    csv_files = [
        filename for filename in os.listdir(current_directory)
        if filename.endswith('.csv')
    ]
    ## display the available csvs
    print("CSV Files available: \n" + str(csv_files))

    user_settings_file_name = input(
        "Type the name of the user settings file you want to use (don't include .csv):\n"
    )

    user_settings_file_name += ".csv"

  cards_file_name = ""
  while os.path.exists(cards_file_name) == False:
    print(
        "\nWhat is the name of the file where your cards are kept? Files available : "
    )
    current_directory = os.path.dirname(__file__)
    json_files = [
        filename for filename in os.listdir(current_directory)
        if filename.endswith('.json')
    ]

    print(str(json_files))

    cards_file_name = input(
        "Enter the name of the file (don't include .json)\n")
    cards_file_name += ".json"

  active_Leitner_system = Leitner_system(cards_file_name,
                                         user_settings_file_name)

  if active_Leitner_system.current_day > 1:
    print("\nWelcome Back " + str(active_Leitner_system.username) + "!")
  else:
    print("\nWelcome to Day One! I hope you enjoy your studying journey!")

  #### main menu
  ###
  ####
  while (True):
    menu_selection = '!'
    while menu_selection not in (["1", "2", "3", "4", "q"]):
      menu_selection = input(
          "\nEnter a Number and Hit Enter:\n1.Start Today's Quiz\n2.Display Study Plan\n3.Edit User Settings\n4.Add or delete card\n(hit q to quit)\n"
      )

    ### first menu option is here to run the quiz
    if menu_selection == "1":
      print("\nToday is study day: " + str(active_Leitner_system.current_day) +
            " out of " + str(active_Leitner_system.plan_len_days) +
            " total days\n")

      study_plan_list = active_Leitner_system.study_plan
      todays_day = active_Leitner_system.current_day
      todays_boxes = study_plan_list[todays_day - 1]

      print("for today's session we are going to study these boxes: " +
            str(todays_boxes) + "\n")
      for current_box_num in todays_boxes:
        active_Leitner_system.run_quiz(current_box_num)

      input("Congrats! You're done with day: " +
            str(active_Leitner_system.current_day) +
            ", hit enter to move to tomorrow!")
      active_Leitner_system.current_day += 1

      if (active_Leitner_system.current_day
          > active_Leitner_system.plan_len_days):
        print(
            "Congrats, that was your last day! I hope you have learned a heap of info!"
        )
      else:
        print("Great! Come back tomorrow for day: " +
              str(active_Leitner_system.current_day))

        active_Leitner_system.user_settings[
            'username'] = active_Leitner_system.username
        active_Leitner_system.user_settings[
            'num_boxes'] = active_Leitner_system.num_boxes
        active_Leitner_system.user_settings[
            'plan_len_days'] = active_Leitner_system.plan_len_days
        active_Leitner_system.user_settings[
            'current_day'] = active_Leitner_system.current_day

        save_progress(active_Leitner_system.cardset,
                      active_Leitner_system.card_filename,
                      active_Leitner_system.user_settings,
                      active_Leitner_system.user_settings_filename)
        print("progress saved")
        ### then it should take us back to the main menu

    ## Option 2: display the study plan
    elif menu_selection == "2":
      study_plan = active_Leitner_system.study_plan

      for day_number, day in enumerate(study_plan, 1):
        print("On " + str(day_number) + " you will study boxes: " + str(day))
    ## now time to edit user settings
    elif menu_selection == "3":
      old_user_settings = active_Leitner_system.user_settings
      print("Current Username: " + str(old_user_settings['username']))

      ## set username
      new_username = input("New Username (or enter to leave the same): ")
      ## if they just hit enter
      if new_username.strip() == False:
        new_username = active_Leitner_system.username

      print("Current Number of Boxes: " + str(old_user_settings['num_boxes']))

      ## set number of boxes
      new_num_boxes = active_Leitner_system.num_boxes
      str_new_num_boxes = input(
          "New Number of Boxes (or hit enter to leave the same)")
      ## if they just hit enter
      if str_new_num_boxes.strip() == False:
        new_num_boxes = active_Leitner_system.num_boxes
        #### stopping place
      else:
        new_num_boxes = int(str_new_num_boxes)

      ## set plan number
      print("Current number of days in study plan: " +
            str(old_user_settings['plan_len_days']))
      str_new_plan_days = input(
          "Please input a new number of days, or hit enter to keep the same")

      if str_new_plan_days.strip() == False:
        new_plan_len_days = old_user_settings['plan_len_days']
      else:
        new_plan_len_days = int(str_new_plan_days)

      print("The current day is : " + str(old_user_settings['current_day']))

      str_new_current_day = input(
          "Please input a new current day or hit enter to leave it the same: ")

      if str_new_current_day.strip() == False:
        new_current_day = str(old_user_settings['current_day'])

      else:
        new_current_day = int(str_new_current_day)

      ## check to see if the file exists
      new_user_settings_filename = ""
      while os.path.exists(new_user_settings_filename) == False:
        current_directory = os.path.dirname(__file__)
        csv_files = [
            filename for filename in os.listdir(current_directory)
            if filename.endswith('.csv')
        ]
        print("Currently Available user save files")
        ## display the available csvs
        print("CSV Files available: \n" + str(csv_files))
        new_user_settings_filename = input(
            "Please enter the name of the csv file where you have your user settings stored (don't include csv)"
        )
        new_user_settings_filename += ".csv"

    ### now we need to put it all together and then save it to the CSV file
    ### new_username new_num_boxes new_plan_days new_current_day
      new_user_settings = {}
      new_user_settings['username'] = new_username
      new_user_settings['num_boxes'] = new_num_boxes
      new_user_settings['plan_len_days'] = new_plan_len_days
      new_user_settings['current_day'] = new_current_day
      set_user_settings(new_user_settings, new_user_settings_filename)
    ## Option 4: add cards
    elif menu_selection == "4":

      print("\nAdd/Delete Cards Mode: ")
      add_or_delete = "z"
      while add_or_delete != 'a' and add_or_delete != 'd':
        add_or_delete = input("Enter a for add or d for delete: \n")

      if add_or_delete == 'a':

        new_question = input("Enter a question for the new card: \n")
        new_answer = input("Enter a new answer for the new card: \n")
        new_card_box_location = int(
            input("Please enter which box to put your card into\n"))
        new_card_dic = {}
        new_card_dic['question'] = new_question
        new_card_dic['answer'] = new_answer
        new_card_dic['box_location'] = new_card_box_location

        active_Leitner_system.add_card(new_card_dic)

      elif add_or_delete == 'd':
        print(
            "Here is your cardset. Make note of the question on the card you want to delete"
        )
        print(str(active_Leitner_system.cardset))
        question_to_delete = input("What is the question you want to delete?")
        deleted_flag = False
        for card in active_Leitner_system.cardset:
          if card['question'] == question_to_delete:
            print("Diagnostic Print: Deleting" + str(card))
            deleted_flag = True
            active_Leitner_system.remove_card(card)
          else:
            print("Diagnostic Print: Card passed over for delete")
            continue

        if deleted_flag == True:
          print("Deleted Succesfully")
        else:
          print(
              "There was an issue deleting the card. Did you type the question exactly?"
          )

    elif menu_selection == "q":
      print("Thank you! Saving. . .\n")
      save_progress(active_Leitner_system.cardset,
                    active_Leitner_system.card_filename,
                    active_Leitner_system.user_settings,
                    active_Leitner_system.user_settings_filename)
      print("Progress Saved, closing . . .")
      sys.exit()

      ##


#########
#########
### PART TWO, ORGANZIZING THE FLASH CARDS
#########
##########

###things to think about
###
### Class
### Leitner_system is a( list of "boxes" of (lists of ("cards" aka dictionaries
## Leitner_system(list boxes (list cards(dic cards))
###
### Methods:
###

#o
# \_/\o
#( Oo)                    \|/
#(_=-)  .===O-  ~~Z~A~P~~ -O-
#/   \_/U'                /|\
#||  |_/
#\\  |
#{K ||
# | PP
# | ||
# (__\\


class Leitner_system:

  #@param self
  #@param cardset: a list of dicitonaries, each dictionary is a card
  #@param list boxes: a list boxes
  ## a box is a list of dictionaries
  ## the dictionaries in the box represent cards
  #@param dictionary user_settings

  def __init__(self, card_filename, user_settings_filename):
    ## import user settings
    self.card_filename = card_filename
    self.user_settings_filename = user_settings_filename

    self.user_settings = get_user_settings(self.user_settings_filename)
    self.username = self.user_settings['username']
    self.num_boxes = int(self.user_settings['num_boxes'])
    self.plan_len_days = int(self.user_settings['plan_len_days'])
    self.current_day = int(self.user_settings['current_day'])
    self.boxes_completed_today = int(
        self.user_settings['boxes_completed_today'])
    self.current_card = int(self.user_settings['current_card'])

    ## cardset is the full cardset, with data for sorting, but not sorted yet
    self.cardset = get_cards(self.card_filename)
    self.boxes = []
    ## set boxes to contain the number of boxes selected
    for _ in range(self.num_boxes):
      self.boxes.append([])
    ## now sort the cards into their boxes
    self.sort_cards_into_boxes()

    ## now let's build our study plan
    self.study_plan = self.create_study_plan()
    self.user_settings = get_user_settings(self.user_settings_filename)

  def sort_cards_into_boxes(self):
    self.boxes = []
    for _ in range(self.num_boxes):
      self.boxes.append([])
    ## each card is a dictionary
    for card in self.cardset:
      ## get the box location from the imported list of dictionarys
      box_location = card['box_location']
      ## the appropriate "box" is a list of cards
      appropriate_box = self.boxes[box_location - 1]
      ## add our card to that box
      appropriate_box.append(card)

  ## used to promote cards back one box
  def promote_card(self, card):

    old_box_location = card['box_location']
    card['box_location'] += 1
    new_box_location = old_box_location + 1

    ## if it's already in the last box, do nothing
    if old_box_location == self.num_boxes:
      return

    ## otherwise we want to put it one box ahead
    else:

      old_box = self.boxes[old_box_location - 1]
      new_box_location = old_box_location + 1
      new_box = self.boxes[new_box_location - 1]

      # Remove the card from the old box
      old_box.remove(card)

      # Append the card to the new box
      new_box.append(card)

      # Update the card's box location
      card['box_location'] = new_box_location

      ## we passed by reference, and we want the card we passed in to be accurate

  def demote_card_to_start(self, card):
    ## save the old box location so we can delete it
    old_box_location = card['box_location']
    ## add our card to the first box, remove from the old box
    if old_box_location > 1:
      self.boxes[old_box_location - 1].remove(card)
      self.boxes[0].append(card)
      card['box_location'] = 1
    ## if it's already in box 1 (index 0), then do nothing
    else:
      return

  ## returns a list where each index cooresponds to a day, and contains a list cooresponding to which boxes to study
  ## needs to repeat the highest number box every day
  ## needs to repeat the first box less often
  def create_study_plan(self):
    num_boxes = self.num_boxes
    num_days = self.plan_len_days

    ## populate our box schedule with blank lists
    box_schedule = []
    for _ in range(0, self.plan_len_days):
      box_schedule.append([])
    min_box_instances = 0
    box_numbers = []  ## decriment until it's all 0s

    ## sets min_box_instances, the total number of study sessions
    ## adds box number to our list of box numbers
    for box_num in range(1, num_boxes + 1):
      min_box_instances += box_num
      box_numbers.append(box_num)

    ## tested as [1,2,3,4,5]

    ## "Cramming" or more than one per day (too many boxes)
    ## if we have more box instances than days, we use up
    ## all instances and then we're done
    ## may end up with more than one box per day
    if min_box_instances > num_days:
      ## for each box number, generate priority number
      ## add it into our schedule ever priority_num days

      ## until we've assigned all of our instances
      boxes_left_to_assign = min_box_instances
      while boxes_left_to_assign > 0:

        for box_number in box_numbers:
          ## ever how_often days
          how_often = box_number
          for day in range(1, num_days + 1):
            ## if the box number is a multiple of the name
            if day % how_often == 0:
              ## add our current box number to that day
              box_schedule[day - 1].append(box_number)
              boxes_left_to_assign -= 1

    ## Taking our time mode (we have enough time for 1 box/day)
    ## if we have more days than instances, we do extra repetitions to fill all the days
    elif min_box_instances < num_days:
      ##until every day has at least one box to study (while there are empty indexes)
      while [] in box_schedule:
        for box_number in box_numbers:
          ## ever how_often days
          how_often = box_number
          for day in range(1, num_days + 1):
            ## if the box number is a multiple of the name
            if day % how_often == 0:
              ## add our current box number to that day
              box_schedule[day - 1].append(box_number)

    return box_schedule

  def run_quiz(self, box_number):
    current_box = self.boxes[box_number - 1]
    username = self.username

    print("Quiz for: " + username)
    print("Box Number: " + str(box_number) + "\n")

    for card in reversed(current_box):
      question = card['question']
      answer = card['answer']
      print("Question: " + question)
      input("Press Enter to reveal Answer")
      print("Answer: " + answer)

      answered_correctly = '!'
      while answered_correctly != 'c' and answered_correctly != 'i':
        answered_correctly = input(
            "was your answer correct 'c' or incorrect 'i'?")

      if answered_correctly == 'i':
        self.demote_card_to_start(card)
      else:
        self.promote_card(card)
      ## incriment current day, so next time we're on the next day
      #print("diagnostic print: " + str(self.boxes))

  def add_card(self, card):

    add_card(card, self.cardset,
             self.card_filename)  ## uses are add card crud function
    box_location = card['box_location']
    self.boxes[box_location - 1].append(card)

  def remove_card(self, card):
    delete_card(card, self.cardset, self.card_filename)
    self.sort_cards_into_boxes()

  #########
  #
  #
  # ests


def tests_1():
  ## test mode

  user_settings_csv_name = "user_settings"
  input("setting settings to user_settings.csv")

  user_settings_dic = {}
  file_path = user_settings_csv_name + ".csv"
  user_settings_dic = get_user_settings(user_settings_dic, file_path)

  print(str(user_settings_dic))

  print(str("checking the set_user_settings function"))

  set_user_settings(
      {
          'username': 'Joey',
          'num_boxes': 10,
          'plan_len_days': 999,
          'current_day': 676
      }, "user_settings.csv")

  ready_to_continue = ""
  while (ready_to_continue != "r"):
    ready_to_continue = str(
        input("check it changed properly. Type r to reset back to robert: "))

  set_user_settings(
      {
          'username': 'Robert',
          'num_boxes': 5,
          'plan_len_days': 30,
          'current_day': 5
      }, "user_settings.csv")

  print("Now checking the get_cards() funciton\n")
  print("importing flashcards.json")
  filename = "flashcards.json"
  print("succesfully imported\n ")
  print(str(get_cards(filename)))

  ### testing the add_card funciton

  print("\nnow testing the add_card() function")
  print("question: guess what?, answer: chicken butt, box: 1")
  card = {
      'question': 'guess what',
      'answer': 'chicken butt',
      'box_location': 1
  }
  cardset = get_cards("flashcards.json")

  user_input = ""
  while user_input != "a":
    user_input = input("check the before picture, then hit 'a' to continue: ")
    ## add the card to the cardset
  add_card(card, cardset, "flashcards.json")  ## card, cardset, filename
  print("now look at the json to verify that we have chicken butt \n")

  ## now test delete card

  print("Now to test delete card")

  user_input = ""
  while user_input != "d":
    user_input = input("check the before picture, then hit 'd' to continue: ")
  print("deleting chicken butt")
  print(". . . ")

  delete_card(card, cardset, "flashcards.json")
  print("Now check the JSON to verify")

  ### testing our Leitner System Class

  ## initialize our leitner system

  test_Leitner_system = Leitner_system(cardset, user_settings_dic,
                                       "flashcards_1.json",
                                       "user_settings.csv")

  print("Leitner System Created Succesfully \n")

  print("username: " + str(test_Leitner_system.username))
  print("number of boxes: " + str(test_Leitner_system.num_boxes))
  print("number of days in study plan: " +
        str(test_Leitner_system.plan_len_days))
  print("current day: " + str(test_Leitner_system.current_day))

  print("\nTesting sorting into cards . . .")
  test_Leitner_system.sort_cards_into_boxes()

  card_to_promote = {
      'question': 'When does the narwal bacon',
      'answer': 'midnight',
      'box_location': 1
  }

  print("\nCurrent cardset")
  print(str(test_Leitner_system.cardset))
  print("\nadd the card")
  test_Leitner_system.add_card(card_to_promote)
  print(str(test_Leitner_system.cardset))
  print("\npromote the card")
  test_Leitner_system.promote_card(card_to_promote)
  print("\nHere are our boxes")
  print(str(test_Leitner_system.boxes))

  print("Verify if that looks okay... Moving on...")

  print("\nWe're gonna promote that last card twice then demote to start")
  print("boxes before we double promote:")
  print(str(test_Leitner_system.boxes))
  print("promote process for one card")
  test_Leitner_system.promote_card(card_to_promote)
  print("boxes after two promotes")
  test_Leitner_system.promote_card(card_to_promote)

  print("boxes after promoted twice: ")
  print(str(test_Leitner_system.boxes))

  print("now let's see if we can demote succesfully")
  test_Leitner_system.demote_card_to_start(card_to_promote)
  print(str(test_Leitner_system.boxes))
  print("Now that card should demote to the start")
  print(str(test_Leitner_system.cardset))
  print("Now we're going to see if we can remove it")
  test_Leitner_system.remove_card(card_to_promote)
  print(str(test_Leitner_system.boxes))
  print("should be removed now")

  print("Now lets test to see if the quiz works")
  test_Leitner_system.run_quiz("1")


### Still need to test for
#def build_study_plan
#def quiz
#def
#def
#def


def tests_2():
  print("Welcome to tests part 2")
  test_Leitner_system = Leitner_system("flashcards_1.json",
                                       "user_settings.csv")
  print("now let's check the schedule builder")
  test_Leitner_system.create_study_plan()
  print(str(test_Leitner_system.study_plan))


def tests_3():
  print("now let's test the quiz section")
  print("Starting with box 1")
  test_Leitner_system = Leitner_system("flashcards_1.json",
                                       "user_settings.csv")
  ## test running the quiz for box 1
  test_Leitner_system.run_quiz(1)


#  ___
# ___/   \___
#/   '---'   \
#'--_______--'
#     / \
#    /   \
#    /\O/\
#    / | \
#    // \\
# Help! Help!

#########
#########
### PART ONE, THE CRUD SYSTEM
#########
##########

### update card is going to be to add a new
#def add_card():

###
#def delete_card():


# returns user settings as a dictionary
# @param {dictionary} user_settings_dic is an empty dictionary, which will be filled with user data
# @ is a string, the name of the file
def get_user_settings(filepath):

  ## Open the filepath in read mode
  user_settings_dic = {}
  with open(filepath, 'r', newline="\n") as user_settings:
    ## defaults to fieldnames in the first row
    reader = csv.DictReader(user_settings)
    ## keeping track of line count to separate labels and settings
    ## each row comes out as a dictionary

    username, num_boxes, plan_len_days, current_day, boxes_completed_today, current_card = "", "", "", "", "", ""

    row_count = 0
    for row in reader:
      if row_count == 0:
        ## if we're on the first line save the column names
        username = row['username']
        num_boxes = row['num_boxes']
        plan_len_days = row['plan_len_days']
        current_day = row['current_day']
        boxes_completed_today = row['boxes_completed_today']
        current_card = row['current_card']

        row_count += 1
      else:
        break

      user_settings_dic = {
          'username': username,
          'num_boxes': num_boxes,
          'plan_len_days': plan_len_days,
          'current_day': current_day,
          'boxes_completed_today': boxes_completed_today,
          'current_card': current_card
      }

    return user_settings_dic


## should recieve a dictionary new_user_settings and a filepath, and write the new settings to the filepath
def set_user_settings(new_user_settings, filepath):

  field_names = list(new_user_settings.keys())

  with open(filepath, 'w', newline="\n") as user_settings_csv:
    # create the writer
    writer = csv.DictWriter(user_settings_csv, fieldnames=field_names)
    writer.writeheader()
    writer.writerow(new_user_settings)

  print("User Settings Saved")


## returns a list of dictionaries with all the cards
## @filename str: the .json file
def get_cards(filename):
  with open(filename, 'r') as file:
    data = json.load(file)
  ## returns a list of dictionaries, each dictionary is a card
  return data


# takes the cardset, adds the card to it, and writes to the JSON
# @param {dictionary} card: contains a dicitonary with all card info
# @param {list} cardset:list of dicitonaries with all cards
# @param {string} filepath: the name of the JSON incl .json
def add_card(card, cardset, filename):
  ## append our card to the cardset
  cardset.append(card)
  ## since it was passed by reference, it should affect "cardset" outside the function
  with open(filename, 'w') as file:
    json.dump(cardset, file, indent=4)


##
def delete_card(card, cardset, filename):
  cardset.remove(card)
  with open(filename, 'w') as file:
    json.dump(cardset, file, indent=4)


def save_progress(cardset, cardset_filename, user_settings,
                  user_settings_filename):
  ## clear out user settings csv
  with open(user_settings_filename, 'w') as file:
    pass

  ### write our user settings to the CSV
  set_user_settings(user_settings, user_settings_filename)

  ### clear out the current cardset JSON
  with open(cardset_filename, 'w') as file:
    pass
  ### write our cardset to the JSON
  with open(cardset_filename, 'w') as file:
    json.dump(cardset, file, indent=4)


##main()

### uncomment to run the unit tests
#tests_3()
#input("Hit enter to continue to tests_2")
#tests_2()
#input("Hit enter to continue to tests_1")
#tests_1()
