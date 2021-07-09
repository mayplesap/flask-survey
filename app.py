from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def start():
    """ Starting page of survey. """

    session["response"] = []

    return render_template("survey_start.html",
                            survery_title = survey.title,
                            survey_instructions = survey.instructions)

@app.route("/begin", methods=["POST"])
def begin():
    """ Clicking on continue button will redirect to survey_question. """

    return redirect("/questions/0")

@app.route("/questions/<int:question_count>")
def survey_question(question_count):
    """ Generate page for the survey questions.
        If not yet answered a question and try to change url, will redirect to correct question.
        If finished survey and tries to go back to a question, will redirect to /thanks """

    question_num = len(session["response"])

    if question_num == len(survey.questions):
        return redirect("/thanks")
    elif question_count == question_num :
        return render_template("question.html", 
                                question = survey.questions[question_num])
    else:
        flash("You are trying to access an invalid question")
        return redirect(f"/questions/{question_num}")
    # return redirect(url_for(".survey_question", question_count = question_num))

@app.route("/answer", methods=["POST"])
def next_question():
    """ Appends question answer to response and 
        redirects user to next question or thank you page. """

    form_response = request.form["answer"]

    response = session["response"]
    response.append(form_response)
    session["response"] = response
    
    question_num = len(session["response"])

    return redirect(f"/questions/{question_num}")


@app.route("/thanks")
def thank_user():
    """ Generates completion.html and thanks the use for completing survey """

    return render_template("completion.html")



