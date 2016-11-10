from peewee import *
from playhouse.csv_loader import load_csv

db = SqliteDatabase('similarity_matrix.db')

class SimilarityVector(Model):
    beer_url = CharField(max_length=250, unique=True)
    sim_vec = TextField() # will be in form [b_0, b_1, ..., b_n]
                           # representing the row in the similarity 
                           # matrix for this beer

    class Meta:
        database = db


def add_vec(beer_url, sim_vec):
    """ Add a similarity vector to the database """
    SimilarityVector.create(beer_url=beer_url,sim_vec=sim_vec)


def delete_row(vec):
    """ Deletes vector instance from database """
    vec.delete_instance()


def load_file(fname):
    """ Initialize the database with csv file """
    load_csv(SimilarityVector, fname)


def initialize(seed=False, fname=None):
    db.connect()
    if seed:
        fname = "similarity_matrix.csv"
        load_file(fname)


if __name__ == '__main__':
    print('here')
    initialize(seed=True)
