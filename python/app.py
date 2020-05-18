from flask import Flask, jsonify, request, send_from_directory
import app_logic, app_decorator

app = Flask(__name__)
import json


@app.route('/data/<data>/feature/<feature>/job')
def barchart_job(data, feature):
  df = get_data(data)
  if feature == 'petitions':
    result = jsonify(app_decorator.get_petitions_jobs(df))
  elif feature == 'petitions-success-ratio':
    result = jsonify(app_decorator.get_scatter_plot_pca(df))
  elif feature == 'wages':
    result = jsonify(app_decorator.get_wages_jobs(df))

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result


@app.route('/data/<data>/feature/<feature>/employer')
def barchart_horizontal_employers(data, feature):
  df = get_data(data)
  if feature == 'petitions':
    result = jsonify(app_decorator.get_petitions_employers(df))
  elif feature == 'petitions-success-ratio':
    result = jsonify(app_decorator.get_scatter_plot_pca(df))
  elif feature == 'wages':
    result = jsonify(app_decorator.get_wages_employers(df))

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result

@app.route('/data/<data>/feature/<feature>')
def scatterplot(data, feature):
  df = get_data(data)
  if feature == 'pca':
    result = jsonify(app_decorator.get_scatter_plot_pca(df))
  elif feature == 'mds':
    result = jsonify(app_decorator.get_scatter_plot_mds(df))
  elif feature =='histogram':
    result = jsonify(app_decorator.get_histogram(df))

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result



@app.route('/data/<data>/feature/<feature>/geomap', methods=['GET'])
def statecsv(data, feature):
  df = get_data(data)
  if feature == 'petitions':
    result = app_logic.geo_map_petitions(df)
  elif feature == 'wages':
    result = app_logic.geo_map_wages(df)

  result.to_csv('sample/state.csv', index=False)
  result = send_from_directory('sample', 'state.csv', as_attachment=True)
  result.headers.add('Access-Control-Allow-Origin', '*')
  return result

@app.route('/data/json')
def statejson():
  result = send_from_directory('sample', 'us-states.json', as_attachment=True)
  result.headers.add('Access-Control-Allow-Origin', '*')
  return result



def get_data(data):
  if data == 'original':
    return app_logic.df
  else:
    print('sample data using')
    return app_logic.df_sample

if __name__ == '__main__':
    app.run ()