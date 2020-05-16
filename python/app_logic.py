import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import sklearn.metrics
import sklearn.manifold
from sklearn.preprocessing import StandardScaler
# Get PCA components
import warnings
from sklearn.decomposition import PCA
from sklearn import preprocessing

def feature_engg(df):
  numeric_feats = df.dtypes[df.dtypes != "object"].index
  skewed_feats = df[numeric_feats].skew(axis=0, skipna=True)
  skewed_feats = skewed_feats[skewed_feats > 1]
  skewed_feats = skewed_feats.index
  df[skewed_feats] = np.log1p(df[skewed_feats])
  object_feats = df.dtypes[df.dtypes == "object"].index
  for i in object_feats:
    df[i] = df[i].fillna('None')
    df[i] = df[i].astype('category')
    df[i] = df[i].cat.codes

def compute_sample(df, num = 358):
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
    # plt.plot(range(1, 11), distortions, marker='o')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('Distortion')
    # plt.show()
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
  pcamodel = PCA(n_components=16)
  pca = pcamodel.fit_transform(sk_normalize(df))
  return pcamodel, pca

def scree_plot(df):
  pcamodel, pca = get_pca(df)
  #variance_ratio = pcamodel.explained_variance_ / sum(pcamodel.explained_variance_)
  return [*range(1, len(pcamodel.explained_variance_ratio_) + 1)], pcamodel.explained_variance_ratio_ * 100, np.cumsum(pcamodel.explained_variance_ratio_ * 100)
  # plt.bar(range(1, len(variance_ratio) + 1), variance_ratio * 100)
  # plt.ylabel('Explained variance')
  # plt.xlabel('Components')
  # plt.plot(range(1, len(variance_ratio) + 1),
  #          np.cumsum(variance_ratio * 100),
  #          c='red',
  #          label="Cumulative Explained Variance")
  # plt.legend(loc='upper left')
def sum_sq(a):
  sum = 0
  for i in a:
    sum += i * i
  return sum

def top_3_attributes(df):
  top_3 = top_3_names(df)
  return df[top_3]
  # x = {}
  # for i in df.columns[top_3]:
  #   x[i] = list(temp.get(i))
  # return x

def top_3_names(df):
  pcamodel, pca = get_pca(df)
  pcamodel_tr = np.transpose(pcamodel.components_)
  most_important = [sum_sq(pcamodel_tr[i][:3]) for i in range(len(pcamodel_tr))]
  sum_squares, attributes = zip(*sorted(zip(most_important, df.columns), reverse=True))
  result = list(attributes[:3])
  return result




def scatter_plot(pca):
  #plt.scatter(pca[:, 0], pca[:, 1])
  return pca[:, 0], pca[:, 1]

def scatter_plot_pca(df):
  pcamodel, pca = get_pca(df)
  return scatter_plot(pca)

def scatter_plot_mds_euc(df):
  dissimilarity_distance_matrix = sklearn.metrics.pairwise.pairwise_distances(sk_normalize(df), metric='euclidean')
  mds = sklearn.manifold.MDS(n_components=2, dissimilarity='precomputed').fit_transform(dissimilarity_distance_matrix)
  return scatter_plot(mds)

def scatter_plot_mds_corr(df):
  dissimilarity_distance_matrix = sklearn.metrics.pairwise.pairwise_distances(sk_normalize(df), metric='correlation')
  mds = sklearn.manifold.MDS(n_components=2, dissimilarity='precomputed').fit_transform(dissimilarity_distance_matrix)
  return scatter_plot(mds)

train=pd.read_csv('train.csv')
features = ['SalePrice', 'OverallQual', 'GrLivArea' ,'GarageCars',
'OverallQual',
'YearBuilt',
'TotalBsmtSF',
'TotRmsAbvGrd',
'MSZoning',
'LotShape',
'Neighborhood',
'Condition1',
'BldgType',
'HouseStyle',
'RoofStyle',
'SaleCondition', 'Fireplaces']

df = train[features]
feature_engg(df)
df_sample = compute_sample(df)
df_stratified = compute_stratified(df, 4)
warnings.filterwarnings("ignore", category=DeprecationWarning)
####Todo
# 1. show elbow in d3
# Normalize? how.. sk_normalize seems better
## bias ?? introduced...what? I think its less
## three attributes -- show calculations?
##
