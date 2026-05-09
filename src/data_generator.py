import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)

NUM_USERS = 500
NUM_TRANSACTIONS = 10000

categories = [
    "Food Delivery", "Groceries", "Fashion", "Electronics",
    "Entertainment", "Travel", "Education", "Health",
    "Rent", "Utilities", "Investment", "EMI"
]

payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "BNPL"]

merchants = [
    "Amazon", "Flipkart", "Zomato", "Swiggy", "Myntra",
    "Netflix", "Uber", "BigBasket", "Croma", "Groww",
    "PhonePe", "Paytm"
]

devices = ["Mobile", "Desktop", "Tablet"]

users = []

for user_id in range(1, NUM_USERS + 1):
    age = np.random.randint(18, 45)
    income = np.random.choice(
        [15000, 25000, 35000, 50000, 75000, 100000],
        p=[0.15, 0.25, 0.25, 0.2, 0.1, 0.05]
    )
    risk_profile = np.random.choice(
        ["Conservative", "Balanced", "Aggressive"],
        p=[0.4, 0.4, 0.2]
    )

    users.append({
        "user_id": user_id,
        "age": age,
        "monthly_income": income,
        "risk_profile": risk_profile
    })

users_df = pd.DataFrame(users)

transactions = []

start_date = datetime(2025, 1, 1)

for txn_id in range(1, NUM_TRANSACTIONS + 1):
    user = users_df.sample(1).iloc[0]

    transaction_date = start_date + timedelta(days=np.random.randint(0, 365))
    transaction_hour = np.random.randint(0, 24)

    category = np.random.choice(categories)
    merchant = np.random.choice(merchants)
    payment_method = np.random.choice(payment_methods, p=[0.45, 0.25, 0.15, 0.05, 0.10])
    device = np.random.choice(devices, p=[0.75, 0.2, 0.05])

    base_amount = {
        "Food Delivery": 400,
        "Groceries": 1200,
        "Fashion": 2500,
        "Electronics": 12000,
        "Entertainment": 800,
        "Travel": 8000,
        "Education": 3000,
        "Health": 2000,
        "Rent": 12000,
        "Utilities": 1800,
        "Investment": 5000,
        "EMI": 6000
    }[category]

    amount = max(100, np.random.normal(base_amount, base_amount * 0.4))
    amount = round(amount, 2)

    day_of_month = transaction_date.day
    is_salary_day_near = 1 if day_of_month in [1, 2, 3, 4, 5] else 0
    is_late_night = 1 if transaction_hour >= 22 or transaction_hour <= 2 else 0

    ad_clicked = np.random.choice([0, 1], p=[0.7, 0.3])
    discount_used = np.random.choice([0, 1], p=[0.65, 0.35])
    cashback_used = np.random.choice([0, 1], p=[0.75, 0.25])

    mood_score = np.random.randint(1, 11)

    impulse_score = 0

    if category in ["Fashion", "Electronics", "Food Delivery", "Entertainment"]:
        impulse_score += 2

    if is_late_night:
        impulse_score += 2

    if ad_clicked:
        impulse_score += 2

    if discount_used:
        impulse_score += 1

    if cashback_used:
        impulse_score += 1

    if payment_method in ["Credit Card", "BNPL"]:
        impulse_score += 2

    if mood_score <= 4:
        impulse_score += 2

    if amount > user["monthly_income"] * 0.15:
        impulse_score += 2

    impulse_purchase = 1 if impulse_score >= 6 else 0

    financial_stress_level = min(
        10,
        int(
            (amount / user["monthly_income"]) * 20
            + (3 if payment_method == "BNPL" else 0)
            + (2 if impulse_purchase else 0)
        )
    )

    transactions.append({
        "transaction_id": txn_id,
        "user_id": user["user_id"],
        "age": user["age"],
        "monthly_income": user["monthly_income"],
        "risk_profile": user["risk_profile"],
        "transaction_date": transaction_date.date(),
        "transaction_hour": transaction_hour,
        "category": category,
        "merchant": merchant,
        "amount": amount,
        "payment_method": payment_method,
        "device": device,
        "is_salary_day_near": is_salary_day_near,
        "is_late_night": is_late_night,
        "ad_clicked": ad_clicked,
        "discount_used": discount_used,
        "cashback_used": cashback_used,
        "mood_score": mood_score,
        "financial_stress_level": financial_stress_level,
        "impulse_purchase": impulse_purchase
    })

transactions_df = pd.DataFrame(transactions)

users_df.to_csv("data/raw/users.csv", index=False)
transactions_df.to_csv("data/raw/transactions.csv", index=False)

print("Dataset generated successfully!")
print("Users:", users_df.shape)
print("Transactions:", transactions_df.shape)