# Pricing Optimization

1. **Data**: 🍫 Experimental and survey data capturing the impact of sensory cues, award and origin labels on willingness-to-pay for Philippine tablea (cocoa liquor). ([source](https://www.kamishima.net/sushi/))
   
   We use willingness-to-pay data for cocoa liquor products in the Philippines.

   The dataset includes 3 chocolate types (Bohol, Davao, and Improved Bicol), each presented under 2 information conditions (award and origin), resulting in 6 products in total. 
The dataset contains willingness-to-pay responses from 204 participants for these 6 products.

   We use the first 100 participants as ground truth.

   **Please** download and preprocess the baseline or helper data before proceeding to data generation or data quality evaluation by running:
   ```bash
   bash run.sh
   ```
  
2. **Generate**:

   💡 We provide 8 generation methods: Sampling, Few-shot Sampling, Persona Sampling, Persona Few-shot Sampling, Batch, Few-shot Batch, Description and Few-shot Description, combined with 4 models.

   `data_generation.py` is used to generate data and is the only script that needs to be executed.
   Following task-specific instructions, users may choose any supported model and generation strategy.

   All generated outputs are saved to the `./results/` directory.

   📌 **Usage**:
    1. Configure the environment variables as described in the main README.
    2. Run `data_generation.py`:
       ```bash
       python3 data_generation.py
    3. Follow task-specific instructions

     ⚠️ **Note**:
     - Different models require corresponding API keys to be configured **before** running the script (e.g., `OPENAI_API_KEY`).
     - Avoid mixing multiple models within the same run, as outputs in the `results/` directory may be overwritten.
    

4. **Evaluation**:

   💡 We provide 5 metrics: MAE, KS Distance, Wasserstein Distance, AverageCR (with 3 cost ranges: 0-32; 0-66; 0-100), and WorstCR (with max cost of 32 and 66).
   All methods are applied to 20 distributions, and we report the mean and 95% confidence interval.

   `data_quality.py` is used to evaluate data quality and is the only script that needs to be executed.
   Following task-specific instructions, users may choose the evaluation method.

   All mean values and confidence intervals are printed to the terminal.

   📌 **Usage**:
   1. Prepare all data and store them in `src/`.  
      (We upload the generated data by default; users may also provide their own.)
   2. Run `data_quality.py`:
      ```bash
      python3 data_quality.py
      ```
   3. Follow the task-specific instructions in the script.



