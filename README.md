# Evaluating-LLM-persona-Generated-Distributions-for-Decision-making

## Environment Setup

Set the following environment variables before running any experiments:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"   # gpt-4o, gpt-5-mini
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"   # gemini-3-flash-preview
export MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY" # mistral-large-latest

# Usage

```bash
# 1. Clone the repository
git clone <repository_url>
cd <repository_name>

# 2. Enter a dataset directory (choose one)
cd Assortment
# or
cd Pricing

# 3. Configure the dataset
bash run.sh

# 4. Choose task type after configuration
# (data generation or data quality evaluation)
cd data_generation
# or
cd data_quality

# 5. Run the main script (same name as the folder)
python data_generation.py
# or
python data_quality.py

# 6. Follow interactive prompts to select the desired task
# (model, method, steering strategy, etc.)
# All outputs will be saved to the corresponding results/ directory
