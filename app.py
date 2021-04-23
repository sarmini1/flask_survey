from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



# when user goes to root route
# render page that shows show the title of the survey, instructions, and a button to start the survey
# button will be a link that directs the user to endpoint /questions/0
@app.route('/')
def render_intro():
    """ Allows user to click button to start survey """
    return render_template("survey_start.html", survey_title = survey.title, survey_instructions = survey.instructions)


# when user goes to /begin endpoint via a POST request
# redirect user to /questions/<len(responses)>
# initializes responses in session
@app.route('/begin', methods=["POST"])
def redirect_to_question():
    """ redirects user to first question when they click begin """
    # responses variable will go on to store all of the user's answers to the questions
    session['responses'] = []
    return redirect("/questions/{len(session['responses'])}")


# checks to make sure we have not finished survey, then
# renders the template for the individual question, which
# displays just that question and its choices OR redirects
# to thank you page.
@app.route("/questions/{len(session['responses'])}")
def show_question():
    """ renders template for next question or redirects to
     end of survey if finished """
    if len(session['responses']) < len(survey.questions):
        current_question = survey.questions[len(session['responses'])]
        return render_template("question.html", 
                                question = current_question, 
                                choices = current_question.choices)
    else:
        return redirect("/completion")


# makes post request to endpoint of /answer and updates
# response list in the session
@app.route("/answer", methods=["POST"])
def store_answer():
    """ adds user response to question to session[responses]
        and redirects to next question """
    #breakpoint()
    response = session['responses']
    response.append(request.form["answer"])
    session['responses'] = response
    return redirect("/questions/{len(session['responses'])}")

    
# makes get request to endpoint of /completion and renders
# template to tell user thank you for completing survey.
@app.route("/completion")
def say_thanks():
    """ thanks user for completing survey """
    return render_template("completion.html")
