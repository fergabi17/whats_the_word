import os
import io
import re
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


import libs

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'whats_the_word'
# Create an environment variable to save this path
app.config["MONGO_URI"] = os.getenv(
    'MONGO_URI',
    'mongodb+srv://root:F3rnand4@myfirstcluster.g4xto.mongodb.net/whats_the_word?retryWrites=true&w=majority'
)

mongo = PyMongo(app)


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

    inputs = mongo.db.inputs
    count = inputs.find().count()
    return render_template('global_words.html', count=count)


@app.route('/getfile', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':
        try:
            file = request.files['myfile']
            file_content = file.read().decode()
            results = libs.get_data_from_whats(file_content.lower())

            inputs = mongo.db.inputs
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
    the_input = mongo.db.inputs.find_one({'_id': ObjectId(results_id)})
    #all_inputs = mongo.db.inputs.find()
    return render_template('edit_results.html', input=the_input)


@app.route('/delete_item/<input_id>/<item>')
def delete_item(input_id, item):
    inputs = mongo.db.inputs
    inputs.update_one({'_id': ObjectId(input_id)}, {"$set": {item: ""}})

    return redirect(url_for('edit_results', results_id=input_id))


@app.route('/delete_results/<input_id>')
def delete_results(input_id):
    mongo.db.inputs.remove({'_id': ObjectId(input_id)})
    return redirect(url_for('home'))


@app.route('/consultdb', methods=['GET', 'POST'])
def consultdb():
    if request.method == 'POST':
        session_id = request.form["session_id"]
        try:
            the_input = mongo.db.inputs.find_one({'_id': ObjectId(session_id)})
            return render_template('display_result.html', results=the_input)
        except:
            return render_template('issue.html',
                                   issue="session_id",
                                   session_id=session_id)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
