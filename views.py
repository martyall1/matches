from flask import Flask, make_response, render_template, redirect, request, url_for
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Comparison, User
from io import StringIO
import csv

import config


engine = create_engine("sqlite:///comparisons.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home.html')

@app.route('/set_cookie/', methods=['GET'])
def setcookie():
    resp = make_response(redirect(url_for('make_comparison')))
    user_id = request.cookies.get("user_id")
    if user_id:
        return resp
    else:
        session = DBSession()
        indices = session.query(User).order_by(User.id.desc())
        if indices:
            user_id = str(indices[0].id + 1)
        else:
            user_id = "1"
        session.add(User(id=user_id, responses=0))
        session.commit()
        session.close()
        resp.set_cookie('user_id', user_id)
        return resp

@app.route('/compare/')
def make_comparison():
    user_id = request.cookies.get('user_id')
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    if (user.responses > 0) and (user.responses > config.min_repetitions):
        user.responses = 0
        session.commit()
        session.close()
        return redirect(url_for('finish'))
    comparison = session.query(Comparison).order_by(Comparison.total_comparisons.asc()).first()
    session.close()
    resp = make_response(render_template('comparison.html', comparison=comparison))
    return resp
        
@app.route("/commit/<int:comparison_id>/", methods=['POST'])
def commit_comparison(comparison_id):
    response = request.form['submit']
    print(response)
    session = DBSession()
    comparison = session.query(Comparison).filter_by(id=comparison_id).one()
    if response == "Match":
        comparison.is_match += 1
    elif response == "Not a Match":
        comparison.is_not_match += 1
    else:
        comparison.is_pass += 1
    comparison.total_comparisons += 1
    user_id = request.cookies.get('user_id')
    session.query(User).filter_by(id=user_id).one().responses += 1
    session.commit()
    session.close()
    return redirect(url_for('make_comparison'))

@app.route("/data/")
def return_data():
    si = StringIO()
    data_writer = csv.writer(si)
    session = DBSession()
    data = session.query(Comparison).with_entities(Comparison.decision_id,
            Comparison.contract_id, Comparison.is_match, Comparison.is_not_match,
            Comparison.is_pass)
    data_writer.writerow(config.csv_columns)
    data_writer.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=%s" % config.csv_filename
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/finish/")
def finish():
    return render_template("finish.html")


if __name__ == "__main__":
    app.debug=True
    app.run(host=config.ip, port=config.port)
