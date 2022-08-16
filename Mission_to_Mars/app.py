from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri = "mongodb://localhost:27017/Mission_to_Mars")

@app.route('/')
def home():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route('/scape')
def scrape():
    
    #run the scape function
    mars_scrape = scrape_mars.scrap()
    
    mongo.db.maras.update({}, mars_scrape, upsert=True)
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug = True)