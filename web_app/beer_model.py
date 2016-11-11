from peewee import *
from playhouse.csv_loader import load_csv

db = SqliteDatabase('beers.db')

class Beer(Model):
    beer_url = CharField(max_length=200,unique=True)
    beer_name = CharField(max_length=200)
    brewery_name = CharField(max_length=200)

    class Meta:
        database = db


def add_beer(beer_url, beer_name, brewery_name):
    """ Create a new beer instance """
    Beer.create(beer_url=beer_url,beer_name=beer_name,
                brewery_name=brewery_name)


def delete_beer(beer):
    """ Delete given beer instance """
    beer.delete_instance()


def load_file(fname):
    """ Initialize the database with given csv file """
    load_csv(Beer, fname)


def initialize(seed=False, fname=None):
    db.connect()
    if seed:
        #fname = "beer_list.csv"
        fname = "test_beer.csv"
        load_file(fname)

if __name__ == '__main__':
    initialize(seed=True)
