from flask import Flask, render_template, url_for, request
import re

from beer_model import Beer
from similarity_matrix import SimilarityVector

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
    requested_beers = []
    clarity_array = []

    for k in request.form:
        if 'beer' in k:
            beer = request.form[k]
            if beer != '':
                bselect = (Beer.select().where((Beer.beer_name.regexp(beer)) |
                                               (Beer.brewery_name.regexp(beer))))
                if len(bselect) > 1:
                    l = []
                    for b in bselect:
                        l.append(b.beer_name)
                    
                    requested_beers.append(beer) 
                    clarity_array.append(l)
                else:
                    beer_array.append(request.form[k])
                    num_beers += 1
                                                   

    print(clarity_array)
    if len(clarity_array) > 0:
        return render_template("clarify.html", clarity_array=clarity_array,requested_beers=requested_beers) 

    return render_template("beer_choices.html", num_beers=num_beers, menu_array=menu_array)


@app.route('/clarified', methods=['GET','POST'])
def clarified():
    
    print(request.form)
    return render_template("beer_choices.html", num_beers=num_beers, menu_array=menu_array)


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")


@app.route('/verify_login', methods=['POST','GET'])
def verify_login():
    return render_template("landing.html", num_beers=num_beers, beer_array=beer_array)


@app.route('/rec', methods=['GET','POST'])
def rec():

    global menu_array
    menu_array = []
    for k in request.form:
        if 'beer' in k:
            menu_array.append(request.form[k])
    
    rec_beers = get_similar(beer_array, menu_array)
    print(rec_beers)

    return render_template("recommendation.html", rec_beers=rec_beers) 


def get_similar(beers, menu):


    """    beers_summed = dists[2][choices].apply(lambda row: np.sum(row), axis=1)
    beers_summed = beers_summed.sort_values(ascending=False)
    ranked_beers = beers_summed.index[beers_summed.index.isin(choices)==False]
    ranked_beers = ranked_beers.tolist()
    ranked_beers[2][1]
    """
    
    beer_vecs = []
    choice_indices = []

    for beer in beers:
        if beer != '':
            for b in (Beer.select().where((Beer.beer_name.regexp(beer)) |
                     (Beer.brewery_name.regexp(beer)))):
                print(b.beer_name)
                for s in (SimilarityVector.select().where(
                                        SimilarityVector.beer_url == b.beer_url)):
                    beer_vecs.append(s.sim_vec)

    for beer in menu:
        if beer != '':
            for b in (Beer.select().where((Beer.beer_name.regexp(beer)) |
                     (Beer.brewery_name.regexp(beer)))):

                print(b.beer_name)
                for s in (SimilarityVector.select().where(
                                        SimilarityVector.beer_url == b.beer_url)):
                    choice_indices.append(s.id)
            

    print(beer_vecs,choice_indices)
    
    return beer_vecs

app.run(debug=True)
