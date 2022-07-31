from flask import Flask, render_template, redirect, url_for # use flask to render a template, redirect to another URL, and create a URL
from flask_pymongo import PyMongo # use PyMongo to interact with Mongo database
import scraping # Convert from jupyter notebook to Python for scraping code

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # app will connect to Mongo using a URI (uniform resource identifier) using a database called mars_app
mongo = PyMongo(app) # the URI that will be used to connect the app to Mongo using port 27017 
# define route for HTML page
@app.route("/") # route to tell Flask what to display when looking at index.html homepage
def index(): # create a function called "index"
   mars = mongo.db.mars.find_one() # uses PyMongo to find "mars" collection in "mars_app" database
   return render_template("index.html", mars=mars) # tells Flask to return HTML template using index.html file using "mars" collection in Mongo

# set up scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars # assign a new variable that points to Mongo collection
   mars_data = scraping.scrape_all() # .scrape_all() in the scraping.py file exported from Jupyter notebook
   mars.update_one({}, {"$set":mars_data}, upsert=True) # .update_one() updates database with new gathered data stored in mars_data. It will create a new doc if one doesn't already exist.
   return redirect('/', code=302) # add a redirect after successsfully scraping the data

if __name__ == "__main__":
   app.run()