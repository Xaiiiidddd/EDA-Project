import os
import pandas as pd
import numpy as np
def clean_data(input_path="data/ecommerce_sales.csv", output_path="data/ecommerce_sales_cleaned.csv"):
    print("Loading raw dataset...")
    df = pd.read_csv(input_path)
    initial_shape = df.shape
    print(f"Original dataset shape: {initial_shape}")
    
    print("\n--- Checking Missing Values ---")
    missing_before = df.isnull().sum()
    print(missing_before[missing_before > 0])

    median_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(median_age)
    print(f"Imputed missing Age values with median age: {median_age:.1f}")
    

    print("\n--- Standardizing Last Purchase Date ---")
    
    def parse_date(date_str):
        if pd.isna(date_str):
            return np.nan
        date_str = str(date_str).strip()
 
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%B %d, %Y"):
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
  
        try:
            return pd.to_datetime(date_str)
        except:
            return np.nan
 
    parsed_dates = df['Last_Purchase_Date'].apply(parse_date)
    unparsed_count = parsed_dates.isna().sum()
    if unparsed_count > 0:
        print(f"Warning: Could not parse {unparsed_count} dates.")
        
    df['Last_Purchase_Date'] = parsed_dates.dt.strftime('%Y-%m-%d')
    print("Standardized all dates to YYYY-MM-DD format.")
    
  
    print("\n--- Handling Outliers in Total_Spend ---")
    q1 = df['Total_Spend'].quantile(0.25)
    q3 = df['Total_Spend'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = max(0, q1 - 1.5 * iqr) 
    upper_bound = q3 + 1.5 * iqr
    
    outliers = df[(df['Total_Spend'] < lower_bound) | (df['Total_Spend'] > upper_bound)]
    print(f"Detected {len(outliers)} outliers in Total_Spend (using IQR rule: Bounds [{lower_bound:.2f}, {upper_bound:.2f}])")
  
    df['Is_Outlier'] = 0
    df.loc[outliers.index, 'Is_Outlier'] = 1
    

    df['Total_Spend_Cleaned'] = df['Total_Spend'].clip(lower_bound, upper_bound)
    print(f"Created 'Total_Spend_Cleaned' column where outliers are capped at {upper_bound:.2f}")
    
 
    print("\n--- Validating Cleaned Data ---")
    missing_after = df.isnull().sum().sum()
    print(f"Total missing values after cleaning: {missing_after}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset exported to {output_path}")
    print(f"Final shape: {df.shape}")
    
    return {
        'initial_shape': initial_shape,
        'final_shape': df.shape,
        'missing_imputed': int(missing_before['Age']),
        'outliers_capped': len(outliers)
    }
if __name__ == "__main__":
    clean_data()
