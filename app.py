# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Connect to mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"

mongo = PyMongo(app)

@app.route("/")
def home():
    
    mars_data = mongo.db.mars.find_one()
    

    return render_template('index.html', data=mars_data)

@app.route("/scrape")
def scraper():
    
    mars_data = mongo.db.mars
    update_data = scrape_mars.scrape()
    mars_data.update({}, update_data, upsert=True)
    return (redirect("/", code=302))

if __name__ == "__main__":
    app.run(debug=True)