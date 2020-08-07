import app_logic


def get_petitions_jobs(df, key, value):
  temp = app_logic.job_petitions(df, key, value)
  temp.columns = ['Job Title', 'Petitions']
  body = {
    "Job Title": list(temp['Job Title']),
    "Petitions": list(temp['Petitions'])
  }
  return body

def get_wages_jobs(df, key, value):
  temp = app_logic.job_wages(df, key, value)
  temp.columns = ['Job Title', 'Wages']
  body = {
    "Job Title": list(temp['Job Title']),
    "Wages": list(temp['Wages'])
  }
  return body



def get_petitions_employers(df, key, value):
  temp = app_logic.employers_petition(df, key, value)
  temp.columns = ['EMPLOYER_NAME', 'COUNT']
  #temp = temp[:10]
  temp['EMPLOYER_NAME'] = temp['EMPLOYER_NAME'].apply(
    lambda x: x.replace("CORPORATION", "").replace("LLP", "").replace("LIMITED", "").replace("SERVICES", "").replace(
      "SOLUTIONS", "").replace("U.S.", "").strip())
  body = {
    "EMPLOYER_NAME": list(temp['EMPLOYER_NAME']),
    "COUNT": list(temp['COUNT'])
  }
  return body


def get_wages_employers(df, key, value):
  temp = app_logic.employers_wages(df, key, value)
  temp.columns = ['EMPLOYER_NAME', 'COUNT']

  body = {
    "EMPLOYER_NAME": list(temp['EMPLOYER_NAME']),
    "COUNT": list(temp['COUNT'])
  }
  return body

def geo_legend_petitions(df, key, value):
 temp = app_logic.geo_legend_petitions(df, key, value)
 body = {
   "legend": temp
 }
 return body

def geo_legend_wages(df, key, value):
  temp = app_logic.geo_legend_wages(df, key, value)
  body = {
    "legend": temp
  }
  return body


def get_scatter_plot_pca(df):
  x1, x2 = app_logic.scatter_plot_pca(df)
  body = {
    "x1": list(x1),
    "x2": list(x2),
    "cluster": list(df['cluster'] if 'cluster' in df.columns else [0] * len(df))
  }
  return body

def get_scatter_plot_mds(df):
  x1, x2 = app_logic.scatter_plot_mds_euc(df)
  body = {
    "x1": list(x1),
    "x2": list(x2),
    "cluster": list(df['cluster'] if 'cluster' in df.columns else [0] * len(df))
  }
  return body


def get_histogram(df):
  x = app_logic.get_histogram(df)
  body = {
    "x": list(x)
  }
  return body