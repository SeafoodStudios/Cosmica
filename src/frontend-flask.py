from flask import Flask, Response, redirect, request
from urllib.parse import unquote, quote
import requests
import ast
import random
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['Search']
        doc = nlp(query)
        search = []
        for token in doc:
            if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                search.append(str(token.text))
        if not search:
            search = query.split()
        return redirect("/search/" + str(quote(" ".join(search))))
    return '''
    <!DOCTYPE html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <html>
    <head>
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
    </body>
    </html>
    '''

@app.route('/search/<path:subpath>', methods=['GET'])
def search(subpath):
    userinput = unquote(subpath)
    data = requests.get("https://33bf-2607-fea8-84e3-f800-e8c5-75b2-40b2-f82d.ngrok-free.app/search/" + str(userinput.replace(" ", "-")))
    if str(data.text) == "[]":
        return Response(f"""<a href="https://cosmica.pythonanywhere.com/"> <img src="https://cosmica.pythonanywhere.com/logo.png" alt="Logo" width="200"> </a><br>""" + "No results, sorry!", mimetype='text/html')
    else:
        unparsedresults = ast.literal_eval(data.text)
        parsedresults = []
        for i in range(len(unparsedresults)):
            parsedresults.append("<a href=" + str(unparsedresults[i]["link"]) + ">" + str(unparsedresults[i]["link"]) + "</a>")
        random.shuffle(parsedresults)
        return Response(f"""<a href="https://cosmica.pythonanywhere.com/"> <img src="https://cosmica.pythonanywhere.com/logo.png" alt="Logo" width="200"> </a><br>""" + str("<br><br>".join(parsedresults[:10])), mimetype='text/html')
