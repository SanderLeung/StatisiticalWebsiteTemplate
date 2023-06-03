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

#SF_data = get_fixtures("88g8-5mnd")
SF_data = pd.read_csv('.\Employee_Compensation.csv')
SF_data.name = 'Compensation data'

def plot_fixture_data(df, code):
    jf_group = df.query(f"job_family_code == '{code}'")
    jf_group.boxplot(column='total_salary', by='job_code', figsize=(50,20))
    fig, ax = plt.subplots(figsize = (25,8))
    fig.tight_layout()
    fig.patch.set_facecolor('#E8E5DA')
    plt.savefig('static/images/plot_for_{}.png'.format(df.name),bbox_inches = 'tight', facecolor=fig.get_facecolor())
    return 

#fig size for insta = (25,8) and for website = (15,8)

def overtime_data(df):
    overtime = df.query('Overtime > Salaries and Salaries > 0')
    overtime['overtime_diff'] = overtime['Overtime'] / overtime['Salaries']
    res = overtime.groupby('Job')['overtime_diff'].mean().sort_values(ascending=False)
    return res.to_frame()

    

