# Evaluating-LLM-persona-Generated-Distributions-for-Decision-making

## Environment Setup

Set the following environment variables before running any experiments:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"   # gpt-4o, gpt-5-mini
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"   # gemini-3-flash-preview
export MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY" # mistral-large-latest

---

## Usage

---

### Step 1. Clone the repository

```bash
git clone <repository_url>
cd <repository_name>

---

### Step 2. Enter a dataset directory

Each decision problem is organized in a separate folder. Choose one dataset to work with.

```bash
cd Assortment
```

```bash
cd Pricing
```

---

### Step 3. Configure the dataset

Run the configuration script inside the dataset directory to prepare data files and directory structure.

```bash
bash run.sh
```

---

### Step 4. Choose the task type

After configuration, choose whether to perform data generation or data quality evaluation.

```bash
cd data_generation
```

```bash
cd data_quality
```

---

### Step 5. Run the main script

Each task folder contains a main Python script with the same name as the folder.

```bash
python data_generation.py
```

```bash
python data_quality.py
```

---

### Step 6. Follow interactive prompts

Follow the on-screen prompts to select the model, method, steering strategy, and other task-specific options.

All outputs will be saved automatically to the corresponding `results/` directory.

