from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses variable will go on to store all of the user's answers to the questions
responses = []

# when user goes to root route
# render page that shows show the title of the survey, instructions, and a button to start the survey
# button will be a link that directs the user to endpoint /questions/0

@app.route('/')
def render_intro():
    return render_template("survey_start.html", survey_title = survey.title, survey_instructions = survey.instructions)

# when user goes to /begin endpoint via a POST request
# redirect user to /questions/<len(responses)>

@app.route('/begin', methods=["POST"])
def redirect_to_question():
    return redirect("/questions/{len(responses)}")

# at the /questions/0/1/2/whatever endpoint
# render the template for the individual question, which
# displays just that question and its choices

@app.route("/questions/{len(responses)}")
def show_question():

    current_question = survey.questions[len(responses)]
    return render_template("question.html", question = current_question, choices = current_question.choices)