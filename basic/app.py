from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSE_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'never-tell'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_survey_start():
    """"select a survey"""

    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=['POST'])
def start_survey():
    """clear the session of responses"""

    session[RESPONSE_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    """save response and redirect to next question"""

    choice = request.form['answer']

    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    else:
        return redirect(f'/questions/{len(responses)}')
    

@app.route('/questions/<int:qid>')
def show_question(qid):
    """display current question"""
    responses = session.get(RESPONSE_KEY)

    if(responses is None):
        return redirect('/')
    
    if(len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    if(len(responses) != qid):
        flash(f'invalid question id: {qid}')
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)

@app.route('/complete')
def complete():
    """survey complete. show completion page"""

    return render_template('completion.html')