import random

def run_campaign_simulation(product_type, channel, budget, duration):
    """
    Simule une campagne de marketing digital avec des facteurs plus réalistes
    basés sur le type de produit et le canal.
    """

    # Coefficients de base (peuvent être ajustés avec des données réelles/synthétiques)
    base_cpc = { # Coût par clic moyen (€)
        'facebook': 0.8,
        'instagram': 0.9,
        'google': 1.5,
        'tiktok': 0.6
    }
    base_conversion_rate = { # Taux de conversion moyen (en %)
        'e-commerce': 0.02, # 2%
        'saas': 0.01,       # 1%
        'app': 0.03,        # 3%
        'local': 0.025      # 2.5%
    }
    base_aov = { # Average Order Value / Valeur moyenne par vente (€)
        'e-commerce': 60,
        'saas': 120,
        'app': 10, # Les revenus d'une app peuvent être plus faibles par vente unitaire
        'local': 80
    }

    # Ajustement des coefficients par canal et type de produit (exemple)
    cpc_multiplier = 1.0
    conversion_multiplier = 1.0
    aov_multiplier = 1.0

    # Impact du canal sur le CPC (exemple : Google est plus cher)
    cpc = base_cpc.get(channel, 1.0) * cpc_multiplier

    # Impact du type de produit sur le taux de conversion et la valeur moyenne
    conversion_rate = base_conversion_rate.get(product_type, 0.015) * conversion_multiplier
    aov = base_aov.get(product_type, 75) * aov_multiplier

    # Simulation journalière pour un meilleur suivi de la performance
    daily_data = []
    total_clicks = 0
    total_impressions = 0
    total_sales = 0
    total_profit = 0

    # Simulation sur la durée spécifiée
    for day in range(1, duration + 1):
        # Budget quotidien (simplifié, pourrait être réparti différemment)
        daily_budget = budget / 30 # Convertir budget mensuel en quotidien
        
        # Le budget quotidien influence les clics
        daily_clicks = (daily_budget / cpc) * (1 + random.uniform(-0.1, 0.1)) # Ajout d'une petite variabilité
        daily_clicks = max(1, daily_clicks) # Au moins 1 clic
        
        daily_impressions = daily_clicks * random.uniform(8, 12) # Ratio impressions/clics
        
        daily_sales = daily_clicks * conversion_rate * (1 + random.uniform(-0.15, 0.15))
        daily_sales = round(daily_sales) # Nombre entier de ventes
        
        daily_revenue = daily_sales * aov
        daily_cost = daily_budget # Pour simplifier, le coût est le budget dépensé
        daily_profit = daily_revenue - daily_cost

        total_clicks += daily_clicks
        total_impressions += daily_impressions
        total_sales += daily_sales
        total_profit += daily_profit

        daily_data.append({
            'day': day,
            'clicks': total_clicks, # Cumulatif
            'impressions': total_impressions, # Cumulatif
            'sales': total_sales, # Cumulatif
            'profit': total_profit # Cumulatif
        })

    # Données pour les graphiques "Performance Over Time"
    performance_labels = [f"Day {d['day']}" for d in daily_data]
    performance_clicks = [d['clicks'] for d in daily_data]
    performance_sales = [d['sales'] for d in daily_data]
    performance_profit = [d['profit'] for d in daily_data]

    # Données pour le graphique "Channel Comparison" (fixe pour l'exemple, mais pourrait être dynamique)
    # Pour le moment, nous allons laisser la logique de comparaison des canaux dans marketing.py
    # ou nous pourrions l'intégrer ici plus tard avec des calculs distincts pour chaque canal.

    results = {
        'clicks': total_clicks,
        'impressions': total_impressions,
        'sales': total_sales,
        'profit': total_profit,
        'charts_data': {
            'performance_over_time': {
                'labels': performance_labels,
                'clicks': performance_clicks,
                'sales': performance_sales,
                'profit': performance_profit,
            },
            # 'channel_comparison' sera géré dans marketing.py pour le moment
        }
    }
    
    return results