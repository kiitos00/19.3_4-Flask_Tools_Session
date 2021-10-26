from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "Nekohebi"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def survey_home():
    """start survey page"""
    return render_template("home.html", survey=satisfaction_survey)

@app.route('/start_survey', methods=['POST'])
def start_survey():
    """redirecting to questions"""
    return redirect('/questions/0')

@app.route('/questions/<int:qnum>')
def survey_questions(qnum):
    question = satisfaction_survey.questions[qnum]
    return render_template('questions.html', question=question, qnum=qnum, survey=satisfaction_survey)

# @app.route('/answer', method='POST')
# def answer():
