#!/usr/bin/env python3

from flask import Flask, abort, request, render_template
import psycopg2

app = Flask(__name__)

con = psycopg2.connect("dbname='safetydome' user='flask' password='flask' host='localhost'")
cur = con.cursor()

@app.route('/')
def index():
    #Give them index.html
    return render_template('index.html')

@app.route('/combatant/')
@app.route('/combatant/<identifier>')
def combatant(identifier=None):
    #give them combatants.html
    if (identifier == None):
        cur.execute('SELECT combatant.name, combatant.id, species.name FROM public.combatant, public.species WHERE combatant.species_id = species.id;')
        combatants = cur.fetchall()
    else:
        cur.execute('SELECT combatant.name, combatant.id, species.name FROM public.combatant, public.species WHERE combatant.species_id = %s AND combatant.species_id = species.id;', identifier)
        combatants = cur.fetchall()
    class Combatant:
        def __init__(self, name, ident, species):
            self.name = name
            self.ident = ident
            self.species = species
    TheRealCombatants = []
    for each in combatants:
        x = Combatant(each[0], each[1],each[2])
        TheRealCombatants.append(x)

    return render_template('combatants.html', combatants = TheRealCombatants)

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
    #Connect to database
    app.run(debug=True, port=8056)


