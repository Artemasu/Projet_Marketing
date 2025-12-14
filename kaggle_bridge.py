import pandas as pd

def analyze_kaggle_data(csv_file):
    print(f"Lecture de {csv_file}...")
    df = pd.read_csv(csv_file)

    df.columns = df.columns.str.strip().str.replace(' ', '_')
    print(f"Colonnes détectées : {list(df.columns)}")

    summary = df.groupby('test_group').agg({
        'converted': 'mean',  
        'total_ads': 'mean'  
    }).reset_index()

    summary.rename(columns={'test_group': 'channel', 'converted': 'avg_conv_rate'}, inplace=True)
    
    costs = {'ad': 0.75, 'psa': 0.05} 
    summary['avg_cpc'] = summary['channel'].map(costs)

    summary.to_csv('market_insights.csv', index=False)
    print("✅ Succès ! Fichier 'market_insights.csv' généré avec les données réelles.")

if __name__ == "__main__":
    analyze_kaggle_data('marketing_AB.csv')