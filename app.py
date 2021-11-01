# Flask app deployed to Heroku

from flask import Flask, jsonify
from sqlalchemy.engine import create_engine
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

# ElephantSQL password stored in local config file
#from config import pw

# ElephantSQL password stored as Heroku environment variable
pw = os.getenv('PASSWORD')

# ElephantSQL server path
DATABASE_URI = f'postgresql+psycopg2://kwwhumda:{pw}@fanny.db.elephantsql.com:5432/kwwhumda'

engine = create_engine(DATABASE_URI)

# Return entire dataframe
@app.route("/api")
def all_data():
    result = engine.execute("select * from us_spend_df")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))

    return jsonify(result_list)

# Return everything given state name
@app.route("/api/<state>")
def state(state):
    result = engine.execute(f"select * from us_spend_df where GeoName = '{state}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))

    return jsonify(result_list)

# Return state name, description,year given state name, year
@app.route("/api/<state>/<year>")
def year(state, year):
    result = engine.execute(f"select geoname, description, `{year}` from us_spend_df where geoname = '{state}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))

    return jsonify(result_list)

# Return everything given GeoFIPS
@app.route("/api/fips/<geo_fips>")
def fips(geo_fips):
    result = engine.execute(f"select * from us_spend_df where geofips = '{geo_fips}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
       result_list.append(dict(r))
    
    return jsonify(result_list)

# Return dollars for Personal Consumption for 2019 given state abbr
@app.route("/api/total2/<code>")
def total2(code):
    result = engine.execute(f"select dollars from us_spend_df where code = '{code}' AND description = 'Personal consumption expenditures' AND year = 2019")
    r = result.fetchone()
    return str(round(r[0]))

# Same as above as dict
@app.route("/api/total1/<code>")
def total1(code):
    result = engine.execute(f"select dollars from us_spend_df where code = '{code}' AND description = 'Personal consumption expenditures' AND year = 2019")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Return state name, description, year, and dollars
@app.route("/api/all_years")
def total_years():
    result = engine.execute(f"select geoname, description, year, dollars FROM us_spend_df")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Return state name, description, year, dollars given state abbr and description
@app.route("/api/all_years/<code>/<desc>")
def total_years_state(code, desc):
    result = engine.execute(f"select geoname, description, year, dollars FROM us_spend_df WHERE code = '{code}' AND description = '{desc}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Return state name, description, year, dollars given state abbr, description, and year
@app.route("/api/by_year/<code>/<desc>/<year>")
def total_by_years_state(code, desc, year):
    result = engine.execute(f"select geoname, description, year, dollars FROM us_spend_df WHERE code = '{code}' AND description = '{desc}' AND year = {year}")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Return state abbr, dollars for Personal Consumption for given year
@app.route("/api/exp_by_year/<year>")
def exp_by_year(year):
    result = engine.execute(f"select code, dollars from us_spend_df where description = 'Personal consumption expenditures' AND year = '{year}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Return  state abbr, year, description, dollars for main subcategories given state abbr
@app.route("/api/sub_by_state/<code>")
def sub_by_state(code):
    result = engine.execute(f"select code, year, description, dollars from us_spend_df where code = '{code}' AND (description = 'Durable goods' OR description = 'Nondurable goods' OR description = 'Household consumption expenditures (for services)' OR description = 'Final consumption expenditures of nonprofit institutions serving households (NPISHs)') ORDER BY year")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Same as above, sorted by year then description
@app.route("/api/sub_by_state2/<code>")
def sub_by_state2(code):
    result = engine.execute(f"select code, year, description, dollars from us_spend_df where code = '{code}' AND (description = 'Durable goods' OR description = 'Nondurable goods' OR description = 'Household consumption expenditures (for services)' OR description = 'Final consumption expenditures of nonprofit institutions serving households (NPISHs)') ORDER BY year, description")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

# Return all subcategory dollars for all years and states
@app.route("/api/all_data")
def all_data2():
 
    data_dict = {}
    for year in range(1997,2020):
        result = engine.execute(f"select description, dollars FROM us_spend_df where (year = {year} AND code = 'US') AND \
            (description = 'Motor vehicles and parts' OR \
            description = 'Furnishings and durable household equipment' OR \
            description = 'Recreational goods and vehicles' OR \
            description = 'Food and beverages purchased for off-premises consumption' OR \
            description = 'Clothing and footwear' OR \
            description = 'Gasoline and other energy goods' OR \
            description = 'Housing and utilities' OR \
            description = 'Health care' OR \
            description = 'Transportation services' OR \
            description = 'Recreation services' OR \
            description = 'Food services and accommodations' OR \
            description = 'Financial services and insurance')")
        rows = result.fetchall()
        result_list = []
        for r in rows:
            result_list.append(dict(r))

        data_dict.update({year:result_list})

    return jsonify(data_dict)

if __name__ == '__main__':
    app.run(debug=False)