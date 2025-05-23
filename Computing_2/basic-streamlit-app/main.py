'''
Instructions to Run the App:
1. Open terminal.
2. Navigate to the basic-streamlit-app folder:
    - cd MEJIA-PYTHON-PORTFOLIO/Computing II/basic-streamlit-app
3. Run Streamlit app with command below:
    - streamlit run main.py
4. Access the app in browser at the URL provided by Streamlit (SEE TERMINAL)
'''

# Import the Streamlit library
import streamlit as st
import pandas as pd

#Title Requirments
st.title("Customer Shopping Trends Analysis")
st.subheader("Explore Customer Shopping Data to understand recent trends and filter by parameters including Product Category, Item Type, Price Limit, Location and Gender.")

#Data Load
df = pd.read_csv("data/shopping_trends 2.csv")

#Data Preview
st.write("Here is a preview of the dataset:")
st.dataframe(df)

#Data Exploration
st.subheader("Data Exploration")
st.write("Explore the data by maniputaing the filters below:")

#Product Category Select box
category = st.selectbox("Select a Product Category", df["Category"].unique())

#Item Multiselect
items = st.multiselect("Select Items Purchased", df["Item Purchased"].unique())

#Price Sldier 
Price_Limit = st.slider("Select a Purchase Amount",\
    min_value=df["Amount(USD)"].min(),\
    max_value= df["Amount(USD)"].max())

#City Select box
State = st.selectbox("Select a Location", df["Location"].unique())

#Gender Select
gender_selection = st.radio("Select Gender", df["Gender"].unique())



#Filter Confirmation
st.subheader('Selected Filters')
st.write("*Please note that the filtered data will only include the selected items within the specified category.*")
st.write(f"**Selected Category:** {category}")
st.write(f"**Selected Items:** {items}")
st.write(f"**Selected Price Limit (USD):** ${Price_Limit}")
st.write(f"**Selected Location:** {State}")
st.write(f"**Selected Gender:** {gender_selection}")


#Final Filtered Data
st.subheader("Final Filtered Data")
if st.button("Click here to confirm your filter selections and view your Final Dataset!"):
    st.dataframe(df[(df["Category"] == category) & (df["Amount(USD)"] <= Price_Limit) & (df["Location"] == State) & (df["Gender"] == gender_selection) & (df["Item Purchased"].isin(items))])
else:
    st.write("Feel free to return and change any of your selections!")
