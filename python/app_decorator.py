import app_logic

features = ['SalePrice', 'OverallQual', 'GrLivArea' ,'GarageCars', 'OverallQual', 'YearBuilt',
'TotalBsmtSF', 'TotRmsAbvGrd', 'MSZoning', 'LotShape', 'Neighborhood',  'Condition1',
'BldgType', 'HouseStyle', 'RoofStyle', 'SaleCondition', 'Fireplaces']

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

def get_scatter_plot_pca(df):
  x1, x2 = app_logic.scatter_plot_pca(df[features])
  body = {
    "x1": list(x1),
    "x2": list(x2),
    "cluster": list(df['cluster'] if 'cluster' in df.columns else [0] * len(df))
  }
  return body

def get_scatter_plot_mds(df, metric):
  if metric == 'euclidean':
    x1, x2 = app_logic.scatter_plot_mds_euc(df[features])
  else:
    x1, x2 = app_logic.scatter_plot_mds_corr(df[features])
  body = {
    "x1": list(x1),
    "x2": list(x2),
    "cluster": list(df['cluster'] if 'cluster' in df.columns else [0] * len(df))
  }
  return body