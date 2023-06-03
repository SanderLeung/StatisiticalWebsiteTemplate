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
import random

#Data imports
#from GetFixtures import SF_data, SF_Overtime
from GetFixtures import overtime_data
SF_data = pd.read_csv('.\Employee_Compensation.csv')
SF_Overtime = overtime_data(SF_data)

app = Flask(__name__)

#Pandas Page
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def OT():
    return render_template('pandas.html',
                           PageTitle = "Pandas",
                           table=[SF_Overtime.to_html(classes='data', index = False)], titles= SF_Overtime.columns.values)



#Matplotlib page
@app.route('/legend', methods=("POST", "GET"))
def legend():
    return render_template('legend.html',
                           PageTitle = "Legend")


@app.route('/plot/<code>')
def plot_png(code=1000):
    fig = create_figure(code)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(code):
    fig, ax = plt.subplots(figsize = (20,10))
    fig.patch.set_facecolor('#E8E5DA')
    jf_group = SF_data.query(f"`Job Family Code` == '{code}'")
    
    x = sorted(jf_group['Job Code'].unique())
    data = [jf_group.query("`Job Code` == @job_code")['Total Salary'] for job_code in x]

    if x:
        ax.boxplot(data, labels = x)

    plt.xticks(rotation = 30, size = 10)
    plt.xlabel("Job Code", size = 15)
    plt.ylabel("Salary", size = 10)
    plt.title("Salary Dist by Job", size = 20)

    return fig

if __name__ == '__main__':
    app.run(debug = True)
