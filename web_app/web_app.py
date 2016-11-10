from flask import Flask, render_template, url_for, request
import re
from beer_model import Beer

app = Flask(__name__)

beer_array = []
menu_array = []
num_beers = 4

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home_page', methods=['GET','POST'])
def home_page(num_beers=num_beers, beer_array=beer_array):

    return render_template("landing.html", num_beers=num_beers, beer_array=beer_array)


@app.route('/beer', methods=['GET','POST'])
def beer_handler():

    num_beers = 0
    global beer_array
    beer_array = []

    for k in request.form:
        if 'beer' in k:
            beer_array.append(request.form[k])
            num_beers += 1

    return render_template("beer_choices.html", num_beers=num_beers, menu_array=menu_array)


@app.route('/rec', methods=['GET','POST'])
def rec():

    global menu_array
    menu_array = []
    for k in request.form:
        if 'beer' in k:
            menu_array.append(request.form[k])
    
    rec_beers = get_similar(beer_array, menu_array)

    return render_template("recommendation.html", rec_beers=rec_beers) 


def get_similar(beers, menu):
    
    m = []
    beer_list = []

    for beer in beers:
        if beer != '':
            for b in (Beer.select().where((Beer.beer_name.regexp(beer)) |
                     (Beer.brewery_name.regexp(beer)))):
                beer_list.append(b.beer_url)
    
    return beer_list

app.run(debug=True)
