from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

# 443-836-295

app = Flask(__name__)
app.config['SECRET_KEY'] = "Nekohebi"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

answers = "Responses"


@app.route('/')
def survey_home():
    """start survey page"""
    return render_template("home.html", survey=satisfaction_survey)


@app.route('/start_survey', methods=['POST'])
def start_survey():
    """redirecting to questions"""
    session[answers] = []
    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def answer():
    """get the answer from questions route for each questions and send to next question"""

    # get the selected answer(option) from question page
    choice = request.form['answer']

    # save the answer in the session as list
    responses = session[answers]
    responses.append(choice)
    session[answers] = responses

    # if all questions are answered, go to complete. Otherwise, send to next question.
    if (len(answers) == len(satisfaction_survey.questions)):
        return redirect('/complete_survey')
    else:
        return redirect(f'/questions/{len(answers)}')


@app.route('/questions/<int:qnum>')
def survey_questions(qnum):

    res = session[answers]
    
    if (res == None):
        # If there is no answer made, go back to home
        return redirect("/")

    if (len(res) != qnum):
        # If the questions number and answered response length is not matched, go back to home with error
        flash('Error: Please answer this question first')
        print(res)
        return redirect(f'/questions/{len(res)}')

    if (len(res) == len(satisfaction_survey.questions)):
        # If the answered repsponces are equal to max number of questions, reditect to the complete page
        return redirect("/complete_survey")

    else:
        # If there is no issue and need to conitue survey
        questions = satisfaction_survey.questions[qnum]
        return render_template('questions.html', questions=questions, qnum=qnum, survey=satisfaction_survey)


@app.route('/complete_survey')
def survey_complete():
    return render_template('done.html')
