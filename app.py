from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_scraped = mongo.db.mars_scraped.find_one()
    return render_template("index.html", marshtml = mars_scraped)


@app.route("/scrape")
def scraper():
    mars_scraped = mongo.db.mars_scraped
    mars_data = scrape_mars.scrape()
    mars_scraped.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)