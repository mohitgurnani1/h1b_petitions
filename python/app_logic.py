import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import sklearn.metrics
import sklearn.manifold
from sklearn.preprocessing import StandardScaler
# Get PCA components
import math
import warnings
from sklearn.decomposition import PCA
from sklearn import preprocessing
import re
from matplotlib.ticker import FuncFormatter
import os

def job_wages(df, key, value):
  job_titles = ['PROGRAMMER ANALYST', 'SOFTWARE ENGINEER', 'BUSINESS ANALYST', 'SENIOR SOFTWARE ENGINEER',
                'TECHNOLOGY LEAD - US' , 'ASSISTANT PROFESSOR', 'SENIOR CONSULTANT', 'DATABASE ADMINISTRATOR', 'PHYSICAL THERAPIST', 'MARKET RESEARCH ANALYST']
  if key == 'state':
    return df[(df['state']==value) & (df['JOB_TITLE'].isin(job_titles))].groupby('JOB_TITLE')['PREVAILING_WAGE'].median().reset_index()
  elif key == 'employer':
    temp = df[(df['EMPLOYER_NAME']==value)&(df['JOB_TITLE'].isin(job_titles))].groupby('JOB_TITLE')['PREVAILING_WAGE'].median().reset_index()
    if temp.shape[0] == 0:
      return df[df['EMPLOYER_NAME'] == value].groupby('JOB_TITLE')[
        'PREVAILING_WAGE'].median().reset_index().nlargest(10, columns='PREVAILING_WAGE')
  return df[df['JOB_TITLE'].isin(job_titles)].groupby('JOB_TITLE')['PREVAILING_WAGE'].median().reset_index()

def job_petitions(df, key, value):
  job_titles = ['PROGRAMMER ANALYST', 'SOFTWARE ENGINEER', 'BUSINESS ANALYST', 'SENIOR SOFTWARE ENGINEER',
                'TECHNOLOGY LEAD - US' , 'ASSISTANT PROFESSOR', 'SENIOR CONSULTANT', 'DATABASE ADMINISTRATOR', 'PHYSICAL THERAPIST', 'MARKET RESEARCH ANALYST']
  if key == 'state':
    return df[(df['state'] == value) & (df['JOB_TITLE'].isin(job_titles))]['JOB_TITLE'].value_counts().div(1000).reset_index()
  elif key == 'employer':
    return df[(df['EMPLOYER_NAME'] == value) & (df['JOB_TITLE'].isin(job_titles))]['JOB_TITLE'].value_counts().div(1000).reset_index()
  return df[df['JOB_TITLE'].isin(job_titles)]['JOB_TITLE'].value_counts().div(1000).reset_index()


def geo_map_petitions(df, key, value):
  if key == 'job':
    temp =  df[df['JOB_TITLE']==value]['state'].value_counts().reset_index()
  elif key == 'employer':
    temp =  df[df['EMPLOYER_NAME']==value]['state'].value_counts().reset_index()
  else:
    temp =  df['state'].value_counts().reset_index()
  temp.columns = ['state', 'count']
  cat, bins = pd.qcut(temp['count'], 4, retbins = True)
  l = list(bins)
  l.reverse()
  temp['count'] = temp['count'].apply(lambda x: range_(x, key))#l[1:]))
  return temp


def geo_legend_petitions(df, key, value):
  if key == 'job':
    temp =  df[df['JOB_TITLE']==value]['state'].value_counts().reset_index()
  elif key == 'employer':
    temp =  df[df['EMPLOYER_NAME']==value]['state'].value_counts().reset_index()
  else:
    temp =  df['state'].value_counts().reset_index()
  temp.columns = ['state', 'count']
  cat, bins = pd.qcut(temp['count'], 4, retbins = True)
  l = list(bins)
  l.reverse()
  return l[1:]

def geo_legend_wages(df, key, value):
  if key == 'job':
    temp =  df[df['JOB_TITLE']==value].groupby('state')['PREVAILING_WAGE'].median().reset_index()
  elif key == 'employer':
    temp =  df[df['EMPLOYER_NAME']==value].groupby('state')['PREVAILING_WAGE'].median().reset_index()
  else:
    temp =  df.groupby('state')['PREVAILING_WAGE'].median().reset_index()
  temp.columns = ['state', 'count']
  temp.columns = ['state', 'count']
  cat, bins = pd.qcut(temp['count'], 4, retbins = True)
  l = list(bins)
  l.reverse()
  return l[1:]


def geo_map_wages(df, key, value):
  if key == 'job':
    temp =  df[df['JOB_TITLE']==value].groupby('state')['PREVAILING_WAGE'].mean().reset_index()
  elif key == 'employer':
    temp =  df[df['EMPLOYER_NAME']==value].groupby('state')['PREVAILING_WAGE'].mean().reset_index()
  else:
    temp =  df.groupby('state')['PREVAILING_WAGE'].mean().reset_index()
  temp.columns = ['state', 'count']
  temp['state'] = temp['state'].apply(lambda x: x.title())
  temp['count'] = temp['count'].apply(lambda x: wage_range(x))
  return temp

def wage_range(x):
  if x > 180:
    return 0
  elif x > 140:
    return 1
  elif x > 100:
    return 2
  else:
    return 3


def range_(x, key):
  if key == 'employer' or key == 'job':
    if x > 1500:
      return 0
    elif x > 500:
      return 1
    elif x > 100:
      return 2
    else:
      return 3
  else:
    if x > 200000:
      return 0
    elif x > 90000:
      return 1
    elif x > 20000:
      return 2
    else:
      return 3
  #
  # if x > arr[0]:
  #   return 0
  # elif x > arr[1]:
  #   return 1
  # elif x > arr[2]:
  #   return 2
  # else:
  #   return 3

def employers_wages(df, key, value):

  if key == 'state':
    return df[(df['state']==value) &(df['PREVAILING_WAGE'] < 1000)].groupby('EMPLOYER_NAME')['PREVAILING_WAGE'].median().nlargest(10).reset_index()
  elif key == 'job':
    return df[(df['JOB_TITLE']==value) & (df['PREVAILING_WAGE'] < 1000)].groupby('EMPLOYER_NAME')['PREVAILING_WAGE'].median().nlargest(10).reset_index()
  return df[df['PREVAILING_WAGE'] < 1000].groupby('EMPLOYER_NAME')['PREVAILING_WAGE'].median().nlargest(10).reset_index()

def employers_petition(df, key, value):
  if key == 'state':
    return df[df['state'] == value]['EMPLOYER_NAME'].value_counts().nlargest(10).reset_index()
  elif key == 'job':
    return df[df['JOB_TITLE'] == value]['EMPLOYER_NAME'].value_counts().nlargest(10).reset_index()
  return df['EMPLOYER_NAME'].value_counts().nlargest(10).reset_index()

def job_petition_success_ratio(df, feature):
  if feature == 'wages':
    temp = df[df['CASE_STATUS']=='CERTIFIED'].groupby('EMPLOYER_NAME')['CASE_STATUS'].count().reset_index()
    temp.columns = ['EMPLOYER_NAME', 'CERTIFIED_CASES']
    temp2 = df.groupby('EMPLOYER_NAME')['CASE_STATUS'].count().reset_index()
    temp2.columns = ['EMPLOYER_NAME', 'total']
    total_d = {}
    for index, row in temp2.iterrows():
      total_d[row[0]] = row[1]
    temp['CERTIFIED_CASES'] = temp.apply(lambda row: find(row, total_d), axis=1)
    temp['FAILED_CASES'] = temp['CERTIFIED_CASES'].apply(lambda x: 100 - x)
    employer_list = ['INFOSYS', 'DELOITTE CONSULTING', 'IBM INDIA PRIVATE', 'ACCENTURE', 'MICROSOFT', 'TATA CONSULTANCY', 'ERNST & YOUNG', 'GOOGLE', 'FACEBOOK']
    temp = temp[temp['EMPLOYER_NAME'].isin(employer_list)]
    temp.to_csv('sample/wagesstacked.csv', index=False)
    return temp
  elif feature == 'petitions':
    print("Inside job_petition_success_ratio")
    job_titles = ['PROGRAMMER ANALYST', 'SOFTWARE ENGINEER', 'BUSINESS ANALYST', 'SENIOR SOFTWARE ENGINEER',
                  'TECHNOLOGY LEAD - US' , 'ASSISTANT PROFESSOR', 'SENIOR CONSULTANT', 'DATABASE ADMINISTRATOR', 'PHYSICAL THERAPIST', 'MARKET RESEARCH ANALYST']
    header = {'JOB_TITLE':[],'CERTIFIED_CASES':[],'FAILED_CASES':[]}
    res_df = pd.DataFrame(data = header)
    for job in job_titles:
      conf_num = df[(df['JOB_TITLE']==job) & (df['CASE_STATUS']=='CERTIFIED')].count()[0]
      total = df[df['JOB_TITLE']==job].count()[0]
      conf = (conf_num/total) * 100
      failed = 100 - conf
      res_df.loc[get_index(res_df)]=[job, conf, failed]
    res_df.to_csv('sample/petitionsstatus.csv', index=False)
    return res_df
  else:
    temp = df[df['CASE_STATUS']=='CERTIFIED'].groupby('state')['CASE_STATUS'].count().reset_index()
    temp.columns = ['state', 'CERTIFIED_CASES']
    temp2 = df.groupby('state')['CASE_STATUS'].count().reset_index()
    temp2.columns = ['state', 'total']
    total_d = {}
    for index, row in temp2.iterrows():
      total_d[row[0]] = row[1]
    temp['CERTIFIED_CASES'] = temp.apply(lambda row: find2(row, total_d), axis=1)
    temp['count'] = temp['CERTIFIED_CASES'].apply(lambda x: label_(x))
    temp.to_csv('sample/geomap.csv', index=False)
    return temp

def label_(x):
  if x > 88:
    return 0
  elif x > 80:
    return 1
  return 2

def find2(row, d):
  return row['CERTIFIED_CASES'] / d[row['state']] * 100


def find(row, d):
  return row['CERTIFIED_CASES'] / d[row['EMPLOYER_NAME']] * 100

def get_index(df):
  index = 0
  if df.empty == False:
    index = max(df.index) + 1
  return index


def feature_engg(df):
  df = df.drop(["Unnamed: 0"], axis=1)
  df['state'] = df['WORKSITE'].apply(lambda x: re.sub(r"^.*,", "", x).strip())
  df['state'] = df['state'].apply(lambda x: x.title())
  df['city'] = df['WORKSITE'].apply(lambda x: re.sub(r",.*", "", x).strip())
  del df['SOC_NAME']
  del df['lat']
  del df['lon']
  del df['WORKSITE']
  df = df.dropna()
  df['EMPLOYER_NAME'] = df['EMPLOYER_NAME'].apply(
    lambda x: x.replace("LTD", "").replace("PVT", "").replace("CORPORATION", "").replace("AFFAIRS", "").replace("MANAGEMENT", "").replace(",", "").replace(
      "/NMVAHCS", "").replace("RIDER", "").replace("&AMP;", "").replace("LLP", "").replace("INC.","").replace("PLLC", "").replace("INC.",
                                                                               "").replace(
      "LLC", "").replace("LIMITED", "").replace("SERVICES", "").replace("SOLUTIONS", "").replace("U.S.", "").strip())

  df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
  df['PREVAILING_WAGE'] = df['PREVAILING_WAGE'].apply(lambda x: round(x/1000, 1))
  indexNames = df[df['EMPLOYER_NAME']=='MODANI HOLDINGS'].index
  df.drop(indexNames , inplace=True)
  indexNames = df[df['EMPLOYER_NAME'] == 'IGNITIONONE'].index
  df.drop(indexNames, inplace=True)
  return df

def convert_cat(df2):
  df = df2.copy(deep=True)
  object_feats = df.dtypes[df.dtypes == "object"].index
  for i in object_feats:
    df[i] = df[i].astype('category')
    df[i] = df[i].cat.codes
  return df

def reduce_df(df, s, e):
  df2 = df.copy(deep=True)
  return df2[(df2['YEAR'] >= s) & (df2['YEAR'] <= e)]

def get_year(start, end):
  return compute_date(start), compute_date(end)

def compute_date(num):
  num = int(num)
  return 2011 + round(num/650*5)


def get_histogram(df):
  return df['YEAR']

def compute_sample(df, num = 358):
  num = math.floor(df.shape[0]/100)
  df_sample = df.sample(n= num)
  return df_sample


def compute_elbow(df):
  distortions = []
  for i in range(1, 11):
    km = KMeans(
      n_clusters=i, init='random',
      n_init=10, max_iter=300,
      tol=1e-04, random_state=0
    )
    km.fit(df)
    distortions.append(km.inertia_)
  return distortions

def sk_normalize(df):
  min_max_scaler = preprocessing.MinMaxScaler()
  np_scaled = min_max_scaler.fit_transform(df)
  return pd.DataFrame(np_scaled, columns = df.columns)

def standardize(df):
  df_std = StandardScaler().fit_transform(df)
  return pd.DataFrame(df_std, columns=df.columns)

def compute_stratified(df, n = 4):
  km = KMeans(
    n_clusters=n, init='random',
    n_init=10, max_iter=300,
    tol=1e-04, random_state=0
  )
  y_km = km.fit_predict(df)
  df_stratified_temp = df.copy()
  df_stratified_temp['cluster'] = y_km
  df_stratified = df_stratified_temp.groupby(y_km).apply(lambda x: x.sample(int(min(len(x), 0.25 * len(x)))))
  return df_stratified

def get_pca(df):
  pcamodel = PCA(n_components=4)
  pca = pcamodel.fit_transform(sk_normalize(df))
  return pcamodel, pca

def scree_plot(df):
  pcamodel, pca = get_pca(df)
  return [*range(1, len(pcamodel.explained_variance_ratio_) + 1)], pcamodel.explained_variance_ratio_ * 100, np.cumsum(pcamodel.explained_variance_ratio_ * 100)

def sum_sq(a):
  sum = 0
  for i in a:
    sum += i * i
  return sum

def scatter_plot(pca):
  return pca[:, 0], pca[:, 1]

def scatter_plot_pca(df):
  pcamodel, pca = get_pca(df_sample_)
  return scatter_plot(pca)

def scatter_plot_mds_euc(df):
  dissimilarity_distance_matrix = sklearn.metrics.pairwise.pairwise_distances(df_sample_, metric='euclidean')
  mds = sklearn.manifold.MDS(n_components=2, dissimilarity='precomputed').fit_transform(dissimilarity_distance_matrix)
  return scatter_plot(mds)


df=pd.read_csv('../h1b_kaggle.csv')
df = feature_engg(df)
df_sample = compute_sample(df)
df_sample_ = sk_normalize(convert_cat(df_sample))
#df_stratified = compute_stratified(df, 4)
warnings.filterwarnings("ignore", category=DeprecationWarning)

temp = df_sample[['YEAR','PREVAILING_WAGE']].copy()
temp['PREVAILING_WAGE'] = temp['PREVAILING_WAGE'].apply(lambda  x: 0)
temp.to_csv('sample/timeline.csv')
job_petition_success_ratio(df, 'petitions')
job_petition_success_ratio(df, 'wages')
job_petition_success_ratio(df, 'state')

employer_list = ['INFOSYS', 'DELOITTE CONSULTING', 'IBM INDIA PRIVATE', 'ACCENTURE', 'MICROSOFT', 'TATA CONSULTANCY',
                 'ERNST & YOUNG', 'GOOGLE', 'FACEBOOK']
df[(df['PREVAILING_WAGE'] < 150 )&  (df['EMPLOYER_NAME'].isin(employer_list))][['CASE_STATUS', 'PREVAILING_WAGE', 'EMPLOYER_NAME']].to_csv('sample/pc.csv', index = False)
