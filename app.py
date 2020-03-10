# Dependencies
from flask import Flask, render_template
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()

# Creates a collection in the database and inserts two documents
db.mars.insert_one(scrape_mars.scrape())


@app.route("/")
def home():
    
    data = list(db.mars.find())

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)