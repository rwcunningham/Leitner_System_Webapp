from flask import Flask, request, render_template, url_for, redirect
import leitner_backend
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        print("name sent to submit: " + name)
        ## redirects to the "def submit"
        return redirect(url_for('submit', name=name))

    ## if request == 'GET' (when the user first loads the page)
    return render_template('index.html')


## url_for from def index() is going to pass "name"
##
@app.route('/submit', methods=['GET', 'POST'])
def submit():

    if request.method == 'POST':
        name = request.form['name']
        print("name recieved by to submit() (post): " + name)
        username = request.form['username']
        flashcard_set = request.form['flashcard_set']

        return redirect(
            url_for('main_menu',
                    username=username,
                    flashcard_set=flashcard_set,
                    name=name))

    name = request.args.get('name')
    print("name recieved by to submit() (get): " + name)
    ## method = GET (when user first loads the page)
    current_directory = os.path.dirname(__file__)
    json_files = [
        filename for filename in os.listdir(current_directory)
        if filename.endswith('.json')
    ]

    csv_files = [
        filename for filename in os.listdir(current_directory)
        if filename.endswith('.csv')
    ]
    return render_template('submit.html',
                           name=name,
                           json_files=json_files,
                           csv_files=csv_files)


@app.route('/main_menu', methods=["POST", "GET"])
def main_menu():
    name = request.args.get('name')
    flashcard_set = request.args.get('flashcard_set')
    username = request.args.get('username')

    if request.method == "POST":
        flashcard_set = request.form['flashcard_set']
        username = request.form['username']
        name = request.form['name']
        print("username passed to front of card: " + username)
        return url_for('run_quiz',
                       name=name,
                       username=username,
                       flashcard_set=flashcard_set)

    return render_template('main_menu.html',
                           username=username,
                           flashcard_set=flashcard_set,
                           name=name)


@app.route('/run_quiz', methods=["POST", "GET"])
def run_quiz():

    ## redirect to front of card on top of the boxes stack
    if request.method == "POST":
        username = request.form['username']
        flashcard_set = request.form['flashcard_set']
        name = request.form['name']
        return redirect(
            url_for('front_card',
                    username=username,
                    flashcard_set=flashcard_set,
                    name=name))
    ## this is just going to be a welcome screen

    ## get the current box
    username = request.args.get('username')
    flashcard_set = request.args.get('flashcard_set')
    name = request.args.get('name')

    current_leitner_system = leitner_backend.Leitner_system(
        flashcard_set, username)

    current_box_num = current_leitner_system.study_plan[
        current_leitner_system.current_day -
        1][current_leitner_system.boxes_completed_today]

    todays_boxes = current_leitner_system.study_plan[
        current_leitner_system.current_day - 1]

    return render_template('run_quiz.html',
                           username=username,
                           flashcard_set=flashcard_set,
                           name=name,
                           current_leitner_system=current_leitner_system,
                           current_box_num=current_box_num,
                           todays_boxes=todays_boxes)

    #current_leitner_system=current_leitner_system,
    #current_box_num=current_box_num)


@app.route('/front_card', methods=['GET', 'POST'])
def front_card():

    if request.method == "POST":
        username = request.form['username']
        flashcard_set = request.form['flashcard_set']
        name = request.form['name']
        current_card = request.form['current_card']
        current_box = request.form['current_box']
        return redirect(
            url_for('back_card',
                    username=username,
                    flashcard_set=flashcard_set,
                    name=name,
                    current_card=current_card,
                    current_box=current_box))

    username = request.args.get('username')
    flashcard_set = request.args.get('flashcard_set')
    name = request.args.get('name')

    current_leitner_system = leitner_backend.Leitner_system(
        flashcard_set, username)

    todays_boxes = current_leitner_system.study_plan[
        current_leitner_system.current_day - 1]
    num_boxes_today = len(todays_boxes)
    boxes_completed_today = current_leitner_system.boxes_completed_today
    current_card = current_leitner_system.current_card
    current_box = todays_boxes[boxes_completed_today]

    ## if we've completed our boxes for the day, move to the next day
    if boxes_completed_today == num_boxes_today:
        current_leitner_system.current_day += 1
        leitner_backend.save_progress(
            current_leitner_system.cardset,
            current_leitner_system.card_filename,
            current_leitner_system.user_settings,
            current_leitner_system.user_settings_filename)

    ## fetch the text from the JSON
    ## figure out which

    return render_template('front_card.html',
                           username=username,
                           flashcard_set=flashcard_set,
                           name=name,
                           current_leitner_system=current_leitner_system,
                           current_box=current_box,
                           current_card=current_card)


@app.route('/back_card', methods=['GET', 'POST'])
def back_card():

    ### put the POST section here
    if request.method == "POST":
        username = request.form['username']
        flashcard_set = request.form['flashcard_set']
        name = request.form['name']
        correct = request.form['correct']
        current_card = int(request.form['current_card'])
        current_box = int(request.form['current_box'])

        if correct == "true":
            ## reconstruct the leitner system
            current_leitner_system = leitner_backend.Leitner_system(
                flashcard_set, username)

            ## promote our card
            print("promoting this card: " +
                  str(current_leitner_system.boxes[current_box -
                                                   1][current_card]))
            current_leitner_system.promote_card(
                current_leitner_system.boxes[current_box - 1][current_card])

            leitner_backend.save_progress(current_leitner_system.cardset,
                                          flashcard_set,
                                          current_leitner_system.user_settings,
                                          username)

            ## if we got it right, don't increase current card? Our list will be one shorter

            current_leitner_system.user_settings['current_card'] = str(
                current_leitner_system.current_card)
            print("Current Card in system: " +
                  str(current_leitner_system.current_card))
            print("Current Card in settings (before write to csv): " +
                  str(current_leitner_system.user_settings['current_card']))

            ## if we're at the end of the box, increase boxes completed today
            print("Current card vs size of box: " +
                  str(current_leitner_system.current_card) + " vs " +
                  str(len(current_leitner_system.boxes[current_box - 1])))

            if current_leitner_system.current_card >= (len(
                    current_leitner_system.boxes[current_box - 1])):

                current_leitner_system.boxes_completed_today += 1
                current_leitner_system.current_card = 0
                current_leitner_system.user_settings['current_card'] = 0
                current_box += 1
                current_card = 0

                ## now, if boxes completed today is more than the                    boxes in the study plan for today, advance                     the day
                print("boxes completed today: " +
                      str(current_leitner_system.boxes_completed_today) +
                      "number of boxes today" + str(
                          len(current_leitner_system.study_plan[
                              current_leitner_system.current_day])))

                if current_leitner_system.boxes_completed_today >= len(
                        current_leitner_system.study_plan[
                            current_leitner_system.current_day]):

                    current_leitner_system.current_day += 1
                    current_leitner_system.boxes_completed_today = 0
                    current_box = 1
                    current_card = 0

            ## save our progress to the save files
            leitner_backend.save_progress(current_leitner_system.cardset,
                                          flashcard_set,
                                          current_leitner_system.user_settings,
                                          username)

            ## back to front of card
            print("current box is : " + str(current_box))
            print("current day is: " + str(current_leitner_system.current_day))
            return redirect(
                url_for('front_card',
                        username=username,
                        flashcard_set=flashcard_set,
                        name=name,
                        current_box=current_box))
        else:
            return

    name = request.args.get('name')
    username = request.args.get('username')
    flashcard_set = request.args.get('flashcard_set')
    print("Going to back of the card, username and flashcard set: " +
          username + " " + flashcard_set)
    current_leitner_system = leitner_backend.Leitner_system(
        flashcard_set, username)
    current_box = int(request.args.get('current_box'))
    current_card = int(request.args.get('current_card'))

    return render_template('back_card.html',
                           username=username,
                           flashcard_set=flashcard_set,
                           name=name,
                           current_leitner_system=current_leitner_system,
                           current_box=current_box,
                           current_card=current_card)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
