# Exploratory Data Analysis Report: E-Commerce Customer Behavior & Spend
Author: Zaid Ali
Date: 2026-05-26
Dataset Size: 1,500 Customers

1. Executive Summary
This report presents an Exploratory Data Analysis (EDA) of our customer sales dataset containing demographics, purchasing metrics, ratings, and subscription/churn states. The primary objective is to uncover patterns driving customer spending and identify factors that lead to customer churn.

Key Findings
Membership Tier drives Revenue: Premium and Gold subscription tiers contribute disproportionately to total spend. Premium members spend, on average, 4.5x more than Bronze members.
Satisfaction is the Churn Catalyst: A customer's rating is the single strongest indicator of churn. Retained customers maintain an average satisfaction rating of 4.0, while churned customers drop to an average of 2.6.
Outliers and Cleaning: Approximately 9.3% of the dataset's values required cleaning (imputing missing ages, standardizing mixed date formats, and capping extreme outliers in spend using the IQR method).

2. Data Quality & Preprocessing
To ensure statistical integrity, several cleaning procedures were performed:

Missing Value Imputation: The Age column was missing 75 entries (5.0%). These were successfully imputed with the median customer age of 41.6 years to prevent bias and retain rows.
Date Standardization: The column Last_Purchase_Date was formatted inconsistently (e.g., YYYY-MM-DD, DD/MM/YYYY, and text formats). All values were parsed and standardized to standard ISO format (YYYY-MM-DD).
Outlier Capping: The Total_Spend column contained 139 outliers (values above $2024.72, calculated via Q3 + 1.5 * IQR). Capping outliers rather than removing rows was critical to preserve the integrity of customer records while preventing severe skewness in our summaries.
Distribution of Total Spend: Raw vs. CleanedFigure 1: Comparison of Total Spend distribution before and after IQR outlier capping.

3. Univariate & Bivariate Insights
A. Total Spend vs. Age by Membership Level
We analyzed the correlation between customer age and total spend across the different subscription levels.

The overall dataset demonstrates a weak-to-moderate positive correlation (r≈0.35) between Age and Total Spend, showing that older customers generally spend more.
However, subscription tier segmentation is the primary driver: Premium and Gold members spend significantly more regardless of age.
Total Spend vs. Age by Membership LevelFigure 2: Scatter plot of Total Spend vs. Age, categorized by membership levels.

B. Total Spend by Membership Level
A box-and-violin plot analysis was conducted to see how total spending varies across subscription tiers.

Bronze: Average spend is lowest, hovering around 150–350.
Premium: Total spend peaks, with a distribution range from 1,800toouroutliercapof2,024.
Total Spend Distribution by Membership LevelFigure 3: Violin plot displaying the density and distribution of spending by membership tier.

4. Influencing Factors of Customer Churn
   
A. Churn vs. Average Rating (Satisfaction)
By evaluating the relationship between customer satisfaction (1-5 ratings) and churn, we found a distinct pattern:

Retained active customers have a median satisfaction rating of 4.0.
Customers who churned have a median satisfaction rating of 2.5, revealing a severe drop in happiness before departure.
Satisfaction Rating by Churn StatusFigure 4: Box plot comparing satisfaction ratings for active vs. churned customers.

5. Statistical Correlations
The Pearson correlation matrix provides a numeric view of the linear relationships within the dataset:

Spend & Items Purchased (r=0.90): Shows a nearly perfect positive correlation, showing that total spend is directly proportional to item quantity.
Rating & Churn (r=−0.56): Confirms a strong negative relationship (lower rating strongly indicates higher churn probability).
Discount Applied & Churn (r≈−0.05): Surprisingly, discounts do not have a strong linear correlation with customer retention in this cohort.
Correlation Matrix HeatmapFigure 5: Heatmap of Pearson correlation coefficients between numeric columns.

6. Recommendations & Action Items
Based on the visual and statistical trends, we propose three business recommendations:

Targeted Attrition Prevention: Setup an automated alert system when a customer's average rating falls below 3.0 to trigger proactive customer service.
Nurture High-Tier Members: Premium and Gold members generate the bulk of our revenue. Implement exclusive rewards or early-access product drops to retain these segments.
Upgrade Bronze Members: Since Bronze members have low purchase frequencies and spends, run promotional campaigns showcasing the benefits of moving up to the Silver tier.
