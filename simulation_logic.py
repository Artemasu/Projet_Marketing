import pandas as pd
import numpy as np

def run_campaign_simulation(product_type, channel, budget, duration):
    try:
        market_df = pd.read_csv('market_insights.csv')
        stats = market_df[market_df['channel'] == 'ad'].iloc[0]
        cpc_reel = stats['avg_cpc']
        conv_rate_reel = stats['avg_conv_rate']
    except:
        cpc_reel, conv_rate_reel = 0.8, 0.02

    aov_map = {'e-commerce': 60, 'saas': 150, 'app': 15, 'local': 100}
    panier_moyen = aov_map.get(product_type.lower(), 50)

    daily_budget = budget / duration
    performance_labels = []
    performance_clicks = []
    performance_sales = []
    performance_profit = []

    cum_clicks = 0
    cum_sales = 0
    cum_profit = 0

    for day in range(1, duration + 1):
        day_clicks = np.random.poisson(daily_budget / cpc_reel)
        
        day_sales = np.random.binomial(day_clicks, conv_rate_reel)
        
        day_profit = (day_sales * panier_moyen) - daily_budget

        cum_clicks += day_clicks
        cum_sales += day_sales
        cum_profit += day_profit

        performance_labels.append(f"Jour {day}")
        performance_clicks.append(int(cum_clicks))
        performance_sales.append(int(cum_sales))
        performance_profit.append(int(cum_profit))

    final_roi = (cum_profit / budget) * 100 if budget > 0 else 0

    best_roi = -float('inf')
    best_budget, best_days = 0, 0
    for test_budget in [1000, 3000, 5000, 10000]:
        for test_days in [7, 14, 30]:
            t_clicks = test_budget / cpc_reel
            t_sales = t_clicks * conv_rate_reel
            t_profit = (t_sales * panier_moyen) - test_budget
            t_roi = (t_profit / test_budget) * 100
            if t_roi > best_roi:
                best_roi, best_budget, best_days = t_roi, test_budget, test_days

    return {
        'clicks': int(cum_clicks),
        'impressions': int(cum_clicks * 12),
        'sales': int(cum_sales),
        'profit': float(cum_profit),
        'roi': round(final_roi, 2),
        'panier_moyen': panier_moyen,
        'best_approach': {
            'budget': best_budget,
            'days': best_days,
            'expected_roi': round(best_roi, 2)
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