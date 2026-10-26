#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 22:55:28 2026

@author: aaronkumar.p
"""


import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PERSONAL FINANCE & SPENDING ANALYZER
# ============================================================

# ------------------------------------------------------------
# 1. CREATE TRANSACTION DATA
# ------------------------------------------------------------

data = {
    "Date": [
        "2026-01-02", "2026-01-05", "2026-01-08", "2026-01-12",
        "2026-01-15", "2026-01-18", "2026-01-22", "2026-01-25",
        "2026-02-02", "2026-02-06", "2026-02-10", "2026-02-14",
        "2026-02-18", "2026-02-21", "2026-02-25", "2026-02-28",
        "2026-03-03", "2026-03-07", "2026-03-11", "2026-03-15",
        "2026-03-19", "2026-03-23", "2026-03-27", "2026-03-30"
    ],
    "Category": [
        "Food", "Transport", "Shopping", "Entertainment",
        "Food", "Bills", "Transport", "Shopping",
        "Food", "Bills", "Entertainment", "Transport",
        "Shopping", "Food", "Bills", "Entertainment",
        "Food", "Transport", "Shopping", "Bills",
        "Food", "Entertainment", "Transport", "Shopping"
    ],
    "Description": [
        "Restaurant", "Bus", "Clothes", "Movie",
        "Cafe", "Electricity", "Auto", "Shoes",
        "Restaurant", "Internet", "Gaming", "Cab",
        "Accessories", "Groceries", "Phone Bill", "Concert",
        "Cafe", "Metro", "Books", "Electricity",
        "Restaurant", "Movie", "Auto", "Clothes"
    ],
    "Amount": [
        450, 80, 1200, 350,
        300, 1800, 120, 1500,
        550, 900, 500, 200,
        1800, 700, 850, 1200,
        350, 100, 950, 1800,
        600, 400, 150, 2200
    ],
    "Type": [
        "Expense", "Expense", "Expense", "Expense",
        "Expense", "Expense", "Expense", "Expense",
        "Expense", "Expense", "Expense", "Expense",
        "Expense", "Expense", "Expense", "Expense",
        "Expense", "Expense", "Expense", "Expense",
        "Expense", "Expense", "Expense", "Expense"
    ]
}

data = pd.DataFrame(data)

print("\n===== ORIGINAL TRANSACTION DATA =====")
print(data)


# ------------------------------------------------------------
# 2. BASIC DATA INFORMATION
# ------------------------------------------------------------

print("\n===== DATASET INFORMATION =====")
print("Number of transactions:", len(data))
print("Number of columns:", len(data.columns))

print("\nColumn data types:")
print(data.dtypes)

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate rows:")
print(data.duplicated().sum())


# ------------------------------------------------------------
# 3. CONVERT DATE COLUMN
# ------------------------------------------------------------

data["Date"] = pd.to_datetime(data["Date"])

print("\nDate column converted successfully.")


# ------------------------------------------------------------
# 4. BASIC FINANCIAL SUMMARY
# ------------------------------------------------------------

total_spending = data["Amount"].sum()
average_transaction = data["Amount"].mean()
highest_transaction = data["Amount"].max()
lowest_transaction = data["Amount"].min()

print("\n===== FINANCIAL SUMMARY =====")
print(f"Total spending: ₹{total_spending:,.2f}")
print(f"Average transaction: ₹{average_transaction:,.2f}")
print(f"Highest transaction: ₹{highest_transaction:,.2f}")
print(f"Lowest transaction: ₹{lowest_transaction:,.2f}")


# ------------------------------------------------------------
# 5. CATEGORY-WISE SPENDING
# ------------------------------------------------------------

category_spending = data.groupby("Category")["Amount"].sum().sort_values(
    ascending=False
)

print("\n===== SPENDING BY CATEGORY =====")
print(category_spending)


# ------------------------------------------------------------
# 6. HIGHEST SPENDING CATEGORY
# ------------------------------------------------------------

highest_category = category_spending.idxmax()
highest_category_amount = category_spending.max()

print("\n===== HIGHEST SPENDING CATEGORY =====")
print(f"{highest_category}: ₹{highest_category_amount:,.2f}")


# ------------------------------------------------------------
# 7. MONTHLY SPENDING
# ------------------------------------------------------------

data["Month"] = data["Date"].dt.strftime("%B")

monthly_spending = data.groupby(
    data["Date"].dt.to_period("M")
)["Amount"].sum()

print("\n===== MONTHLY SPENDING =====")
print(monthly_spending)


# ------------------------------------------------------------
# 8. TOP 5 TRANSACTIONS
# ------------------------------------------------------------

top_transactions = data.sort_values(
    by="Amount",
    ascending=False
).head(5)

print("\n===== TOP 5 TRANSACTIONS =====")
print(top_transactions[["Date", "Category", "Description", "Amount"]])


# ------------------------------------------------------------
# 9. HIGH-SPENDING TRANSACTIONS
# ------------------------------------------------------------

high_spending = data[data["Amount"] >= 1500]

print("\n===== HIGH-SPENDING TRANSACTIONS =====")
print(high_spending[["Date", "Category", "Description", "Amount"]])


# ------------------------------------------------------------
# 10. DATA CLEANING DEMONSTRATION
# ------------------------------------------------------------

print("\n===== DATA CLEANING =====")

# Create a copy so the original dataset remains available
cleaned_data = data.copy()

# Introduce a missing value for demonstration
cleaned_data.loc[5, "Amount"] = None

# Introduce a duplicate row for demonstration
duplicate_row = cleaned_data.iloc[[2]]
cleaned_data = pd.concat(
    [cleaned_data, duplicate_row],
    ignore_index=True
)

print("Missing values before cleaning:")
print(cleaned_data.isnull().sum())

print("\nDuplicate rows before cleaning:")
print(cleaned_data.duplicated().sum())

# Fill missing amount using the median
median_amount = cleaned_data["Amount"].median()
cleaned_data["Amount"] = cleaned_data["Amount"].fillna(median_amount)

# Remove duplicates
cleaned_data = cleaned_data.drop_duplicates()

print("\nMissing values after cleaning:")
print(cleaned_data.isnull().sum())

print("\nDuplicate rows after cleaning:")
print(cleaned_data.duplicated().sum())


# ------------------------------------------------------------
# 11. RE-CALCULATE TOTAL AFTER CLEANING
# ------------------------------------------------------------

cleaned_total = cleaned_data["Amount"].sum()

print("\n===== CLEANED DATA SUMMARY =====")
print(f"Total spending after cleaning: ₹{cleaned_total:,.2f}")
print("Number of transactions after cleaning:", len(cleaned_data))


# ------------------------------------------------------------
# 12. SAVE CLEANED DATASET
# ------------------------------------------------------------

cleaned_data.to_csv(
    "transactions_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved as transactions_cleaned.csv")


# ------------------------------------------------------------
# 13. VISUALIZATION 1 — CATEGORY SPENDING
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

category_spending.plot(kind="bar")

plt.title("Spending by Category")
plt.xlabel("Category")
plt.ylabel("Amount Spent (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "spending_by_category.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# 14. VISUALIZATION 2 — MONTHLY SPENDING
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

monthly_spending.plot(
    kind="bar"
)

plt.title("Monthly Spending")
plt.xlabel("Month")
plt.ylabel("Amount Spent (₹)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "monthly_spending.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# 15. VISUALIZATION 3 — TRANSACTION AMOUNTS
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    range(1, len(data) + 1),
    data["Amount"],
    marker="o"
)

plt.title("Transaction Amounts")
plt.xlabel("Transaction Number")
plt.ylabel("Amount (₹)")
plt.tight_layout()

plt.savefig(
    "transaction_trend.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# 16. FINAL INSIGHTS
# ------------------------------------------------------------

print("\n========================================")
print("           FINAL INSIGHTS")
print("========================================")

print(f"Total spending: ₹{total_spending:,.2f}")
print(f"Average transaction: ₹{average_transaction:,.2f}")
print(f"Highest spending category: {highest_category}")
print(f"Highest category spending: ₹{highest_category_amount:,.2f}")
print(f"Highest single transaction: ₹{highest_transaction:,.2f}")

print("\nTop spending categories:")

for category, amount in category_spending.head(3).items():
    print(f"- {category}: ₹{amount:,.2f}")

print("\nAnalysis completed successfully!")
