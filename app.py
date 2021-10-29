from flask import Flask, jsonify
from sqlalchemy.engine import create_engine
from flask_cors import CORS

#engine = create_engine("sqlite:///DataFiles/SAEXP1")

app = Flask(__name__)
CORS(app)
pw = 'TZFLAhpQ6P1tPJzfXg3MoUnfUIOcHcd2'

#DATABASE_URI = f'postgresql+psycopg2://postgres:{pw}@localhost:5432/Project2_Dev'
DATABASE_URI = f'postgresql+psycopg2://kwwhumda:{pw}@fanny.db.elephantsql.com:5432/kwwhumda'

engine = create_engine(DATABASE_URI)

@app.route("/api")
def all_data():
    result = engine.execute("select * from us_expenditure")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))

    return jsonify(result_list)

@app.route("/api/<state>")
def state(state):
    result = engine.execute(f"select * from us_expenditure where GeoName = '{state}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))

    return jsonify(result_list)

@app.route("/api/<state>/<year>")
def year(state, year):
    result = engine.execute(f"select GeoName, Description, `{year}` from us_expenditures where GeoName = '{state}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))

    return jsonify(result_list)

@app.route("/api/fips/<geo_fips>")
def fips(geo_fips):
    result = engine.execute(f"select * from us_expenditure where geofips = '{geo_fips}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
       result_list.append(dict(r))
    #fips = f'\"{fips}\"'
    #return (fip)
    return jsonify(result_list)

@app.route("/api/total2/<code>")
def total2(code):
    result = engine.execute(f"select dollars from us_expenditure where code = '{code}' AND description = 'Personal consumption expenditures' AND year = 2019")
    r = result.fetchone()
    return str(round(r[0]))

@app.route("/api/total1/<code>")
def total1(code):
    result = engine.execute(f"select dollars from us_expenditure where code = '{code}' AND description = 'Personal consumption expenditures' AND year = 2019")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

@app.route("/api/all_years")
def total_years():
    result = engine.execute(f"select geoname, description, year, dollars FROM us_spend_df")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

@app.route("/api/exp_by_year/<year>")
def exp_by_year(year):
    result = engine.execute(f"select geoname, dollars from us_spend_df where description = 'Personal consumption expenditures' AND year = '{year}'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

if __name__ == '__main__':
    app.run(debug=True)