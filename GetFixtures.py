import pandas as pd
import matplotlib.pyplot as plt
from sodapy import Socrata
import datetime

def get_sf_data():
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.sfgov.org", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.sfgov.org,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")
    now = datetime.datetime.now()
    last_year = now.year - 1
    results = client.get_all("88g8-5mnd", year=last_year, year_type='Calendar')

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)
    df["total_salary"] = df["total_salary"].astype(float)
    df["overtime"] = df["overtime"].astype(float)
    df["salaries"] = df["salaries"].astype(float)
    return(df)

#SF_data = pd.read_csv('.\Employee_Compensation.csv')
#SF_data.name = 'Compensation data'

def create_figure(df, code):
    fig, ax = plt.subplots(figsize = (20,10))
    fig.patch.set_facecolor('#E8E5DA')
    jf_group = df.query(f"job_family_code == '{code}'")
    
    x = sorted(jf_group['job_code'].unique())
    data = [jf_group.query("job_code == @job_code")['total_salary'] for job_code in x]

    if x:
        ax.boxplot(data, labels = x)

    plt.xlabel("Job Code", size = 15)
    plt.ylabel("Salary", size = 10)
    plt.title(f"Salary Dist by Job for family {code}", size = 20)

    return fig

def overtime_data(df):
    overtime = df.query('overtime > salaries and salaries > 0')
    overtime['overtime_diff'] = overtime['overtime'] / overtime['salaries']
    res = overtime.groupby('job')['overtime_diff'].mean().sort_values(ascending=False)
    return res.to_frame()

    

