# Evaluating-LLM-persona-Generated-Distributions-for-Decision-making

## Environment Setup

Set the following environment variables before running any experiments:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"   # gpt-4o, gpt-5-mini
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"   # gemini-3-flash-preview
export MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY" # mistral-large-latest
```

---

## Usage

---

### Step 1. Clone the repository

```bash
git clone <repository_url>
cd <repository_name>
```

---

### Step 2. 

Choose one decision problem and navigate to the corresponding directory.
We provide three decision problems in this repository:
- **Assortment**
- **Pricing**
- **Newsvendor**

Then, follow the instructions provided in the README file of the selected problem.

For example, to work on the Newsvendor problem:
```bash
cd Newsvendor
```

