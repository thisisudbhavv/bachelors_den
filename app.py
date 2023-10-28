from flask import Flask, jsonify, render_template, request
from database import load_home, load_homes, add_apply

app = Flask(__name__)


@app.route('/')
def hello_world():
  homes = load_homes()
  return render_template('home.html', homes=homes)


@app.route('/api/homes')
def list_homes():
  return jsonify(load_homes())


@app.route('/home/<id>')
def show_home(id):
  home = load_home(id)
  if not home:
    return "Home not found", 404
  return render_template('jobpage.html', home=home)

@app.route('/api/home/<id>')
def show_homes(id):
  home = load_home(id)
  return jsonify(home)

@app.route('/home/<id>/apply', methods=['post'])
def apply_home(id):
  data = request.form
  home = load_home(id)
  add_apply(id, data)
  return render_template("application_submit.html", apply=data, home=home)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)