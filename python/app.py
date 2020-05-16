from flask import Flask, jsonify, request, send_from_directory
import app_logic, app_decorator

app = Flask(__name__)
import json



UPLOAD_DIRECTORY = "top3/"

features = ['SalePrice', 'OverallQual', 'GrLivArea' ,'GarageCars', 'OverallQual', 'YearBuilt',
'TotalBsmtSF', 'TotRmsAbvGrd', 'MSZoning', 'LotShape', 'Neighborhood',  'Condition1',
'BldgType', 'HouseStyle', 'RoofStyle', 'SaleCondition', 'Fireplaces']

@app.route('/data/<data>/feature/<feature>')
def hello_name(data, feature):

  df = get_data(data)
  if feature == 'screeplot':
    result = jsonify(app_decorator.get_scree_plot(df))
  elif feature == 'scatterplot-pca':
    result = jsonify(app_decorator.get_scatter_plot_pca(df))
  elif feature == 'mds':
    if 'metric' in request.args:
        result = jsonify(app_decorator.get_scatter_plot_mds(df, request.args['metric']))
  elif feature == 'top-3':
    result = jsonify(app_logic.top_3_names(df[features]))
  elif feature == 'scatterplot-matrix':
    result = app_logic.top_3_attributes(df[features])
    result["cluster"] = list(df['cluster'] if 'cluster' in df.columns else [0] * len(df))
    result.to_csv('top3/temp.csv', index = False)
    result = send_from_directory(UPLOAD_DIRECTORY, 'temp.csv', as_attachment=True)

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result

def get_data(data):
  if data == 'orig':
    return app_logic.df
  elif data == 'sampled':
    return app_logic.df_sample
  else:
    return app_logic.df_stratified

if __name__ == '__main__':
    app.run ()