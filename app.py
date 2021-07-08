from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

response = []
question_count = 0

@app.route("/")
def start():
    """ TODO """

    return render_template("survey_start.html",
                    survery_title = survey.title,
                    survey_instructions = survey.instructions)

@app.route("/begin", methods=["POST"])
def begin():
    """ TODO """

    print(request.form)
    return redirect("/questions/0")

@app.route("/questions/<int:question_count>")
def survey_question(question_count):
    """ TODO """

    return render_template("question.html", question = survey.questions[question_count], count=question_count+1)

# @app.route("/questions")
# def question_redirect(question_count):
#     """ TODO """

#     return redirect("question.html", question = survey.questions[question_count])

@app.route("/answer", methods=["POST"])
def next_question():
    """ TODO """
    # breakpoint()
    form_response = request.form["answer"]
    count = request.form["count"]
    response.append(form_response)

    if int(count) < len(survey.questions):
        return redirect(url_for(".survey_question", question_count=count))
    else:
        return redirect("/thank")

@app.route("/thank")
def thank_user():
    """ TODO """
    breakpoint()
    return render_template("completion.html")



