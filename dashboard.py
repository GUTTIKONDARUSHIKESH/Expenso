import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Daily Expense Live Tracker")

df = pd.read_csv("Data/expenses.csv")

st.sidebar.header("Filter Data")

category_filter = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["Category"].unique())
)

if category_filter != "All":
    df = df[df["Category"] == category_filter]

st.sidebar.header("Add New Expense")

date = st.sidebar.date_input("Date")
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount")
payment = st.sidebar.text_input("Payment Mode")
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    new_expense = pd.DataFrame([[date, category, amount, payment, description]], columns=df.columns)
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv("Data/expenses.csv", index=False)

st.subheader("Expense Data")
st.write(df)

st.download_button(
    label="Download Expense Report",
    data=df.to_csv(index=False),
    file_name="expense_report.csv",
    mime="text/csv"
)

total_expense = df["Amount"].sum()

st.metric("Total Expenses", f"₹{total_expense}")

st.subheader("Expense Analysis")

category_total = df.groupby("Category")["Amount"].sum()

# Bar Chart
st.subheader("Category-wise Expense (Bar Chart)")
fig1, ax1 = plt.subplots()
category_total.plot(kind="bar", ax=ax1)
st.pyplot(fig1)

# Pie Chart
st.subheader("Expense Distribution (Pie Chart)")
fig2, ax2 = plt.subplots()
category_total.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
st.pyplot(fig2)

st.subheader("Daily Spending Trend")

daily_total = df.groupby("Date")["Amount"].sum()

fig3, ax3 = plt.subplots()
daily_total.plot(kind="line", marker="o", ax=ax3)

st.pyplot(fig3)
