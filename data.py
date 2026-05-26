import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
def generate_dataset(num_records=1500, random_seed=42):
    np.random.seed(random_seed)
    
  
    customer_ids = [f"CUST-{1000 + i}" for i in range(num_records)]
    

    age = np.random.normal(loc=41, scale=12, size=num_records)
    age = np.clip(age, 18, 80).astype(float)

    nan_age_indices = np.random.choice(num_records, size=int(num_records * 0.05), replace=False)
    age[nan_age_indices] = np.nan
    
    genders = np.random.choice(['Male', 'Female', 'Non-Binary'], size=num_records, p=[0.48, 0.47, 0.05])
    

    locations = np.random.choice(['North', 'East', 'South', 'West'], size=num_records, p=[0.3, 0.25, 0.25, 0.2])
    

    membership_levels = np.random.choice(['Bronze', 'Silver', 'Gold', 'Premium'], size=num_records, p=[0.4, 0.3, 0.2, 0.1])
    

    base_spend = {'Bronze': 150, 'Silver': 400, 'Gold': 900, 'Premium': 2000}
    spend = []
    for m, a in zip(membership_levels, age):
        m_base = base_spend[m]
    
        age_val = a if not np.isnan(a) else 41
        a_effect = (age_val - 18) * 8
        noise = np.random.normal(0, 100)
        s = max(50.0, m_base + a_effect + noise)
        spend.append(round(s, 2))
    spend = np.array(spend)
    

    outlier_indices = np.random.choice(num_records, size=int(num_records * 0.03), replace=False)
    for idx in outlier_indices:
        spend[idx] = round(spend[idx] * np.random.uniform(3, 5), 2)
       
    items_purchased = []
    for s in spend:
        base_items = max(1, int(s / np.random.uniform(35, 60)))
        items_purchased.append(base_items)
    items_purchased = np.array(items_purchased)
    
    avg_ratings = []
    for m, s in zip(membership_levels, spend):
        m_bonus = {'Bronze': 0.0, 'Silver': 0.2, 'Gold': 0.5, 'Premium': 0.7}[m]
        s_bonus = min(0.5, s / 3000.0)
        base_rating = np.random.normal(loc=3.5 + m_bonus + s_bonus, scale=0.8)
        rating = np.clip(base_rating, 1.0, 5.0)
        avg_ratings.append(round(rating, 1))
    avg_ratings = np.array(avg_ratings)
    
    discounts = np.random.choice([0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4], size=num_records, p=[0.3, 0.2, 0.15, 0.15, 0.1, 0.07, 0.03])
    
    purchase_freq = np.random.choice(['Rare', 'Occasional', 'Frequent'], size=num_records, p=[0.35, 0.45, 0.20])
    
    pref_category = np.random.choice(['Electronics', 'Apparel', 'Home & Kitchen', 'Beauty', 'Sports'], size=num_records, p=[0.3, 0.25, 0.2, 0.15, 0.1])
    
    base_date = datetime(2025, 1, 1)
    dates = []
    for i in range(num_records):
        random_days = np.random.randint(0, 365)
        d = base_date + timedelta(days=random_days)
      
        fmt_rand = np.random.rand()
        if fmt_rand < 0.02:
            dates.append(d.strftime("%d/%m/%Y"))
        elif fmt_rand < 0.04:
            dates.append(d.strftime("%B %d, %Y"))
        else:
            dates.append(d.strftime("%Y-%m-%d"))
            
    churn_status = []
    for r, s, f in zip(avg_ratings, spend, purchase_freq):
        f_val = {'Rare': 1.0, 'Occasional': 0.0, 'Frequent': -1.2}[f]
        # x is the log-odds of churning
        x = 2.5 - 0.7 * r - 0.0003 * s + 0.8 * f_val
        p_churn = 1 / (1 + np.exp(-x))
        churn_status.append(1 if np.random.rand() < p_churn else 0)

    df = pd.DataFrame({
        'Customer_ID': customer_ids,
        'Age': age,
        'Gender': genders,
        'Location': locations,
        'Membership_Level': membership_levels,
        'Total_Spend': spend,
        'Items_Purchased': items_purchased,
        'Average_Rating': avg_ratings,
        'Discount_Applied': discounts,
        'Purchase_Frequency': purchase_freq,
        'Preferred_Category': pref_category,
        'Last_Purchase_Date': dates,
        'Churn_Status': churn_status
    })
    
    return df
if __name__ == "__main__":
    print("Generating synthetic data...")
    df = generate_dataset(1500)
   
    os.makedirs("data", exist_ok=True)
    
    output_path = os.path.join("data", "ecommerce_sales.csv")
    df.to_csv(output_path, index=False)
    print(f"Dataset generated and saved to {output_path}")
    print(f"Shape: {df.shape}")
