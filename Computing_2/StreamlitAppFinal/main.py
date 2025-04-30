import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title
st.title("💰 Smart Invest Plan")
st.subheader("Personalized financial planning made easy")

# User Inputs Revelant to investment
age = st.slider("Your Age", 18, 80, 30)
income = st.number_input("Your Annual Income ($)", min_value=0, value=60000, step=1000)
dependents = st.slider("Number of Financial Dependents", 0, 5, 0)
risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
goal = st.selectbox("Savings Goal", ["Retirement", "Education", "Buying a Home", "Other"])

# Investemnt Calculations
# Default asset allocation
stocks = 60
bonds = 30
cash = 10

# Adjustments based on inputs
#Age adjustment
#Asummes younger individuals have higher risk tolerance and therefore can afford higher risk invetsments that dont necesarily pay as fast (Equity Assets)
if age < 30: #If they are below 30, we assume a higher risk tolerance compared to default and reccomend more equity
    stocks += 10
elif age > 50:
    bonds += 10 #If they are above, we assume a lower risk tolerance compared to default and reccomend more fixed income

if dependents >= 2: #More dependents, means less risk tolerance and a need for a safer investemnt plan meaning switch from equity to fixed income
    bonds += 10
    stocks -= 10

#Despite oen ssituation, some might still have a persona; prefernece towards riskier, higehr return portafolios
if risk_tolerance == "High":
    stocks += 10
    bonds -= 10
elif risk_tolerance == "Low":
    bonds += 10
    stocks -= 10

cash = 100 - (stocks + bonds)


#Budget Plan
#Save and Invest $ are proportional to income.
if income < 40000: #Lower income - lower invest - lower save
    invest_pct = 10
    save_pct = 10
elif income < 100000: #medium income - higher invest - higher save
    invest_pct = 15
    save_pct = 15
else:
    invest_pct = 20
    save_pct = 20

#knowing what % of income will be spent in investing and saving, we know that 
essentials_pct = 50 #we are suppoing that 50% of income according to OPERS
extra_pct = 100 - (essentials_pct + invest_pct + save_pct)

#Bar Graph showing Income Breakdown based on extra_pct, essentials_pct, invest_pct, save_pct)
st.header("📊 Where Your Money Goes Each Month")

# Convert yearly percentages to monthly dollar values
monthly_income = income / 12
essentials_amt = monthly_income * (essentials_pct / 100)
save_amt = monthly_income * (save_pct / 100)
invest_amt = monthly_income * (invest_pct / 100)
fun_amt = monthly_income * (extra_pct / 100)

# Prepare data
categories = ["Essentials", "Saving", "Investing", "Fun & Other"]
amounts = [essentials_amt, save_amt, invest_amt, fun_amt]

# Plot
fig, ax = plt.subplots()
ax.bar(categories, amounts)
ax.set_ylabel("Amount in USD ($)")
ax.set_title("Monthly Allocation of Your Income")
st.pyplot(fig)
