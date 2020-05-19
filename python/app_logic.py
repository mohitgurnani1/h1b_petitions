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

def job_wages(df):
  job_titles = ['PROGRAMMER ANALYST', 'SOFTWARE ENGINEER', 'BUSINESS ANALYST', 'SENIOR SOFTWARE ENGINEER',
                'TECHNOLOGY LEAD - US' , 'ASSISTANT PROFESSOR', 'SENIOR CONSULTANT', 'DATABASE ADMINISTRATOR', 'PHYSICAL THERAPIST', 'MARKET RESEARCH ANALYST']
  return df[df['JOB_TITLE'].isin(job_titles)].groupby('JOB_TITLE')['PREVAILING_WAGE'].mean().reset_index()

def job_petitions(df):
  # print(df['JOB_TITLE'].value_counts()[:30]) #Top 30 job roles
  job_titles = ['PROGRAMMER ANALYST', 'SOFTWARE ENGINEER', 'BUSINESS ANALYST', 'SENIOR SOFTWARE ENGINEER',
                'TECHNOLOGY LEAD - US' , 'ASSISTANT PROFESSOR', 'SENIOR CONSULTANT', 'DATABASE ADMINISTRATOR', 'PHYSICAL THERAPIST', 'MARKET RESEARCH ANALYST']

  return df[df['JOB_TITLE'].isin(job_titles)]['JOB_TITLE'].value_counts().div(1000).reset_index()

def job_petition_success_ratio(df):
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
  # print(res_df)
  return res_df
   
def get_index(df):
  index = 0
  if df.empty == False:
    index = max(df.index) + 1
  return index

def geo_map_petitions(df):
  temp =  df['state'].value_counts().reset_index()
  temp.columns = ['state', 'count']
  temp['state'] = temp['state'].apply(lambda x: x.title())
  temp['count'] = temp['count'].apply(lambda x: range(x))
  return temp

def geo_map_wages(df):
  temp =  df.groupby('state')['PREVAILING_WAGE'].mean().reset_index()
  temp.columns = ['state', 'count']
  temp['state'] = temp['state'].apply(lambda x: x.title())
  temp['count'] = temp['count'].apply(lambda x: wage_range(x))
  return temp

def wage_range(x):
  if x > 180000:
    return 0
  elif x > 140000:
    return 1
  elif x > 100000:
    return 2
  else:
    return 3


def range(x):
  if x > 200000:
    return 0
  elif x > 90000:
    return 1
  elif x > 20000:
    return 2
  else:
    return 3

def employers_wages(df):
  return df.groupby('EMPLOYER_NAME')['PREVAILING_WAGE'].mean().nlargest(10).reset_index()

def employers_petition(df):
  return df['EMPLOYER_NAME'].value_counts().nlargest(10).reset_index()

def feature_engg(df):
  df = df.drop(["Unnamed: 0"], axis=1)
  df['state'] = df['WORKSITE'].apply(lambda x: re.sub(r"^.*,", "", x).strip())
  df['city'] = df['WORKSITE'].apply(lambda x: re.sub(r",.*", "", x).strip())
  del df['SOC_NAME']
  del df['lat']
  del df['lon']
  del df['WORKSITE']
  df = df.dropna()
  return df

def convert_cat(df2):
  df = df2.copy(deep=True)
  object_feats = df.dtypes[df.dtypes == "object"].index
  for i in object_feats:
    df[i] = df[i].astype('category')
    df[i] = df[i].cat.codes
  return df


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
