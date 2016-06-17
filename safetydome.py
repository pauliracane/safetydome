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
        #If no identifier was passed, pull all combatants
        cur.execute('SELECT combatant.name, combatant.id, species.name FROM public.combatant, public.species WHERE combatant.species_id = species.id;')
        combatants = cur.fetchall()

    elif (identifier.isnumeric()):
        #If a numeric identifier was passed, pull combatant X
        cur.execute('SELECT combatant.name, combatant.id, species.name FROM public.combatant, public.species WHERE combatant.species_id = %s AND combatant.species_id = species.id;', identifier)
        combatants = cur.fetchall()

    else:
        #If a non-numeric identifier was passed, URL Not found.
        abort(404)

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
@app.route('/battle/<identifier1>-<identifier2>')
def battle(identifier1=None, identifier2=None):
    #Give them battle.html
    if (identifier1 == None or identifier2 == None):
        cur.execute("SELECT fight.combatant_one, fight.combatant_two, fight.winner, (select combatant.name from public.combatant WHERE combatant.id = fight.combatant_one),(SELECT combatant.name from public.combatant WHERE combatant.id = fight.combatant_two) FROM public.fight, public.combatant")
        fight = cur.fetchall()
        
    elif (identifier1.isnumeric() and identifier2.isnumeric()):
        cur.execute("SELECT fight.combatant_one, fight.combatant_two, fight.winner, (select combatant.name from public.combatant WHERE combatant.id = fight.combatant_one),(SELECT combatant.name from public.combatant WHERE combatant.id = fight.combatant_two) FROM public.fight, public.combatant WHERE fight.combatant_one = %s and fight.combatant_two = %s", [identifier1, identifier2])
        fight = cur.fetchall()
    else:
        abort(404)

    class Fight:
        def __init__(self, one_id, one_name, two_id, two_name, winner):
            self.one_id = one_id
            self.one_name = one_name
            self.two_id = two_id
            self.two_name = two_name
            self.winner = winner
    
    TheFightList = []
    for each in fight:
        x = Fight(each[0], each[3], each[1], each[4], each[2])
        TheFightList.append(x)

    return render_template('battle.html', fights = TheFightList)

@app.route('/results/')
def results():
    #call results.html
    return render_template('results.html')

if __name__ == '__main__':
    #Connect to database
    app.run(debug=True, port=8056)


