#dependencies

from flask import Flask, render_template
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars



# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_DB

# Drops collection if available to remove duplicates
#db.listing_data.drop()


# Set route
@app.route('/')
def index():
    scrape()
    listings = db.listing_data.find_one()

    # Return the template with the teams list passed in
    return render_template('index.html', listings=listings)


@app.route('/scrape')
def scrape():
    listing = db.listing_data
    data = scrape_mars.scrape()
    listing.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
