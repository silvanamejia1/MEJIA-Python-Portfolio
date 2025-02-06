# Import the Streamlit library
import streamlit as st
import pandas as pd

st.write("Hello, streamlit")
st.title("Welcome!")
st.markdown("This is a basic Streamlit app")
st.write("This app displays a simple DataFrame as a demonstration.")

#Color Picker Button
if st.button("Click me to pick a color!"):
    color = st.color_picker("Pick a color", "#00f900")
else:
    st.write("Click me to view a Dataset!")
    st.subheader("Look at the Dataset Below!")
    #aca poner un boton que haga otra cosa (puede ser explore a data frame)

