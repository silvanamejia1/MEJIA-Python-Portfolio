import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("💰 EasyInvest Planner")
st.subheader("Personalized financial planning made easy")
st.markdown("""
Welcome to **EasyInvest Planner**. Your personalized tool to help you better plan your income allocation and investment strategy. 🎯

This app takes into account your age, income, financial dependents, and risk preferences to give you two key recommendations:
- **How to allocate your income** → Essentials, Savings, Investing, and Fun/Other.
- **How to invest your investment portion** → Variable Income, Fixed Income, and Alternatives.

### 📌 How do filters affect my plan?
- **Age** → Younger users are recommended to take more investment risk (more variable income). Older users shift toward safer options (more Fixed Income).
- **Income** → Higher income allows for higher saving and investing percentages.
- **Dependents** → More dependents means safer allocations (less variable Income, more Fixed Income) and slightly higher essential expenses. This supposes taht a higher % of your income would go towards essential for otehr members in your family.
- **Risk Tolerance** → If you prefer higher risk, your portfolio will lean more toward Variable. If lower, toward Fixed Income. Answer this based on personal preference.
- **Savings Goal** → While not changing calculations directly, it helps frame your investment mindset.

Use the filters on the left to personalize your plan and click the buttons to see a clear visual breakdown of where your money should go and how you should invest.
""")
#SECTION 1: USER INPUTS
# User Inputs Revelant to investment
age = st.slider("Your Age", 18, 80, 30)
income = st.number_input("Your Annual Income ($)", min_value=0, value=60000, step=1000)
dependents = st.slider("Number of Financial Dependents", 0, 5, 0)

# Calculate risk score based on user profile (This will give user some backround on their current risk profile given inputs but flexibility to change if they have more agressive investment goals)
risk_score = 0

# Age Factor
if age < 30:
    risk_score += 2  # Younger → Higher risk 
elif age < 50:
    risk_score += 1  # Middle-aged → Moderate
else:
    risk_score -= 1  # Older → Lower risk 

# Income Factor
if income >= 150000:
    risk_score += 2
elif income >= 70000:
    risk_score += 1
else:
    risk_score -= 1

# Dependents Factor
if dependents >= 3:
    risk_score -= 2
elif dependents >= 1:
    risk_score -= 1

# Final suggested risk category
if risk_score >= 3:
    suggested_risk = "High"
    risk_explanation = "Given your younger age and/or higher income and fewer dependents, you may have the flexibility to take on more risk for higher potential returns."
elif risk_score >= 0:
    suggested_risk = "Medium"
    risk_explanation = "Your profile suggests a balanced approach, aiming for growth while maintaining some stability."
else:
    suggested_risk = "Low"
    risk_explanation = "Your profile suggests a lower risk tolerance to help preserve your capital and minimize potential losses, which is especially important with age or more dependents."

# Display explanation on how to choose risk level
st.markdown(f"""
**Not sure about your risk tolerance?**

Based on your profile (Age: {age}, Income: ${income:,}, Dependents: {dependents}), you may fall into a **{suggested_risk} Risk Tolerance** category.  
{risk_explanation}

Remember, this is only a suggestion based on your profile. You can freely adjust this to match your personal comfort and investment goals.
""")
risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
goal = st.selectbox("Savings Goal", ["Retirement", "Education", "Buying a Home", "Other"])

#SECTION 2: BUDGET PLAN
# Investemnt Calculations
# Default asset allocation
variable_income = 60
fixed_income = 30
alternatives = 10

# Adjustments based on inputs
#Age adjustment
#Asummes younger individuals have higher risk tolerance and therefore can afford higher risk invetsments that dont necesarily pay as fast (Equity Assets)
if age < 30: #If they are below 30, we assume a higher risk tolerance compared to default and reccomend more equity
    variable_income += 10
elif age > 50:
    fixed_income += 10 #If they are above, we assume a lower risk tolerance compared to default and reccomend more fixed income

if dependents >= 2: #More dependents, means less risk tolerance and a need for a safer investemnt plan meaning switch from equity to fixed income
    fixed_income += 10
    variable_income -= 10

#Despite oen ssituation, some might still have a persona; prefernece towards riskier, higehr return portafolios
if risk_tolerance == "High":
    variable_income += 10
    fixed_income -= 10
elif risk_tolerance == "Low":
    fixed_income += 10
    variable_income -= 10

alternatives = 100 - (variable_income + fixed_income)


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

#Knowing what % of income will be spent in investing and saving, we know that  we still have essentials and "buffer money" to account for
essentials_pct = 50 + (dependents * 5) #we are suppoing that 50% of income according to OPERS, however, we account for an additional % in the case where they have dependants

# Ensure total % doesn't exceed 100
total_allocated = essentials_pct + invest_pct + save_pct
if total_allocated > 100:
    essentials_pct = 100 - (invest_pct + save_pct)

# Extra % is whatever is left over 
extra_pct = 100 - (essentials_pct + invest_pct + save_pct)

#Bar Graph showing Income Breakdown based on extra_pct, essentials_pct, invest_pct, save_pct)
st.header("📊 Where Your Money Goes?")

# Breakdown period (year/moth) Selection
breakdown_period = st.radio("Select breakdown period:", ["Monthly", "Yearly"], horizontal=True)

# Calculate actual dollar amounts according to breakdown period selected
monthly_income = income / 12
yearly_income = income

if breakdown_period == "Monthly":
    essentials_amt = monthly_income * (essentials_pct / 100)
    save_amt = monthly_income * (save_pct / 100)
    invest_amt = monthly_income * (invest_pct / 100)
    fun_amt = monthly_income * (extra_pct / 100)
else:
    essentials_amt = yearly_income * (essentials_pct / 100)
    save_amt = yearly_income * (save_pct / 100)
    invest_amt = yearly_income * (invest_pct / 100)
    fun_amt = yearly_income * (extra_pct / 100)

# Show message with dollar values
st.markdown(f"""
Based on your income, here's how much you should ideally spend in a **{breakdown_period.lower()}**:
- 🏠 Essentials: **${essentials_amt:,.2f}**
- 💾 Saving: **${save_amt:,.2f}**
- 📈 Investing: **${invest_amt:,.2f}**
- 🎉 Fun & Other: **${fun_amt:,.2f}**
""")

#Compare to actual spending values
st.markdown("Before seeing the suggested plan, tell us how you're currently breaking down your income. This will help you visualize how your current spending compares to your ideal spending:")
st.markdown(f"**Enter your spending amounts below based on your selected breakdown period ({breakdown_period}).**")
st.markdown("Please round your entries to the nearest $100 to make calculations easier.")

# User input for actual spending (default is set to 0)
actual_essentials = st.number_input(f"How much do you spend on Essentials {breakdown_period}?", min_value=0.0, value=0.0, step=100.0)
actual_saving = st.number_input(f"How much do you save {breakdown_period}?" , min_value=0.0, value=0.0, step=100.0)
actual_investing = st.number_input(f"How much do you invest {breakdown_period}?", min_value=0.0, value=0.0, step=100.0)
actual_fun = st.number_input(f"How much do you spend on Fun & Other {breakdown_period}?", min_value=0.0, value=0.0, step=100.0)

# Exapnder Button to show bar chart of income breakdown (will be side by side chart comapring their actual breakdown vs ideal breakdown)
with st.expander(f"Show {breakdown_period} Breakdown"):

    # Categories
    categories = ["Essentials", "Saving", "Investing", "Fun & Other"]

    # Ideal amounts (recommended breakdown)
    ideal_amounts = [essentials_amt, save_amt, invest_amt, fun_amt]

    # Actual amounts (user input)
    actual_amounts = [actual_essentials, actual_saving, actual_investing, actual_fun]

    # Bar positions
    x = range(len(categories))
    width = 0.35 

    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot ideal amounts
    bars_ideal = ax.bar([p - width/2 for p in x], ideal_amounts, width=width, label='Suggested', color='#FFB347')

    # Plot actual amounts
    bars_actual = ax.bar([p + width/2 for p in x], actual_amounts, width=width, label='Actual', color='#5DADE2')

    # Add labels on top of bars
    for bar in bars_ideal + bars_actual:
        height = bar.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_ylabel("Amount in USD ($)")
    ax.set_title(f"{breakdown_period} Allocation: Suggested vs. Actual Spending")
    ax.set_xticks(list(x))
    ax.set_xticklabels(categories)
    ax.legend()

    fig.tight_layout(pad=4)
    st.pyplot(fig)

## STEP 3: INVESTMENT BREAKDOWN
#Pie chart of investing breakdown
st.markdown("## 🧩 Structuring Your Investments")
st.markdown("Once you know your spending breakdown, it's time to see how you should structure your investments:")
with st.expander("Show How I Should Be Investing"):#st.exapnder over button so that other information stays after click

    # Investment Allocation Suggestion
    st.header("📈 How You Should Be Investing")

    # Labels and values
    investment_labels = ['Variable Income', 'Fixed Income', 'Alternatives']
    investment_values = [variable_income, fixed_income, alternatives]
    investment_colors = ['#AED9E0', '#5DADE2', '#154360']

    # Create pie chart
    fig_invest, ax_invest = plt.subplots()
    ax_invest.pie(
        investment_values, #data that will be ploted 
        labels=investment_labels, #labels that goes with each %
        autopct='%1.1f%%', #One decimal place to improve readability
        colors=investment_colors, #define the same colors as before
        wedgeprops={'edgecolor': 'white'} #define the edges of each pie to be able to separate slices
    )
    ax_invest.axis('equal')  # Make the pie circular
    st.pyplot(fig_invest) #tie into streamlit app

## STEP 4: ASSET CLASS EXPLANATION
#Asset class expalnation
st.markdown("### ❓ What do these investment types mean?") 
st.markdown("Understanding how Variable Income, Fixed Income, and Alternatives contribute to your portafolio is key to making informed decisions. Explore the sections below to learn more about each type of investment.")

# Explanation of Variable Income
with st.expander("What is Variable Income?"):
     st.markdown("""
Variable income investments are assets where returns can fluctuate depending on market performance. They tend to offer **higher growth potential but also more volatility.**

**How it impacts your portfolio:**  
Increases your potential for long-term growth, but adds more risk. Suitable when you're younger or willing to take more risk.

**Examples:**  
- Stocks  
- S&P 500 Index Funds  
- Mutual Funds
""")

# Explanation of Fixed Income
with st.expander("What is Fixed Income?"):
        st.markdown("""
Fixed income investments provide stable and predictable returns, making them **lower-risk options.** These investments help preserve your capital and offer steady income.

**How it impacts your portfolio:**  
Reduces risk and volatility, while ensuring you have consistent returns. Especially important as you get closer to retirement or have lower risk tolerance.

**Examples:**  
- Treasury Bonds  
- Certificates of Deposit (CDs)  
- Municipal Bonds
        """)

# Explanation of Alternatives
with st.expander("What are Alternatives?"):
    st.markdown("""
Alternatives include investments that are outside of traditional stocks and bonds. Despite being **risky**, they **help diversify your portfolio** and often behave differently in various market conditions.

**How it impacts your portfolio:**  
Helps reduce overall risk through diversification and can offer unique growth opportunities not tied to the stock or bond market.

**Examples:**  
- Real Estate 
- Commodities  
- Private Equity
        """)

#Takeaway
st.markdown("### 👤 Your Personalized Investment Plan")
st.markdown("Now that you have an investment strategy, let's put it all together into your personalized plan:")
with st.expander("See Your Personalized Investment Plan"):
    st.header("📌 Your Personalized Investment Plan")

    st.markdown(f"""
    ### 📈 Variable Income ({variable_income}%)

    Higher risk, focused on long-term growth.  
    **Recommendation:** Start with [S&P 500 index funds](https://www.investopedia.com/terms/s/sp500.asp), which offer diversification and are considered a safer bet for beginners.

    ---

    ### 🏦 Fixed Income ({fixed_income}%)

    Lower risk, providing steady returns.  
    **Recommendation:** Consider Treasury Bonds. They are among the safest investments.

    ---

    ### 🌎 Alternatives ({alternatives}%)

    Diversify your portfolio with assets that don't move like stocks or bonds.  
    **Recommendation:** Look into **data center real estate**, which is in high demand due to the AI boom.
    """)

