#Import Pandas
import pandas as pd

#Import Streamlit
import streamlit as st

#Install english language
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy import displacy



#Hi! My name is Silvana Mejia and I am a Junior majoring in Busienss Analytics at the University of Notre Dame. I want to work in Wealth Managment in the future.

# Streamlit app 
# Page Title
st.title("Custom Named Entity Recognition (NER) with spaCy")
st.markdown("""
Welcome to the **Custom NER Explorer**!

This app lets you explore how Named Entity Recognition (NER) works using **spaCy**. You can:
- Paste your own text
- Define your own custom entity labels and patterns (like people, places, tools, events, etc.)
- See your custom entities highlighted in the text using DisplaCy

Go ahead and follow the steps below!""")
            
# Step 1: Text Input or Upload
st.subheader("Step 1: Enter Your Text")
st.markdown("You can either paste your text or upload a .txt file below.")

# File uploader
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

# Text area for manual input
text_input = st.text_area("Or paste your text here:", height=200)

# Determine which input to use
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
elif text_input.strip():
    text = text_input
else:
    text = ""

#------------------------------------------------

# Step 2: Creating Custom Patterns
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
label = st.text_input("Entity Label (e.g. FRUIT, EVENT)", key= "label_input") #label_input key created to be able to reference later
pattern = st.text_input("Pattern to Match (e.g. apple, Bengal Bouts)", key = "pattern_input") #pattern_input key created to be able to reference later

#This if statement that adds new pattern to the custom_patterns list in the session, shows error message if pattern already in list or ask the user to add a pattern if text boxes left blank 
if st.button("➕ Add Entity Pattern"):  
    label = st.session_state.label_input.upper()
    pattern = st.session_state.pattern_input.lower()

    if label and pattern:
        new_pattern = {"label": label, "pattern": pattern} 

        if new_pattern in st.session_state.custom_patterns: #duplicate pattern
            st.warning("⚠️ That pattern and label have already been added.") #warning message displayed because its a pattern taht has already been added
        
        else: #new pattern
            st.session_state.custom_patterns.append({ 
            "label": label.upper(),
            "pattern": pattern.lower()
        })
        st.success(f"Pattern added Succesfuly: {label.upper()} → {pattern}") #success message displayed 
    else:
        st.warning("Please enter both a label and a pattern.") #warning message displayed because no new text was inputed


# This if statemnt adds a markdown with all aptetrns that have been created in teh session and is cleared in teh acse where the clear patterns button has been clicked
if st.session_state.custom_patterns:
    st.markdown("### ✅ Your Custom Patterns So Far:")

    for item in st.session_state.custom_patterns:
        st.write(f"• **{item['label']}** - {item['pattern']}")

    # Button that clears teh custom_patterns list and reruns makes teh app rerun. Since the only thing saved to the session is the custom_patterns list, the app functionality is not affected
    if st.button("🗑️ Clear All Patterns", key="clear_btn"):
        st.session_state.custom_patterns = []
        st.rerun()

#------------------------------------------------
# Step 3: Creating Entity Ruller

