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
        try:
            file = request.files['myfile']
            file_content = file.read().decode()
            results = libs.get_data_from_whats(file_content.lower())
            this_insert = inputs.insert_one(results)
            
            return render_template(
                'display_result.html',
                results= results
            )
        except:
            return render_template('issue.html', issue="input")

    return redirect(url_for('home'))


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


@app.route('/delete_results/<input_id>')
def delete_results(input_id):
    inputs.remove({'_id': ObjectId(input_id)})
    flash("Your results were successfully deleted!")
    return redirect(url_for('home'))


@app.route('/consultdb', methods=['GET', 'POST'])
@app.route('/edit_results/consultdb', methods=['GET', 'POST'])
def consultdb():
    if request.method == 'POST':
        try:
            session_id = request.form["session_id"]
            the_input = inputs.find_one({'_id': ObjectId(session_id)})
            the_input_id = the_input["_id"]
            return render_template('display_result.html', results=the_input, the_input_id=the_input_id)
        except:
            return render_template('issue.html',
                                    issue="session_id",
                                    session_id=session_id)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
