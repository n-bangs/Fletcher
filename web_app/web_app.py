from flask import Flask, render_template, url_for, request
import numpy as np
from pymongo import MongoClient
import operator
from bson.objectid import ObjectId
import json
import re

from beer_model import Beer

app = Flask(__name__)

client = MongoClient()
db = client.sim_vecs
col = db.vectors


f = open('url_dict.json')
url_dict = json.loads(f.read())

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
    rec_beers = [r[0] for r in rec_beers]

    return render_template("recommendation.html", rec_beers=rec_beers) 


def get_similar(beers, menu):

    beer_list = []
    menu_list = []
    beer_vecs = []
    sub_list = []
    sub_beer_vecs = []

    for beer in menu:
        print(beer)
        if beer != '':
            for b in (Beer.select().where((Beer.beer_name.regexp(beer)) |
                     (Beer.brewery_name.regexp(beer)))):
                print(b.beer_url)
                try:
                    for v in col.find({'_id':ObjectId(url_dict[b.beer_url][1])}):
                        vec = v['sim_vec'].split(',')
                        sub_list.append([b.beer_name,b.beer_url])
                        vector = [float(v.strip('[').strip(']')) for v in vec]
                        sub_beer_vecs.append(vector)
                except:
                    pass
            menu_list.append(sub_list)
            beer_vecs.append(sub_beer_vecs)


    for beer in beers:
        if beer != '':
            #for b in (Beer.select().where((Beer.beer_name.regexp(beer)) |
            #         (Beer.brewery_name.regexp(beer)))):
            for b in (Beer.select().where((Beer.beer_name.regexp(beer)) |
                     (Beer.brewery_name.regexp(beer)))):
                beer_list.append(url_dict[b.beer_url][0])
            #    choice_indices = []
            #    try:
            #        choice_indices.append(url_dict[b.beer_url][0])
            #    except:
            #        pass
        
            #menu_list.append(choice_indices)
            
    m = {} 
    #print(m)
    print(len(beer_vecs))
    print(menu_list)
    
    for j in range(len(menu_list)):
        for i in range(len(beer_vecs[j])):
            l = []
            for b in beer_list:
                l.append(beer_vecs[j][i][b])
            m[menu_list[j][i][0]] = np.sum(l)
        
    sorted_m = sorted(m.items(), key=operator.itemgetter(1), reverse=True)

    print(sorted_m)
    return sorted_m
    
#    beers_summed = df[beer_list].apply(lambda row: np.sum(row), axis=1)
#    print(beers_summed)
#    beers_summed = beers_summed.sort_values(ascending=False)
#    ranked_beers = beers_summed.index[beers_summed.index.isin(beer_list)==False]
#    ranked_beers = beers_summed.index[beers_summed.index.isin(menu_list)==True]
#    ranked_beers = ranked_beers.tolist()
#    ranked_beers[:5]
    


app.run(debug=True)
