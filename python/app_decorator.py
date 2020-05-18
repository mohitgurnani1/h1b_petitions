import app_logic

def get_scree_plot(df):
  x, y_bar, y_line = app_logic.scree_plot(df[features])
  body = {
    "x_label": "Components",
    "y_label": "Explained Variance",
    "z_label": "Cumulative Explained Variance",
    "x": x,
    "y": list(y_bar),
    "z": list(y_line)
  }
  return body


def get_petitions_jobs(df):
  temp = app_logic.job_petitions(df)
  temp.columns = ['Job Title', 'Petitions']
  body = {
    "Job Title": list(temp['Job Title']),
    "Petitions": list(temp['Petitions'])
  }
  return body

def get_wages_jobs(df):
  temp = app_logic.job_wages(df)
  temp.columns = ['Job Title', 'Wages']
  body = {
    "Job Title": list(temp['Job Title']),
    "Wages": list(temp['Wages'])
  }
  return body



def get_petitions_employers(df):
  temp = app_logic.employers_petition(df)
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


def get_wages_employers(df):
  temp = app_logic.employers_wages(df)
  temp.columns = ['EMPLOYER_NAME', 'COUNT']
  #temp = temp[:10]
  temp['EMPLOYER_NAME'] = temp['EMPLOYER_NAME'].apply(
    lambda x: x.replace("CORPORATION", "").replace("AFFAIRS", "").replace("MANAGEMENT", "").replace(",", "").replace("/NMVAHCS", "").replace("RIDER", "").replace("&AMP;", "").replace("LLP", "").replace("PLLC", "").replace("INC.", "").replace("LLC", "").replace("LIMITED", "").replace("SERVICES", "").replace(
      "SOLUTIONS", "").replace("U.S.", "").strip())
  body = {
    "EMPLOYER_NAME": list(temp['EMPLOYER_NAME']),
    "COUNT": list(temp['COUNT'])
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