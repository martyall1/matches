from flask import Flask, make_response, render_template, redirect, request, url_for
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Comparison
from io import StringIO
import csv

engine = create_engine("sqlite:///comparisons.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home.html')

@app.route('/compare/')
def make_comparison():
    session = DBSession()
    comparison = session.query(Comparison).order_by(Comparison.total_comparisons.asc()).first()
    session.close()
    return render_template('comparison.html', comparison=comparison)
        
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
    data_writer.writerow(["decision_id", "contract_id", "is_match", "is_not_match", "pass"])
    data_writer.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=matches.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0', port=8000)
