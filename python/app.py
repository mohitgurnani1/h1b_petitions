from flask import Flask, jsonify, request, send_from_directory
import app_logic, app_decorator

app = Flask(__name__)
import json


@app.route('/data/<data>/feature/<feature>/job')
def barchart_job(data, feature):
  df = get_data(data)
  if 'syear' in request.args:
    s, e = app_logic.get_year(request.args['syear'], request.args['eyear'])
    df = app_logic.reduce_df(df, s, e)
  key = None
  value = None
  if 'state' in request.args:
    key = 'state'
    value = request.args['state']
  elif 'job' in request.args:
    key = 'job'
    value = request.args['job']
  elif 'employer' in request.args:
    key = 'employer'
    value = request.args['employer']
  if feature == 'petitions':
    result = jsonify(app_decorator.get_petitions_jobs(df, key, value))
  elif feature == 'petitions-success-ratio':
    result = jsonify(app_decorator.get_scatter_plot_pca(df))
  elif feature == 'wages':
    result = jsonify(app_decorator.get_wages_jobs(df, key, value))

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result


@app.route('/data/<data>/feature/<feature>/employer')
def barchart_horizontal_employers(data, feature):
  df = get_data(data)
  if 'syear' in request.args:
    s, e = app_logic.get_year(request.args['syear'], request.args['eyear'])
    df = app_logic.reduce_df(df, s, e)
  key = None
  value = None
  if 'state' in request.args:
    key = 'state'
    value = request.args['state']
  elif 'job' in request.args:
    key = 'job'
    value = request.args['job']
  elif 'employer' in request.args:
    key = 'employer'
    value = request.args['employer']
  if feature == 'petitions':
    result = jsonify(app_decorator.get_petitions_employers(df,  key, value ))
  elif feature == 'wages':
    result = jsonify(app_decorator.get_wages_employers(df, key, value))

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result



@app.route('/data/<data>/feature/<feature>/jobstacked', methods=['GET'])
def grouped_stacked_barchart_job(data, feature):
  df = get_data(data)
  #result = app_logic.job_petition_success_ratio(df, feature)
  if feature == 'wages':
    result = send_from_directory('sample', 'wagesstacked.csv', as_attachment=True)
  elif feature == 'petitions':
    result = send_from_directory('sample', 'petitionsstatus.csv', as_attachment=True)
  else:
    result = send_from_directory('sample', 'geomap.csv', as_attachment=True)
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

@app.route('/data/<data>/feature/<feature>/geolegend', methods=['GET'])
def geomap_legend(data, feature):
  df = get_data(data)
  if 'syear' in request.args:
    s, e = app_logic.get_year(request.args['syear'], request.args['eyear'])
    df = app_logic.reduce_df(df, s, e)
  key = None
  value = None
  if 'state' in request.args:
    key = 'state'
    value = request.args['state']
  elif 'job' in request.args:
    key = 'job'
    value = request.args['job']
  elif 'employer' in request.args:
    key = 'employer'
    value = request.args['employer']
  if feature == 'petitions':
    result = jsonify(app_decorator.geo_legend_petitions(df, key, value))
  elif feature == 'wages':
    result = jsonify(app_decorator.geo_legend_wages(df, key, value))

  result.headers.add('Access-Control-Allow-Origin', '*')
  return result


@app.route('/data/<data>/feature/<feature>/geomap', methods=['GET'])
def geomap(data, feature):
  df = get_data(data)
  if 'syear' in request.args:
    s, e = app_logic.get_year(request.args['syear'], request.args['eyear'])
    df = app_logic.reduce_df(df, s, e)
  key = None
  value = None
  if 'state' in request.args:
    key = 'state'
    value = request.args['state']
  elif 'job' in request.args:
    key = 'job'
    value = request.args['job']
  elif 'employer' in request.args:
    key = 'employer'
    value = request.args['employer']
  if feature == 'petitions':
    result = app_logic.geo_map_petitions(df, key, value)
  elif feature == 'wages':
    result = app_logic.geo_map_wages(df, key, value)

  result.to_csv('sample/state.csv', index=False)
  result = send_from_directory('sample', 'state.csv', as_attachment=True)
  result.headers.add('Access-Control-Allow-Origin', '*')
  return result

@app.route('/data/json')
def statejson():
  result = send_from_directory('sample', 'us-states.json', as_attachment=True)
  result.headers.add('Access-Control-Allow-Origin', '*')
  return result

@app.route('/random')
def random():
  result = send_from_directory('sample', 'timeline.csv', as_attachment=True)
  result.headers.add('Access-Control-Allow-Origin', '*')
  return result


@app.route('/random2')
def random2():
  result = send_from_directory('sample', 'pc.csv', as_attachment=True)
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