#Import Pandas
import pandas as pd

#Import Streamlit
import streamlit as st

#Install english language
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy import displacy

# Streamlit app 
# Page Title
st.title("Custom Named Entity Recognition (NER) with spaCy")
st.markdown("""
Welcome to the **Custom NER Explorer**!

This app lets you explore how Named Entity Recognition (NER) works using **spaCy**. You can:
- Paste or upload your own text
- Define your own custom entity labels and patterns
- See your custom entities highlighted in the text using DisplaCy

Go ahead and follow the steps below!""")
            
# Step 1: Text Input or Upload
st.subheader("Step 1: Enter Your Text")
st.markdown("You can either paste your text or upload a .txt file below.")
st.markdown("**Here is a sample text you can try**: ")
st.markdown("Hi! I’m Silvana Mejia, a junior at Notre Dame majoring in Business Analytics with minors in Finance and Computing. I’m passionate about the intersection between people and the financial industry, which is what led me to explore wealth management as a career path. Over the past few years, I’ve had the chance to intern in Barcelona and study abroad in London, two experiences that pushed me outside my comfort zone and taught me how to adapt quickly, work across cultures, and communicate clearly. I’m also actively involved in ALPFA, where I’ve found a community that motivates me to grow both professionally and personally. During my free time, I've become very passionate about Golf, Travel and learning to cook new dishes.")

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
st.subheader("Step 3: Apply Custom NER Rules")
st.markdown("Click below to process your text using the patterns you've defined. This will show both your custom entities and spaCy's built-in ones.")


if st.button("🔍 Run NER on Text"):
   if not text:
       st.warning("Please provide some text in Step 1.")
   elif not st.session_state.custom_patterns:
       st.warning("Please add at least one custom pattern in Step 2.")
   else:
       # Add the custom EntityRuler BEFORE the NER component so both show up, but custom rules are picked up prior to entities
       ruler = nlp.add_pipe("entity_ruler", before="ner", config={          
           "phrase_matcher_attr": "LOWER"        # Enable case-insensitive matching
       })


       # Add user-defined patterns
       ruler.add_patterns(st.session_state.custom_patterns)


       # Process the text
       doc = nlp(text)


       # Show detected entities
       if doc.ents:
           st.success("✅ Entities detected!")
           st.markdown("### Detected Entities:")
           for ent in doc.ents:
               st.write(f"• **{ent.text}** → `{ent.label_}`")


           # Visualize entities with displacy
           st.markdown("### Highlighted Text")
           html = displacy.render(doc, style="ent", page=True)
           st.components.v1.html(html, height=500, scrolling=True)


