#!/usr/bin/env python3

from flask import Flask, abort, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    #Give them index.html
    return render_template('index.html')

@app.route('/combatant/')
@app.route('/combatant/<identifier>')
def combatant(identifier=None):
    #give them combatants.html
    return render_template('combatants.html')

@app.route('/battle/')
@app.route('/battle/<identifier>')
def battle(identifier=None):
    #Give them battle.html
    return render_template('battle.html')

@app.route('/results/')
def results():
    #call results.html
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=False, port=8056)
    


