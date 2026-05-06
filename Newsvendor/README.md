# Newsvendor

1. **Data**: 👖 This dataset consists of H&M fashion retailer sales data (Ling et al., 2022), preprocessed to retain 300 trouser items with their weekly demand over 30 weeks under stable prices. (__[source](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data?select=articles.csv)__)
   
   For each item, we use the empirical distribution of its 30 weekly demand observations as the ground truth $F$. Each item is associated with metadata such as product name, type, and color.

   The relatent code of data preprocessing is in file: `Newsvendor_data_pre.ipynb`

3. **Generate**:
💡 Unlike the assortment and pricing tasks, the newsvendor setting is structurally different: a single observation is a weekly demand realization for an item rather than a choice or valuation by an individual. The "human simulation" paradigm is therefore less applicable, and we omit the agent-based sampling methods.

   The relatent code of data preprocessing is in file: `Newsvendor_data_generation.ipynb`

3. **Evaluation**:
💡 The relatent code of data preprocessing is in file: `Newsvendor_data_result.ipynb`


  

