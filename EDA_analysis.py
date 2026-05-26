import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def run_analysis(input_path="data/ecommerce_sales_cleaned.csv", plot_dir="plots", json_output="dashboard/data_summary.json"):
    print("Running exploratory data analysis...")
    df = pd.read_csv(input_path)
    

    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(os.path.dirname(json_output), exist_ok=True)

    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16
    })
    

    print("Generating spend distribution plot...")
    plt.figure(figsize=(10, 5))
    sns.histplot(df['Total_Spend'], color='red', alpha=0.4, kde=True, label='Raw Total Spend (with Outliers)')
    sns.histplot(df['Total_Spend_Cleaned'], color='teal', alpha=0.6, kde=True, label='Cleaned Total Spend (IQR Capped)')
    plt.title('Distribution of Total Spend: Raw vs. Cleaned', pad=15)
    plt.xlabel('Spend ($)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'spend_distribution.png'), dpi=150)
    plt.close()
 
    print("Generating spend vs age plot...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df, 
        x='Age', 
        y='Total_Spend_Cleaned', 
        hue='Membership_Level', 
        hue_order=['Bronze', 'Silver', 'Gold', 'Premium'],
        palette='viridis', 
        alpha=0.7, 
        edgecolor=None
    )
   
    sns.regplot(data=df, x='Age', y='Total_Spend_Cleaned', scatter=False, color='darkred', line_kws={"linewidth": 2, "linestyle": "--"})
    plt.title('Total Spend vs. Age by Membership Level', pad=15)
    plt.xlabel('Customer Age')
    plt.ylabel('Cleaned Total Spend ($)')
    plt.legend(title='Membership Level')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'spend_vs_age.png'), dpi=150)
    plt.close()
   
    print("Generating churn vs satisfaction plot...")
    plt.figure(figsize=(9, 5))
    sns.boxplot(
        data=df, 
        x='Churn_Status', 
        y='Average_Rating', 
        palette={0: 'teal', 1: 'coral'},
        hue='Churn_Status',
        legend=False
    )
    plt.title('Customer Satisfaction Rating by Churn Status', pad=15)
    plt.xlabel('Churn Status (0 = Active, 1 = Churned)')
    plt.ylabel('Average Rating (1-5)')
    plt.xticks([0, 1], ['Active (Retained)', 'Churned'])
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'churn_vs_satisfaction.png'), dpi=150)
    plt.close()
    
    
    print("Generating membership vs spend plot...")
    plt.figure(figsize=(9, 5))
    sns.violinplot(
        data=df, 
        x='Membership_Level', 
        y='Total_Spend_Cleaned', 
        order=['Bronze', 'Silver', 'Gold', 'Premium'],
        palette='muted',
        hue='Membership_Level',
        legend=False
    )
    plt.title('Total Spend Distribution by Membership Level', pad=15)
    plt.xlabel('Membership Level')
    plt.ylabel('Cleaned Spend ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'membership_vs_spend.png'), dpi=150)
    plt.close()
    
  
    print("Generating correlation matrix...")
    plt.figure(figsize=(8, 6))
    numerical_cols = ['Age', 'Total_Spend_Cleaned', 'Items_Purchased', 'Average_Rating', 'Discount_Applied', 'Churn_Status']
    corr_matrix = df[numerical_cols].corr()
    
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f", 
        linewidths=0.5, 
        vmin=-1, 
        vmax=1
    )
    plt.title('Correlation Matrix of Customer Metrics', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'correlation_heatmap.png'), dpi=150)
    plt.close()

    print("Computing metrics and statistics...")
  
    total_customers = len(df)
    churn_rate = float(df['Churn_Status'].mean())
    avg_spend = float(df['Total_Spend_Cleaned'].mean())
    avg_rating = float(df['Average_Rating'].mean())
    avg_age = float(df['Age'].mean())
    total_revenue = float(df['Total_Spend_Cleaned'].sum())
    

    def get_breakdown(column):
        grouped = df.groupby(column).agg(
            Count=('Customer_ID', 'count'),
            Avg_Spend=('Total_Spend_Cleaned', 'mean'),
            Churn_Rate=('Churn_Status', 'mean')
        )
   
        grouped['Avg_Spend'] = grouped['Avg_Spend'].round(2)
        grouped['Churn_Rate'] = grouped['Churn_Rate'].round(4)
        return grouped.to_dict(orient='index')
        
    membership_breakdown = get_breakdown('Membership_Level')
    gender_breakdown = get_breakdown('Gender')
    location_breakdown = get_breakdown('Location')
    category_breakdown = get_breakdown('Preferred_Category')
    
 
    df['Age_Group'] = pd.cut(df['Age'], bins=[18, 30, 45, 60, 80], labels=['18-30', '31-45', '46-60', '61-80'])
    age_breakdown = get_breakdown('Age_Group')
   
    age_hist, age_bins = np.histogram(df['Age'], bins=12)
    age_distribution = {
        "labels": [f"{int(age_bins[i])}-{int(age_bins[i+1])}" for i in range(len(age_bins)-1)],
        "values": age_hist.tolist()
    }
    
  
    spend_hist, spend_bins = np.histogram(df['Total_Spend_Cleaned'], bins=15)
    spend_distribution = {
        "labels": [f"${int(spend_bins[i])}-{int(spend_bins[i+1])}" for i in range(len(spend_bins)-1)],
        "values": spend_hist.tolist()
    }
   
    corr_json = {}
    for col1 in corr_matrix.columns:
        corr_json[col1] = {}
        for col2 in corr_matrix.columns:
            corr_json[col1][col2] = round(float(corr_matrix.loc[col1, col2]), 3)
            
  
    sample_records = df.head(50).copy()

    for col in sample_records.columns:
        if sample_records[col].dtype.name == 'category' or isinstance(sample_records[col].dtype, pd.CategoricalDtype):
            sample_records[col] = sample_records[col].astype(str)

    sample_records = sample_records.fillna("N/A")
    sample_data = sample_records.to_dict(orient='records')
    
    summary_data = {
        "metadata": {
            "total_records": total_customers,
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "kpis": {
            "total_customers": total_customers,
            "churn_rate": round(churn_rate * 100, 2),
            "avg_spend": round(avg_spend, 2),
            "avg_rating": round(avg_rating, 2),
            "avg_age": round(avg_age, 1),
            "total_revenue": round(total_revenue, 2)
        },
        "distributions": {
            "age": age_distribution,
            "spend": spend_distribution
        },
        "breakdowns": {
            "membership": membership_breakdown,
            "gender": gender_breakdown,
            "location": location_breakdown,
            "category": category_breakdown,
            "age_group": age_breakdown
        },
        "correlation": corr_json,
        "samples": sample_data
    }
    
    with open(json_output, 'w') as f:
        json.dump(summary_data, f, indent=4)
        
    js_output = json_output.replace('.json', '.js')
    with open(js_output, 'w') as f:
        f.write(f"const DATA_SUMMARY = {json.dumps(summary_data, indent=4)};\n")
        
    print(f"Analysis completed. Summary statistics saved in JSON to {json_output}")
    print(f"Visualizations saved to {plot_dir}/")
    
if __name__ == "__main__":
    run_analysis()
