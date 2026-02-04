import random
def load_user_features(path):
    with open(path, 'r') as f:
        return [line.strip().split() for line in f]

def age_to_band(a):
    if a is None: return "unknown"
    a = int(round(a))
    if a <= 24: return "18-24"
    if a <= 34: return "25-34"
    if a <= 44: return "35-44"
    return "45+"

def sex_to_gender(s):
    if s is None: return "unknown"
    return "female" if int(round(s)) == 1 else "male"

def income_to_band(v):
    if v is None: return "unknown"
    return "middle_to_high" if int(round(v)) == 1 else "low"

def mainshop_to_text(v):
    if v is None: return "unknown"
    return "yes" if int(round(v)) == 1 else "no"

def tablea_freq_bin3(v):
    if v is None: 
        return "unknown"
    v = int(round(v))
    if v <= 3:
        return "low"
    if v <= 6:
        return "middle"
    return "high"

def choco_pref_from_darkch(v):
    if v is None: return "unknown"
    v = int(round(v))
    if v <= 3: return "low"
    if v <= 6: return "middle"
    return "high"

def award_fam_trust(gtseen, gttrust, acseen, actrust):
    seen_any = (gtseen == 1) or (acseen == 1)

    trust_max = None
    if gttrust is not None and 1 <= gttrust <= 5:
        trust_max = gttrust
    if actrust is not None and 1 <= actrust <= 5:
        trust_max = actrust if (trust_max is None or actrust > trust_max) else trust_max

    if (not seen_any) and (trust_max is None or trust_max <= 2):
        return "low award influence"
    if seen_any and (trust_max is not None) and (trust_max >= 4):
        return "high award influence"
    return "moderate award influence"

def importance_origin_text(v):
    if v is None:
        return "unknown"
    v = int(round(v))
    v = 1 if v < 1 else (5 if v > 5 else v)

    labels = {
        1: "not important",
        2: "slightly important",
        3: "moderately important",
        4: "important",
        5: "very important",
    }

    return labels[v]

def user_to_text(fields):
    if len(fields) != 11:
        raise ValueError("Expect 11 fields: AGE, SEX, HHINCO, MAINSH, TABLEACH, IORIGIN, DARKCH, GTSEEN, GTTRUST, ACSEEN, ACTRUST")

    AGE      = float(fields[0])
    SEX      = int(fields[1])
    HHINCO   = int(fields[2])
    MAINSH   = int(fields[3])
    TABLEACH = int(fields[4])
    IORIGIN  = int(fields[5])
    DARKCH   = int(fields[6])
    GTSEEN   = int(fields[7])
    GTTRUST  = int(fields[8])
    ACSEEN   = int(fields[9])
    ACTRUST  = int(fields[10])

    age_band   = age_to_band(AGE)
    gender     = sex_to_gender(SEX)
    income     = income_to_band(HHINCO)
    main_shop  = mainshop_to_text(MAINSH)
    tablea_fq  = tablea_freq_bin3(TABLEACH)          
    imp_origin = importance_origin_text(IORIGIN)     
    choco_pref = choco_pref_from_darkch(DARKCH)      
    award_cat  = award_fam_trust(GTSEEN, GTTRUST, ACSEEN, ACTRUST)

    return f"A {age_band} {gender} with {income} income and {main_shop} main shopping experience, who consumes tablea at a {tablea_fq} frequency, considers origin {imp_origin}, has a {choco_pref} preference for chocolate, and is {award_cat}."


def sample_fewshot_lines(k, INFO):
    if INFO == 1:
        path = "src/examples_awards.txt"
    elif INFO == 2:
        path = "src/examples_origin.txt"
    else:
        raise ValueError("INFO must be 1 (awards) or 2 (origin)")

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    if len(lines) < k:
        raise ValueError(f"File {path} has only {len(lines)} lines, need {k}")

    return "\n".join(random.sample(lines, k))



__all__ = [
    "user_to_text",
    "sample_fewshot_lines",
    "load_user_features",
]
