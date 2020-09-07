import os
import io
import re
from os import path
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import libs

if path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)
inputs = mongo.db.inputs


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/consult')
def consult():
    return render_template('consult.html')


@app.route('/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')


@app.route('/global_words')
def global_words():
    global_results = libs.get_global_results(inputs)
    return render_template('global_words.html', global_results=global_results)


@app.route('/getfile', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':
        #try:
        file = request.files['myfile']
        user_ignored = request.form['ignored']

        if len(user_ignored) > 0:
            user_ignored = {
                "user_ignored": libs.process_ignored_words(user_ignored)
            }
            mongo.db.user_ignored.insert_one(user_ignored)

        file_content = file.read().decode()

        results = libs.get_data_from_whats(file_content.lower())
        this_insert = inputs.insert_one(results)
        return redirect(url_for('display_results', session_id=results['_id']))
        #except:
        return render_template('issue.html', issue="input")
    return redirect(url_for('home'))


@app.route('/edit_results/consultdb/<session_id>')
@app.route('/getfile/<session_id>')
def display_results(session_id):
    try:
        the_input = inputs.find_one({'_id': ObjectId(session_id)})
        the_input_id = the_input["_id"]
        return render_template('display_result.html',
                               results=the_input,
                               the_input_id=the_input_id)
    except:
        return render_template('issue.html',
                               issue="session_id",
                               session_id=session_id)


@app.route('/edit_results/<results_id>')
def edit_results(results_id):
    try:
        the_input = inputs.find_one({'_id': ObjectId(results_id)})
        return render_template('edit_results.html', input=the_input)
    except:
        return render_template('issue.html',
                               issue="session_id",
                               session_id=results_id)


@app.route('/delete_item/<input_id>/<item>')
def delete_item(input_id, item):
    inputs.update_one({'_id': ObjectId(input_id)}, {"$set": {item: ""}})
    flash("Your information was successfully removed!")
    return redirect(url_for('edit_results', results_id=input_id))


@app.route('/getfile/edit_participants/<input_id>', methods=['GET', 'POST'])
@app.route('/edit_results/edit_participants/<input_id>',
           methods=['GET', 'POST'])
def edit_participants(input_id):
    if request.method == 'POST':
        try:
            the_input = inputs.find_one({'_id': ObjectId(input_id)})
            participants = the_input['participants']

            for participant in participants:
                participant_to_change = request.form[str(participant)].lower()

                if len(participant_to_change
                       ) > 0 and participant_to_change != participant[0]:

                    # Links
                    links = the_input['links']
                    for link in links:
                        if link[0] == participant[0]:
                            new_link = [participant_to_change, link[1]]
                            links.insert(links.index(link), new_link)
                            links.remove(link)

                    # Media
                    medias = the_input['media']
                    for media in medias:
                        if media[0] == participant[0]:
                            new_media = [participant_to_change, media[1]]
                            medias.insert(medias.index(media), new_media)
                            medias.remove(media)

                    # Longest word
                    longest_dates = the_input['longest_word_dates']
                    if longest_dates[0][1] == participant[0]:
                        longest_dates = [[
                            longest_dates[0][0], participant_to_change
                        ]]
                        inputs.update_one(
                            {'_id': ObjectId(input_id)},
                            {"$set": {
                                "longest_word_dates": longest_dates,
                            }})
                        print("updated")
                        print(longest_dates)
                    else:
                        print(longest_dates)
                        print(participant)

                    # Participant Name
                    new_participant = [participant_to_change, participant[1]]
                    participants.insert(participants.index(participant),
                                        new_participant)
                    participants.remove(participant)

                    inputs.update_many({'_id': ObjectId(input_id)}, {
                        "$set": {
                            "media": medias,
                            "links": links,
                            "participants": participants
                        }
                    })

            url_rule = request.url_rule
            if 'getfile' in url_rule.rule:
                return redirect(url_for('display_results',
                                        session_id=input_id))
            else:
                return redirect(url_for('edit_results', results_id=input_id))

        except:
            return render_template('issue.html',
                                   issue="session_id",
                                   session_id=input_id)


@app.route('/delete_results/<input_id>')
def delete_results(input_id):
    inputs.remove({'_id': ObjectId(input_id)})
    flash("Your results were successfully deleted!")
    return redirect(url_for('home'))


@app.route('/consultdb', methods=['GET', 'POST'])
def consultdb():
    if request.method == 'POST':
        try:
            session_id = request.form["session_id"]
            the_input = inputs.find_one({'_id': ObjectId(session_id)})
            the_input_id = the_input["_id"]
            return redirect(url_for('display_results', session_id=session_id))
        except:
            return render_template('issue.html',
                                   issue="session_id",
                                   session_id=session_id)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
