# Newsvendor

1. **Data**: 👖 This dataset consists of H&M fashion retailer sales data (Ling et al., 2022), preprocessed to retain 300 trouser items with their weekly demand over 30 weeks under stable prices. (__[source]([https://data.mendeley.com/datasets/7c5vfsgcnz/1](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data?select=articles.csv)__)
   
   For each item, we use the empirical distribution of its 30 weekly demand observations as the ground truth $F$. Each item is associated with metadata such as product name, type, and color.

2. **Generate**:
💡 Unlike the assortment and pricing tasks, the newsvendor setting is structurally different: a single observation is a weekly demand realization for an item rather than a choice or valuation by an individual. The "human simulation" paradigm is therefore less applicable, and we omit the agent-based sampling methods.

   We provide 1 generation method: **Descriptive with Few-shot examples**, combined with 4 models. For each target item, the LLM is prompted with the item's metadata and a reference set of 100 other items (including their metadata and historical demand parameters), and asked to predict the **mean** and **standard deviation** of a normal distribution corresponding to the item's weekly demand.

   We also include a **Random baseline** which uses the empirical distribution of demands aggregated over all 300 items.

   2. Follow task-specific instructions

⚠️ Note:
   * Different models require corresponding API keys to be configured before running the script (e.g., `OPENAI_API_KEY`).
   * Avoid mixing multiple models within the same run, as outputs in the `results/` directory may be overwritten.

3. **Evaluation**:
💡 We provide . All methods are applied to 20 distributions, and we report the mean and 95% confidence interval.

`data_quality.py` is used to evaluate data quality and is the only script that needs to be executed. Following task-specific instructions, users may choose the evaluation method.

All mean values and confidence intervals are printed to the terminal.
📌 Usage:
   1. Prepare all data and store them in `src/`. (We upload the generated data by default; users may also provide their own.)
   2. Run `data_quality.py`:

```
python3 data_quality.py
```

   3. Follow the task-specific instructions in the script.



