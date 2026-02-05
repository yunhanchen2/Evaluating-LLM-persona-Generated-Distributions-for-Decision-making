# 📊 Evaluating-LLM-persona-Generated-Distributions-for-Decision-making

## 🔧 Environment Setup

We provide 4 supported models in this repository.
Please configure the corresponding API keys before running any experiments.

- 🔑 `OPENAI_API_KEY`: gpt-4o, gpt-5-mini  
- 🔑 `GOOGLE_API_KEY`: gemini-3-flash-preview  
- 🔑 `MISTRAL_API_KEY`: mistral-large-latest  

Set the following environment variables:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
export MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY"
```

---

## 🚀 Usage

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
- **🍣 Assortment**
- **🍫 Pricing**
- **👖 Newsvendor**

Then, follow the instructions provided in the README file of the selected problem.

For example, to work on the Newsvendor problem:
```bash
cd Newsvendor
```

