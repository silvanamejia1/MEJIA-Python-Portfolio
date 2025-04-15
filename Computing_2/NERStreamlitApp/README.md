# Custom Named Entity Recognition (NER) with spaCy and Streamlit

## Project Overview

### Purpose of this App

This app explores Named Entity Recognition (NER) using the spaCy library. The purpose of the project is to allow users to upload or paste their own text, define custom entities using spaCy's `EntityRuler`, and visualize both custom and built-in entities in the text. It uses Streamlit for the interface and `displacy` for entity visualization.

Going deeper into spaCys approached to NER, spaCy's trained pipelines combine statistical models and linguistic rules to identify entities such as names, organizations, and locations in context. The app uses spaCy’s default English pipeline (en_core_web_sm).
In addition to built-in NER, the app allows users to define custom entity patterns using spaCy’s EntityRuler. The result is a blended system where both custom and pre-trained entities are visualized in the text. 	In the NERStreamlitApp, we push the text through the entity ruler first in order to highlight patterns before they are picked up by the NER pipeline. In the end both user generated patterns and entities are highlighted.

## Instructions

### Installation
#### To run the app locally, follow the steps below:
1. Open terminal inside main portafolio (MEJIA-Python-Portfolio)
2. Run ‘pip install pipreqs’ command
2. Navigate to the NERStreamlitApp folder:
   - ‘cd MEJIA-PYTHON-PORTFOLIO/Computing II/NERStreamlitApp’
3. Run ‘ls’ command to check you are in the right folder (should be NERStreamlitApp)
4. Run ‘pipreqs’ command to create text file in folder  
5. Run  ‘streamlit run NERStreamlitApp.py’ to open stremlit browser 

#### Link to deployed version 
https://mejia-python-portfolio-xc8cd8k6emvanofpqkrmqs.streamlit.app/

### Required Libraries and Intsalation Commands
- spaCy (and spaCys English model)
	- import spacy
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
- streamlit
	- import streamlit as st
- pandas 
    - import pandas as pd


## App Features

### Step 1: Upload or Paste Text

- Users can upload a `.txt` file or paste their own custom text into a text area.
- A sample text is provided in the app to allow for initial exploration and guidance.
- The uploaded or entered text is processed to extract named entities.

### Step 2: Define Custom Entities

- Users define custom entities by entering:
  - `Label`: The category name(e.g., `MAJOR`, `YEAR`, `CLUBS`)
  - `Pattern`: Specific example of item in the category (e.g., `business analytics`, `junior`, `ALPFA`)
- Patterns are case-insensitive.
- Duplicate patterns are not re-recorded.
- All added patterns are displayed in a list with the option to clear them.
- If a pattern is not added and “Add Pattern” is clicked warning message is displayed

### Step 3: Apply Custom NER Rules

- The app uses a combination of:
  - spaCy's built-in model (`en_core_web_sm`)
  - A custom `EntityRuler` inserted before the built-in NER (step 2)
- Detected entities are shown in two ways:
  - A structured list of recognized entity-label pairs.
  - Highlighted text using spaCy’s `displacy` visualizer embedded in Streamlit.

## References
- Using the ['spaCy 101']('https://spacy.io/usage/spacy-101') website was extremily useful to understand how spaCy operates on the backend to recognize certains parts of text. This also helped me link to the way it connects to its NER feature and EntityRuler processing pipeline.
