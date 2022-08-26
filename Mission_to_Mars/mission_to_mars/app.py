from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mission_to_mars")



@app.route('/')
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars_scrape = mars)


@app.route('/scape')
def scrape():
    
    #run the scape function
    mars = mongo.db.mars
    mars_scrape = scrape_mars.scrape()
    mars.replace_one({}, mars_scrape, upsert=True)
    
    return redirect('/', code = 302)

if __name__ == "__main__":
    app.run(debug = True)