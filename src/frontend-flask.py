from flask import Flask, Response, redirect, request
from markupsafe import escape
from urllib.parse import unquote, quote
import requests
import ast
import random
import time
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="API_KEY")

global then
then = time.time()
global now
now = time.time()
global ai_limit
ai_limit = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['Search']
        search = query.split()
        return redirect("/search/" + str(quote(" ".join(search))))
    return '''
    <!DOCTYPE html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <html>
    <head>
    <title>Cosmica Search Engine</title>
    <style>
    body, html {
      height: 100%;
      margin: 0;
    }

    .center {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100%;
      text-align: center;
    }

    input {
      margin: 0px 0 0 0;
    }
    img {
      margin: 0;
    }
    </style>
    </head>
    <body>
    <div class="center">
    <img src="https://cosmica.pythonanywhere.com/logo.png" alt="Logo for Cosmica" width="200">
        <form method="post">
            <input type="text" name="Search" placeholder="Search the universe!">
            <input type="submit" value="Search">
        </form>
    </div>
    <a href="https://www.producthunt.com/products/cosmica?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-cosmica" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=974665&theme=neutral&t=1749324211335" alt="Cosmica - Data&#0032;privacy&#0032;and&#0032;non&#0032;big&#0032;tech&#0032;focused&#0032;search&#0032;engine&#0046; | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
    </body>
    </html>
    '''

@app.route('/search/<path:subpath>', methods=['GET'])
def search(subpath):
    global ai_limit
    global then
    global now
    userinput = unquote(subpath)
    data = requests.get("https://33bf-2607-fea8-84e3-f800-e8c5-75b2-40b2-f82d.ngrok-free.app/search/" + str(userinput.replace(" ", "-")))
    if str(data.text) == "[]":
        now = time.time()
        if (now - then) >= 60:
            ai_limit = 0
            then = now

        if ai_limit < 10:
            ai_limit += 1
            completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": str(userinput)}]
            )
            aioutput = str(completion.choices[0].message.content)
            return Response(f"""<title>Cosmica Search Engine</title><a href="https://cosmica.pythonanywhere.com/"> <img src="https://cosmica.pythonanywhere.com/logo.png" alt="Logo" width="200"> </a><br>""" + f"""Looks like the universe couldn't find what you were looking for. Instead, we'll have the help of an alien to help you!<br><br><div style="white-space: pre-wrap; word-wrap: break-word; max-width: 100%; overflow-wrap: break-word;">""" + aioutput + "</div>", mimetype='text/html')
        else:
            return Response(f"""<title>Cosmica Search Engine</title><a href="https://cosmica.pythonanywhere.com/"> <img src="https://cosmica.pythonanywhere.com/logo.png" alt="Logo" width="200"> </a><br>""" + "No results, sorry! Space can be quite lonely sometimes, but eventually, you'll find something.", mimetype='text/html')
    else:
        unparsedresults = ast.literal_eval(data.text)
        parsedresults = []
        for i in range(len(unparsedresults)):
            parsedresults.append("<a href=" + str(unparsedresults[i]["link"]) + ">" + str(unparsedresults[i]["link"]) + "</a>")
        random.shuffle(parsedresults)
        return Response(f"""<title>Cosmica Search Engine</title><a href="https://cosmica.pythonanywhere.com/"> <img src="https://cosmica.pythonanywhere.com/logo.png" alt="Logo" width="200"> </a><br>""" + str("<br><br>".join(parsedresults[:10])), mimetype='text/html')
