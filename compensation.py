"""  HOW TO HOST PANDAS AND MATPLOTLIB ONLINE TEMPLATE"""
#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for 
from flask import Response

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io

#Data imports
from GetFixtures import *
#SF_data = pd.read_csv('.\Employee_Compensation.csv')

app = Flask(__name__)
SF_Data = get_sf_data()

#Pandas Page
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def OT():
    SF_Overtime = overtime_data(SF_Data)
    return render_template('pandas.html',
                           PageTitle = "Pandas",
                           table=[SF_Overtime.to_html(classes='data', index = False)], titles= SF_Overtime.columns.values)
#Matplotlib page
@app.route('/legend', methods=("POST", "GET"))
def legend():
    return render_template('legend.html',
                           PageTitle = "Legend")

@app.route('/plot')
def plot_all():
    output = io.BytesIO()
    for family in sorted(SF_Data['job_family_code'].unique()):
        fig = create_figure(SF_Data, family) 
        FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot/<code>')
def plot_png(code=1000):
    fig = create_figure(SF_Data, code)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug = True)
