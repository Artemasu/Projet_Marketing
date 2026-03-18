from flask import Flask, render_template, request, redirect, url_for
import json
import sqlite3
import os
import pandas as pd
from simulation_logic import run_campaign_simulation

marketing = Flask(__name__)
DATABASE = 'campaign_results.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_type TEXT,
                channel TEXT,
                budget REAL,
                duration INTEGER,
                clicks INTEGER,
                impressions INTEGER,
                sales INTEGER,
                profit REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute("PRAGMA table_info(simulations)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'roi' not in columns:
            cursor.execute('ALTER TABLE simulations ADD COLUMN roi REAL DEFAULT 0')
        if 'panier_moyen' not in columns:
            cursor.execute('ALTER TABLE simulations ADD COLUMN panier_moyen REAL DEFAULT 0')
        conn.commit()

init_db()

@marketing.route('/')
def index():
    return render_template('index.html')

@marketing.route('/simulate', methods=['POST'])
def simulate():
    product = request.form.get('product', 'e-commerce')
    channel = request.form.get('channel', 'facebook')
    budget = float(request.form.get('budget', 5000))
    duration = int(request.form.get('duration', 30))

    sim_results = run_campaign_simulation(product, channel, budget, duration)
    
    try:
        df_insights = pd.read_csv('market_insights.csv')
        channel_comparison = {
            'channels': df_insights['channel'].tolist(),
            'sales': [round(val * 100, 2) for val in df_insights['avg_conv_rate'].tolist()]
        }
    except:
        channel_comparison = {'channels': ['ad', 'psa'], 'sales': [2.55, 1.79]}
    
    sim_results['charts_data']['channel_comparison'] = channel_comparison

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO simulations (product_type, channel, budget, duration, clicks, impressions, sales, profit, roi, panier_moyen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product, channel, budget, duration, sim_results['clicks'], sim_results['impressions'], 
                  sim_results['sales'], sim_results['profit'], sim_results['roi'], sim_results['panier_moyen']))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur DB insertion: {e}")

    results = {
        **sim_results,
        'charts_data_json': json.dumps(sim_results['charts_data'])
    }

    return render_template('results.html', results=results, request=request)

@marketing.route('/history')
def history():
    simulations = []
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM simulations ORDER BY timestamp DESC')
            simulations = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur historique: {e}")
    return render_template('history.html', simulations=simulations)

@marketing.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM simulations')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur suppression: {e}")
    return redirect(url_for('history'))

if __name__ == '__main__':
    marketing.run(debug=True)