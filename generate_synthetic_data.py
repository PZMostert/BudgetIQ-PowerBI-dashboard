"""
Generates SYNTHETIC BudgetIQ-style transaction data for the Power BI dashboard.
No real people, accounts or transactions are used. Output mirrors the BudgetIQ
`transactions` table: id, user_id, date, description, amount, category, created_at.
Seeded, so re-running gives the same files.
"""
import calendar, random, uuid
from datetime import date, datetime
import pandas as pd

rng = random.Random(2026)
USER_ID = str(uuid.UUID(int=rng.getrandbits(128), version=4))  # fake persona
rows = []

def uid():
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))

def rand_day(y, m, lo=1, hi=None):
    hi = min(hi or 99, calendar.monthrange(y, m)[1])
    return date(y, m, rng.randint(lo, hi))

def amt(lo, hi, mode=None):
    return round(rng.triangular(lo, hi, mode if mode is not None else lo + (hi - lo) * 0.3), 2)

def pos(merchant):
    """Mimic messy bank text: mixed English/Afrikaans prefixes, truncation, casing."""
    prefix = rng.choice(["POS Aankope ", "POS Purchase ", "POS Aankope ", ""])
    text = (prefix + merchant)[:30]
    return text.upper() if rng.random() < 0.25 else text

def add(d, desc, amount, cat):
    rows.append({"date": d, "description": desc, "amount": amount, "category": cat})

MERCH = {
    "Groceries": ["Checkers Hyper Menlyn", "Pick n Pay Brooklyn", "Woolworths Food Waterkloof", "Shoprite Centurion", "Spar Garsfontein"],
    "Food & Dining": ["Wimpy Menlyn", "Steers Centurion", "Nandos Brooklyn", "Spur Hazelwood", "Vida e Caffe", "Uber Eats", "Mr D Food", "KFC Lyttelton", "Debonairs Pizza", "Yoco *Coffee Shop", "Ocean Basket"],
    "Fuel": ["Engen Garsfontein", "Shell Ultra City", "Sasol Hatfield", "BP Centurion", "TotalEnergies N1"],
    "Parking": ["Admyt Parking", "Parkade Menlyn", "Hatfield Parking", "Campus Parking"],
    "Airtime & Data": ["Vodacom Airtime", "MTN Prepaid Data", "Telkom Mobile Data", "Cell C Airtime"],
    "Entertainment": ["Ster-Kinekor Menlyn", "Computicket", "Steam Purchase", "Dstv Showmax Rental"],
    "Clothing & Beauty": ["Mr Price Sport", "Cotton On", "Truworths", "Edgars", "Sportscene", "Woolworths Fashion", "Salon Menlyn"],
    "Health & Pharmacy": ["Dis-Chem Pharmacy", "Clicks Pharmacy", "Medirite Pharmacy"],
    "Shopping": ["Takealot", "Amazon", "Builders Express", "Game Stores", "Makro", "PEP Home"],
    "Travel": ["Uber Trip", "Bolt Ride", "Gautrain", "Intercape"],
    "Other": ["Yoco *Market Stall", "Snapscan *Vendor", "PayFast *Online", "Unknown Merchant"],
    "Education": ["UP Bookshop", "Udemy", "Coursera", "CNA Stationery"],
}
RANGES = {  # (low, high, mode) per transaction
    "Groceries": (45, 700, 180), "Food & Dining": (35, 380, 110), "Fuel": (300, 850, 480),
    "Parking": (8, 45, 20), "Airtime & Data": (29, 349, 99), "Entertainment": (60, 450, 150),
    "Clothing & Beauty": (120, 1100, 350), "Health & Pharmacy": (60, 650, 190),
    "Shopping": (80, 1500, 380), "Travel": (35, 320, 90), "Other": (20, 400, 90), "Education": (60, 650, 200),
}
COUNTS = {  # (min, max) per month
    "Groceries": (10, 14), "Food & Dining": (9, 14), "Fuel": (3, 5), "Parking": (3, 7),
    "Airtime & Data": (2, 4), "Entertainment": (1, 3), "Clothing & Beauty": (0, 2),
    "Health & Pharmacy": (1, 2), "Shopping": (1, 3), "Travel": (1, 3), "Other": (1, 3), "Education": (0, 1),
}
SEASON = {11: {"Shopping": 1.8}, 12: {"Food & Dining": 1.5, "Shopping": 2.0, "Entertainment": 1.8, "Clothing & Beauty": 1.8, "Travel": 1.6, "Groceries": 1.2},
          1: {"Education": 3}, 2: {"Education": 2}}

months = [(2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 10)]

for y, m in months:
    last = calendar.monthrange(y, m)[1]
    # Income
    sal_day = 18 if m == 12 else 25
    add(date(y, m, sal_day), rng.choice(["Salaris Kredietoorbetaling", "Salary Credit ACME PTY LTD"]), round(29850 + rng.uniform(-40, 60), 2), "Income")
    if m == 12:
        add(date(y, m, 18), "Bonus Credit ACME PTY LTD", 12350.00, "Income")
    if m in (11, 2, 4, 6, 8, 9):
        add(rand_day(y, m, 5, 22), "EFT Freelance Payment", amt(1800, 3500, 2200), "Income")
    # Fixed monthly items
    add(date(y, m, 1), "Debiet Order Huur Rental", -7800.00, "Rent")
    add(date(y, m, 3), "Debiet Order Discovery Insure", -1250.00, "Insurance")
    add(date(y, m, 5), "Debiet Order Virgin Active", -499.00, "Gym")
    add(date(y, m, 7), "Debiet Order Webafrica Fibre", -899.00, "Internet & Subscriptions")
    add(date(y, m, 9), "Netflix.com", -199.00, "Internet & Subscriptions")
    add(date(y, m, 11), "Spotify", -79.99, "Internet & Subscriptions")
    add(date(y, m, last), "Monthly Account Fee", -69.00, "Bank Fees")
    if rng.random() < 0.7:
        add(rand_day(y, m, 2, 27), "Cash Withdrawal Fee", -12.50, "Bank Fees")
    for _ in range(2):
        add(rand_day(y, m, 2, 28), "City of Tshwane Prepaid Elec", -round(rng.uniform(450, 750), 0), "Utilities")
    add(date(y, m, 26), "Savings Transfer", -1500.00, "Savings")
    add(rand_day(y, m, 1, 20), rng.choice(["EFT Mom", "Elektroniese Oorbetaling Ma"]), -float(rng.choice([500, 600, 800, 1000])), "Family")
    if m % 2 == 0:
        add(rand_day(y, m, 2, 27), "IB Transfer To Acc *4417", -float(rng.choice([800, 1000, 1500])), "Transfers")
    if m in (12, 1, 6):
        add(rand_day(y, m, 3, 20), "Transfer From Savings", 2000.00, "Transfer In")
    # Variable spend
    for cat, (lo_n, hi_n) in COUNTS.items():
        n = rng.randint(lo_n, hi_n)
        n = max(0, round(n * SEASON.get(m, {}).get(cat, 1) if cat not in ("Education",) else n))
        if cat == "Education":
            n = SEASON.get(m, {}).get("Education", 0) and rng.randint(1, 2) or (1 if rng.random() < 0.25 else 0)
        for _ in range(n):
            lo, hi, mode = RANGES[cat]
            mult = SEASON.get(m, {}).get(cat, 1) if cat != "Education" else 1
            add(rand_day(y, m), pos(rng.choice(MERCH[cat])), -amt(lo, hi * (1 + (mult - 1) * 0.4), mode), cat)

# Deliberate quirks for the cleaning and anomaly pages
add(date(2026, 3, 14), "POS Aankope Takealot Laptop", -14999.00, "Shopping")          # large one-off purchase
add(date(2026, 2, 19), "POS Purchase Unknown Merchant", -6200.00, "Other")             # suspicious / unexplained
add(date(2026, 5, 8), "Dishonoured Debit Order Fee", -350.00, "Bank Fees")             # unusual fee
add(date(2025, 12, 28), "Flysafair Return x2", -3450.00, "Travel")                     # holiday flights

df = pd.DataFrame(rows).sort_values(["date", "description"]).reset_index(drop=True)

# Miscategorised rows (real-world noise: auto-categoriser missed these)
spend_idx = df[df.category.isin(["Groceries", "Food & Dining"]) & (df.amount > -300)].index.tolist()
for i in rng.sample(spend_idx, 15):
    df.at[i, "category"] = "Other"

# Exact duplicate transactions (same day, text and amount, new id)
dup_src = df[df.category.isin(["Groceries", "Food & Dining", "Fuel", "Shopping"])].sample(6, random_state=7)
df = pd.concat([df, dup_src]).sort_values(["date", "description"]).reset_index(drop=True)

df.insert(0, "id", [uid() for _ in range(len(df))])
df.insert(1, "user_id", USER_ID)
# created_at = upload time (one batch per month, the day after month end)
def batch(d):
    nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return datetime(nxt.year, nxt.month, 1, 18, 20, 3, 515824).strftime("%Y-%m-%d %H:%M:%S.%f")
df["created_at"] = df["date"].apply(batch)
df["amount"] = df["amount"].round(2)
df = df[["id", "user_id", "date", "description", "amount", "category", "created_at"]]
df.to_csv("transactions_synthetic.csv", index=False)

budgets = pd.DataFrame([
    ("Rent", 7800), ("Groceries", 3000), ("Fuel", 2000), ("Food & Dining", 1700), ("Utilities", 1300),
    ("Internet & Subscriptions", 1200), ("Insurance", 1250), ("Gym", 500), ("Airtime & Data", 400),
    ("Entertainment", 500), ("Clothing & Beauty", 700), ("Health & Pharmacy", 450), ("Shopping", 1000),
    ("Parking", 150), ("Travel", 500), ("Education", 300), ("Family", 800), ("Bank Fees", 100),
    ("Savings", 1500), ("Other", 300)], columns=["category", "monthly_budget"])
budgets.to_csv("budgets_synthetic.csv", index=False)
print(len(df), "transactions;", df.date.min(), "to", df.date.max())
