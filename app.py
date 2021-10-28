from flask import Flask, jsonify
from sqlalchemy.engine import create_engine

#engine = create_engine("sqlite:///DataFiles/SAEXP1")

app = Flask(__name__)

#pw = 'kyler20'
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

@app.route("/api/total2/<state>")
def total2(state):
    result = engine.execute(f"select \"2019\" from us_expenditures where GeoName = '{state}' AND Description = 'Personal consumption expenditures'")
    r = result.fetchone()
    return str(round(r[0]))

@app.route("/api/total1/<state>")
def total1(state):
    result = engine.execute(f"select \"2019\" from us_expenditures where GeoName = '{state}' AND Description = 'Personal consumption expenditures'")
    rows = result.fetchall()
    result_list = []
    for r in rows:
        result_list.append(dict(r))
    return jsonify(result_list)

if __name__ == '__main__':
    app.run(debug=True)