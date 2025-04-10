#Import Pandas
import pandas as pd

#Import Streamlit
import streamlit as st

#Hi! My name is Silvana Mejia and I am a Junior majoring in Busienss Analytics at the University of Notre Dame. I want to work in Wealth Managment in the future.

# Streamlit app 
# Page Title
st.title("Custom Named Entity Recognition (NER) with spaCy")
st.markdown("""
Welcome to the **Custom NER Explorer**!

This app lets you explore how Named Entity Recognition (NER) works using **spaCy**. You can:
- Paste your own text,
- Define your own custom entity labels and patterns (like people, places, tools, events, etc.)
- See your custom entities highlighted in the text"

Go ahead and follow the steps below!""")
            
# Step 1: Text Input
st.subheader("Step 1: Enter Your Text")
st.markdown("This can be the text passed through the Entity Rule we will created in Step 3")
text = st.text_area("Paste your text here:", height=200)
  
# Step 2: Define Custom Patterns
st.subheader("Step 2: Define Your Custom Entities")
st.markdown("""
Each entity needs:
    - **Label** = the type of thing you want to recognize (e.g. `"FRUIT"`, `"EVENT"`)
    - **Pattern** = the word or phrase you want to match (e.g. `"apple"`, `"Bengal Bouts"`)

**Example:**
- Label: FRUIT
- Pattern: apple

Add as many as you want!
""")

#This if statement checks if a list of custom patterns has alredy been created, if not cresated it is built and added to the session
if "custom_patterns" not in st.session_state: 
    st.session_state.custom_patterns = [] 

#I will define a clear_inputs() fucntion in order to make sure that text boxes are cleared when necessary
def clear_inputs():
    st.session_state.label_input = ""
    st.session_state.pattern_input = ""

#This is a text input box that allows the user to insert labels and patterns
label = st.text_input("Entity Label (e.g. FRUIT, EVENT)") #label_input key created to be able to reference later
pattern = st.text_input("Pattern to Match (e.g. apple, Bengal Bouts)") #pattern_input key created to be able to reference later

#This if statement that adds new pattern to the custom_patterns list in the session or ask the user to add a pattern if text boxes left blank 
if st.button("➕ Add Entity Pattern"): 
    if label and pattern:
        new_pattern = {"label": label, "pattern": pattern}

        if new_pattern in st.session_state.custom_patterns:
            st.warning("⚠️ That pattern and label have already been added.")
        
        else:
            st.session_state.custom_patterns.append({ 
            "label": label.upper(),
            "pattern": pattern.lower()
        })
        st.success(f"Pattern added Succesfuly: {label.upper()} → {pattern}") #success message displayed 
    else:
        st.warning("Please enter both a label and a pattern.") #warning message displayed because no new text was inputed

# Display added patterns
if st.session_state.custom_patterns:
    st.markdown("### ✅ Your Custom Patterns So Far:")
    for item in st.session_state.custom_patterns:
        st.write(f"• **{item['label']}** -  {item['pattern']}")
