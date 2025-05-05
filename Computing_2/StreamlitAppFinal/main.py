import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title
st.title("💰 Smart Invest Plan")
st.subheader("Personalized financial planning made easy")
st.markdown("""
Welcome to **Smart Invest Plan** — your personalized tool to help you better plan your income allocation and investment strategy. 🎯

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

# User Inputs Revelant to investment
age = st.slider("Your Age", 18, 80, 30)
income = st.number_input("Your Annual Income ($)", min_value=0, value=60000, step=1000)
dependents = st.slider("Number of Financial Dependents", 0, 5, 0)
risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
goal = st.selectbox("Savings Goal", ["Retirement", "Education", "Buying a Home", "Other"])

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

# 1. Breakdown period (year/moth)
breakdown_period = st.radio("Select breakdown period:", ["Monthly", "Yearly"], horizontal=True)

# 2. Calculate actual dollar amounts
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

# 3. Show message with dollar values
st.markdown(f"""
Based on your income, here's how much you should ideally spend in a **{breakdown_period.lower()}**:
- 🏠 Essentials: **${essentials_amt:,.2f}**
- 💾 Saving: **${save_amt:,.2f}**
- 📈 Investing: **${invest_amt:,.2f}**
- 🎉 Fun & Other: **${fun_amt:,.2f}**
""")

# 4. Button to show bar chart of income breakdown
if st.button(f"Show {breakdown_period} Breakdown"):
    categories = ["Essentials", "Saving", "Investing", "Fun & Other"]
    amounts = [essentials_amt, save_amt, invest_amt, fun_amt]
    colors = ['#FFD580', '#FFAA5C', '#FF7F7F', '#FF4C4C']  # Sunset ombré shades

    fig, ax = plt.subplots(figsize=(10, 9))
    bars = ax.bar(categories, amounts, color=colors)

    # Add dollar labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 9),
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_ylabel("Amount in USD ($)")
    ax.set_title(f"{breakdown_period} Allocation of Your Income")
    fig.tight_layout(pad=4)
    st.pyplot(fig)

#Pie chart of investing breakdown
if st.button("Show How I Should Be Investing"):

    # Investment Allocation Section
    st.header("📈 How You Should Be Investing")

    # Labels and values
    investment_labels = ['Variable Income', 'Fixed Income', 'Alternatives']
    investment_values = [variable_income, fixed_income, alternatives]

    # I choose colors that are different from the first bar graph to avoid confusion
    investment_colors = ['#AED9E0', '#5DADE2', '#154360']

    # Create pie chart
    fig_invest, ax_invest = plt.subplots()
    ax_invest.pie(
        investment_values, #data that will be ploted 
        labels=investment_labels, #labels that goes with each %
        autopct='%1.1f%%', #One decimal place to improve readability
        colors=investment_colors, #define the same colors as before
        wedgeprops={'edgecolor': 'white'} #define teh edges of each pie to be able to separate slices
    )
    ax_invest.axis('equal')  # Make the pie circular
    st.pyplot(fig_invest) #tie into streamlit app

    # This insight is meant to give backround on the why beahind investment desicions in a way that is wasy to undertsand for an individual without prior finance knowledge 
    st.markdown(f"""
    Based on your inputs:
    - **{variable_income }% Variable Income**: Higher risk, Focused on long-term growth.
    - **{fixed_income}% Fixed Income**: Lower risk, steady returns.
    - **{alternatives}% Alternatives**: Diversify your portfolio.
    """)

#Custom entity Patterns
import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')  # Load spaCy

# Add entity ruler (so we can add patterns later)
ruler = nlp.add_pipe("entity_ruler", before="ner", config={"phrase_matcher_attr": "LOWER"})

# 📌 Custom Investment Pattern Section
st.header("🧠 Assets You're Interested In for Investing")

# Initialize pattern list if not exist
if "custom_investment_patterns" not in st.session_state:
    st.session_state.custom_investment_patterns = []

# Input for new investment pattern
col1, col2 = st.columns(2)
with col1:
    custom_pattern = st.text_input("Investment Name (ex: Google)", key="custom_pattern_input")
with col2:
    custom_label = st.selectbox("Investment Type", ["VARIABLE INCOME", "FIXED INCOME", "ALTERNATIVE"], key="custom_label_input")

if st.button("Add Pattern"):
    if custom_pattern:
        # Add new pattern to session state
        new_pattern = {"label": custom_label, "pattern": custom_pattern}
        st.session_state.custom_investment_patterns.append(new_pattern)

        # Also add to the entity ruler so spaCy will recognize it
        ruler.add_patterns([new_pattern])

        st.success(f"Added: {custom_pattern} as {custom_label}")
    else:
        st.warning("Please enter an investment name.")

if st.button("See My Personalized Investment Plan"):

    # Prepare lists by type
    variable_income = [p["pattern"] for p in st.session_state.custom_investment_patterns if p["label"] == "STOCK"]
    fixed_income = [p["pattern"] for p in st.session_state.custom_investment_patterns if p["label"] == "BOND"]
    alternatives = [p["pattern"] for p in st.session_state.custom_investment_patterns if p["label"] == "ALTERNATIVE"]

    st.header("📌 Your Personalized Investment Suggestions")

    # Display recommendations
    st.markdown("**Your Variable Income investments should be:** " + (", ".join(variable_income) if variable_income else "None added."))

    st.markdown("**Your Fixed Income investments should be:** " + (", ".join(fixed_income) if fixed_income else "None added."))

    st.markdown("**Your Alternative investments should be:** " + (", ".join(alternatives) if alternatives else "None added."))