from flask import Flask, render_template, request
import json
from simulation_logic import run_campaign_simulation # <-- NOUVEAU
import sqlite3 # <-- NOUVEAU

# Le nom de l'application Flask correspond au nom du fichier
marketing = Flask(__name__)
DATABASE = 'campaign_results.db' # <-- NOUVEAU : Nom de la base de données

# NOUVEAU : Fonction pour initialiser la base de données
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_type TEXT NOT NULL,
                channel TEXT NOT NULL,
                budget REAL NOT NULL,
                duration INTEGER NOT NULL,
                clicks REAL NOT NULL,
                impressions REAL NOT NULL,
                sales REAL NOT NULL,
                profit REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# NOUVEAU : Appel à l'initialisation de la DB au démarrage de l'app
with marketing.app_context():
    init_db()

@marketing.route('/')
def index():
    # Cette route affiche le formulaire de configuration de la campagne
    return render_template('index.html')

@marketing.route('/simulate', methods=['POST'])
def simulate():
    # Récupérer les données du formulaire
    product = request.form['product']
    channel = request.form['channel']
    budget = float(request.form['budget'])
    duration = int(request.form['duration'])

    # --- UTILISATION DE LA NOUVELLE LOGIQUE DE SIMULATION ---
    simulation_results = run_campaign_simulation(product, channel, budget, duration)
    # --- FIN DE LA NOUVELLE LOGIQUE DE SIMULATION ---

    # Récupérer les métriques principales de la simulation
    clicks = simulation_results['clicks']
    impressions = simulation_results['impressions']
    sales = simulation_results['sales']
    profit = simulation_results['profit']

    # Données pour le graphique "Performance Over Time"
    performance_labels = simulation_results['charts_data']['performance_over_time']['labels']
    performance_clicks = simulation_results['charts_data']['performance_over_time']['clicks']
    performance_sales = simulation_results['charts_data']['performance_over_time']['sales']
    performance_profit = simulation_results['charts_data']['performance_over_time']['profit']

    # Données pour le graphique "Channel Comparison" (peut rester ici pour l'instant)
    # NOTE: Pour une comparaison plus réaliste, cette partie devrait aussi être dans la logique
    # de simulation si vous voulez simuler tous les canaux pour une comparaison directe.
    channel_sales = {
        'Facebook': int(sales * 0.8 if channel == 'facebook' else sales * 0.2),
        'Instagram': int(sales * 0.7 if channel == 'instagram' else sales * 0.25),
        'Google': int(sales * 1.2 if channel == 'google' else sales * 0.3),
        'TikTok': int(sales * 0.9 if channel == 'tiktok' else sales * 0.15),
    }

    results = {
        'clicks': clicks,
        'impressions': impressions,
        'sales': sales,
        'profit': profit,
        'charts_data': {
            'performance_over_time': {
                'labels': performance_labels,
                'clicks': performance_clicks,
                'sales': performance_sales,
                'profit': performance_profit,
            },
            'channel_comparison': {
                'channels': list(channel_sales.keys()),
                'sales': list(channel_sales.values())
            }
        }
    }
    
    # Sérialiser les données des graphiques en JSON pour les passer au frontend
    results['charts_data_json'] = json.dumps(results['charts_data'])

    # NOUVEAU : Sauvegarder les résultats dans la base de données
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO simulations (product_type, channel, budget, duration, clicks, impressions, sales, profit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product, channel, budget, duration, clicks, impressions, sales, profit))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion dans la base de données : {e}")


    # Rendre le template des résultats avec les données de la simulation
    return render_template('results.html', results=results, request=request)

# NOUVEAU : Route pour afficher l'historique des simulations
@marketing.route('/history')
def history():
    simulations = []
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM simulations ORDER BY timestamp DESC')
            simulations = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération de l'historique : {e}")
    
    return render_template('history.html', simulations=simulations)


if __name__ == '__main__':
    # Lancer l'application en mode debug (rechargement automatique)
    marketing.run(debug=True)