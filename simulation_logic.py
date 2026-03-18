import pandas as pd
import numpy as np

def run_campaign_simulation(product_type, channel, budget, duration):
    # 1. RÉCUPÉRATION DES DONNÉES DE MARCHÉ
    try:
        market_df = pd.read_csv('market_insights.csv')
        stats = market_df[market_df['channel'] == 'ad'].iloc[0]
        base_cpc = stats['avg_cpc']
        base_conv_rate = stats['avg_conv_rate']
    except:
        base_cpc, base_conv_rate = 0.8, 0.02

    # 2. PANIER MOYEN SELON LE PRODUIT
    aov_map = {'e-commerce': 60, 'saas': 150, 'app': 15, 'local': 100}
    panier_moyen = aov_map.get(product_type.lower(), 50)

    # 3. SIMULATION RÉELLE
    daily_budget = budget / duration
    performance_labels, performance_clicks, performance_sales, performance_profit = [], [], [], []
    cum_clicks, cum_sales, cum_profit = 0, 0, 0

    for day in range(1, duration + 1):
        daily_cpc = base_cpc * np.random.uniform(0.95, 1.05)
        day_clicks = np.random.poisson(daily_budget / daily_cpc)
        day_sales = np.random.binomial(day_clicks, base_conv_rate)
        day_profit = (day_sales * panier_moyen) - daily_budget
        
        cum_clicks += day_clicks
        cum_sales += day_sales
        cum_profit += day_profit
        
        performance_labels.append(f"Day {day}")
        performance_clicks.append(int(cum_clicks))
        performance_sales.append(int(cum_sales))
        performance_profit.append(int(cum_profit))

    final_roi = (cum_profit / budget) * 100 if budget > 0 else 0

    # 4. ALGORITHME DE RECOMMANDATION (CORRIGÉ POUR ÉVITER LE TYPEERROR)
    best_profit = -float('inf')
    rec_budget, rec_days = budget, duration

    # On s'assure que les bornes de range sont des entiers avec int()
    limit_duration = int(duration)
    limit_budget = int(budget)

    for test_d in range(7, limit_duration + 1):
        # On teste par paliers de 50€, en forçant l'entier pour range()
        start_b = int(min(100, limit_budget))
        for test_b in range(start_b, limit_budget + 1, 50):
            
            t_clicks = test_b / base_cpc
            t_sales = t_clicks * base_conv_rate
            t_profit = (t_sales * panier_moyen) - test_b
            
            if t_profit > best_profit:
                best_profit = t_profit
                rec_budget = test_b
                rec_days = test_d

    rec_roi = (best_profit / rec_budget * 100) if rec_budget > 0 else 0

    return {
        'clicks': int(cum_clicks),
        'impressions': int(cum_clicks * 12),
        'sales': int(cum_sales),
        'profit': float(cum_profit),
        'roi': round(final_roi, 2),
        'panier_moyen': panier_moyen,
        'best_approach': {
            'budget': int(rec_budget),
            'days': int(rec_days),
            'expected_roi': round(rec_roi, 2)
        },
        'charts_data': {
            'performance_over_time': {
                'labels': performance_labels,
                'clicks': performance_clicks,
                'sales': performance_sales,
                'profit': performance_profit
            }
        }
    }