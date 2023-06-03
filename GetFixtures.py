import pandas as pd
import matplotlib.pyplot as plt
from sodapy import Socrata

def get_fixtures(dataset):
    
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.sfgov.org", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.sfgov.org,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    results = client.get_all(dataset)

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)
    
    return(df)

#SF_data = pd.read_csv('.\Employee_Compensation.csv')
#SF_data.name = 'Compensation data'

def get_sf_data():
    df = get_fixtures("88g8-5mnd")
    df["total_salary"] = df["total_salary"].astype(float)
    df["overtime"] = df["overtime"].astype(float)
    df["salaries"] = df["salaries"].astype(float)
    return df

def create_figure(df, code):
    fig, ax = plt.subplots(figsize = (20,10))
    fig.patch.set_facecolor('#E8E5DA')
    jf_group = df.query(f"job_family_code == '{code}'")
    
    x = sorted(jf_group['job_code'].unique())
    data = [jf_group.query("job_code == @job_code")['total_salary'] for job_code in x]

    if x:
        ax.boxplot(data, labels = x)

    plt.xticks(rotation = 30, size = 10)
    plt.xlabel("Job Code", size = 15)
    plt.ylabel("Salary", size = 10)
    plt.title("Salary Dist by Job", size = 20)

    return fig

#fig size for insta = (25,8) and for website = (15,8)

def overtime_data(df):
    overtime = df.query('overtime > salaries and salaries > 0')
    overtime['overtime_diff'] = overtime['overtime'] / overtime['salaries']
    res = overtime.groupby('job')['overtime_diff'].mean().sort_values(ascending=False)
    return res.to_frame()

    

