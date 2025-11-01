from flask import Flask, render_template, request
import json # Pour passer les données des graphiques en JSON

# Le nom de l'application Flask correspond au nom du fichier
marketing = Flask(__name__)

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

    # --- DÉBUT DE LA LOGIQUE DE SIMULATION FICTIVE ---
    # Ces chiffres sont TRÈS BASIQUES et seront remplacés par une logique réelle plus tard
    
    # Métriques principales
    clicks = budget * 2.5 * (duration / 30)
    impressions = clicks * 10
    sales = clicks * 0.05
    profit = sales * 50 - budget

    # Données pour le graphique "Performance Over Time"
    performance_labels = [f"Day {i+1}" for i in range(duration)]
    performance_clicks = [int(clicks / duration * (i+1)) for i in range(duration)]
    performance_sales = [int(sales / duration * (i+1)) for i in range(duration)]
    performance_profit = [int(profit / duration * (i+1)) for i in range(duration)]

    # Données pour le graphique "Channel Comparison"
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
    # --- FIN DE LA LOGIQUE DE SIMULATION FICTIVE ---

    # Rendre le template des résultats avec les données de la simulation
    return render_template('results.html', results=results, request=request)

if __name__ == '__main__':
    # Lancer l'application en mode debug (rechargement automatique)
    marketing.run(debug=True)