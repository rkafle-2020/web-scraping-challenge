from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017/"
# client = pymongo.MongoClient(conn)


# app.config 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# mars = mongo.db.mars
# mars_data = scrape_mars.scrape_all()
# mars.update({}, mars_data, upsert=True)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_facts = mongo.db.mars.find_one()
    
    # Return template and data
    return render_template("index.html", mars_facts=mars_facts)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_scrape = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_scrape, upsert=True)

    #Call the scrape_mars.py and store dictionary of results to mongo
    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)