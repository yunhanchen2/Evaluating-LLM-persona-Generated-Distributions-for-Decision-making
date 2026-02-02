import json
import numpy as np

__all__ = ["read_lines", "load_products", "line_to_expanded_structure"]

def read_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [ln.strip() for ln in f if ln.strip() != '']

def load_products(filename, n_products=3):
    products = [[] for _ in range(n_products)]

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            tokens = line.split()
            if len(tokens) < n_products:
                continue
                
            try:
                values = list(map(float, tokens[:n_products]))
            except ValueError:
                continue

            for i in range(n_products):
                products[i].append(values[i])

    return products

def line_to_expanded_structure(line, n=50):
    dist = json.loads(line)
    supp = dist["premium_support"]
    probs = dist["probabilities"]

    def expand(values, ps):
        ps = np.array(ps, dtype=float)
        raw = ps * n
        cnt = np.floor(raw).astype(int)
        rem = n - cnt.sum()

        # allocate remaining slots to largest fractional parts
        frac = raw - np.floor(raw)
        order = np.argsort(-frac)
        for k in range(rem):
            cnt[order[k]] += 1

        out = []
        for v, c in zip(values, cnt):
            out += [v] * int(c)
        return out  # length n

    expanded = {
        "Bohol": expand(supp["Bohol"], probs["Bohol"]),
        "Davao": expand(supp["Davao"], probs["Davao"]),
        "ImprovedBicol": expand(supp["ImprovedBicol"], probs["ImprovedBicol"]),
    }
    return expanded

