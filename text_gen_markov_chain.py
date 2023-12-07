import PyPDF2 as pypdf
import re
import random
from collections import defaultdict, Counter
import streamlit as st

shrek_script = pypdf.PdfReader('shrek_script.pdf')
pages = shrek_script.pages

text = ''

for page in pages:
    text += page.extract_text()

text = text.replace('\n', ' ')
text = text.replace('  ', ' ')

def build_markov_chain(text):
    words = re.findall(r'\w+', text.lower())
    markov_chain = defaultdict(Counter)

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        markov_chain[current_word][next_word] += 1

    return markov_chain

def generate_sentence(markov_chain, seed_word, length=50):
    current_word = seed_word
    generated_text = [current_word]

    for i in range(length - 1):
        next_word = random.choices(list(markov_chain[current_word].keys()), 
        weights=list(markov_chain[current_word].values()))[0]
        generated_text.append(next_word)
        current_word = next_word
    
    return ' '.join(generated_text)

st.image('shrek.png')
st.title('Shrek-ify')
st.subheader(''' :green[What a Movie Line For a Movie Made By Shrek Would Look Like] ''')
st.write('This is a Markov Chain that was trained on the Shrek script. It generates a sentence based on the previous word.')

input_text = text
markov_chain = build_markov_chain(input_text)
start_word = st.text_input('Enter a word to start the sentence with')
length = st.slider('Length of sentence', 10, 100, 50)

if st.button('Generate Line'):
    # check if the word is in the dictionary
    if start_word not in markov_chain:
        st.write('Word not in the Shrek script. Please try again.')
    else:
        st.write(generate_sentence(markov_chain, start_word, length))