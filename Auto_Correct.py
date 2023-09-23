import streamlit as st
import spacy
import os
from spello.model import SpellCorrectionModel

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Define the model file path
model_path = "model/model.pkl"

# Initialize a spello spell correction model
if os.path.exists(model_path):
    # Load the trained model from the file
    spell_correction_model = SpellCorrectionModel()
    spell_correction_model.load(model_path)
else:
    # Training data
    with open("auto_correct.txt") as file:
        data = file.readlines()
    training_data = [i.strip() for i in data]

    # Train the spell correction model if the model file doesn't exist
    spell_correction_model = SpellCorrectionModel(language="en")
    spell_correction_model.train(training_data)
    # Save the trained model to a file
    spell_correction_model.save(model_path)

    # Function to correct a sentence


def spell_correct_sentence(sentence):
    # Tokenize the input sentence using spaCy
    doc = nlp(sentence)

    corrected_tokens = []

    for token in doc:
        if token.is_alpha:  # Only correct alphabetical tokens
            corrected = spell_correction_model.spell_correct(token.text)
            corrected_tokens.append(corrected['spell_corrected_text'])
        else:
            corrected_tokens.append(token.text)

    corrected_sentence = " ".join(corrected_tokens)
    return corrected_sentence


# Streamlit UI
st.title("Auto Correction App")

# Input box for the user to enter a sentence
input_text = st.text_area("Enter the sentence:", "")

# Button to perform spell correction
if st.button("Correct Spellings"):
    if input_text:
        corrected_sentence = spell_correct_sentence(input_text)

        # Compare the original and corrected sentences
        if input_text == corrected_sentence:
            st.write("Sentence is correct.")
        else:
            st.write("Suggested Sentence:", corrected_sentence)
    else:
        st.warning("Please enter a sentence.")

# Provide an example
st.subheader("Example:")
example_sentence = "This is an exampele senetnce with mstake."
corrected_example = spell_correct_sentence(example_sentence)
st.write("Original Sentence:", example_sentence)
st.write("Suggested Sentence:", corrected_example)
