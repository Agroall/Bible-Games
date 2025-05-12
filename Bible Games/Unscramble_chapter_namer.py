import streamlit as st
import time
import random

st.title('📖 Unscramble That Bible Book!')
st.write('Click to start!')

# Bible books with duplicates like "1 Samuel" and "2 Samuel" merged
bible_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Samuel", "Kings", "Chronicles", "Nehemiah", "Esther",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Obadiah", 
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Romans", "Corinthians", "Galatians", 
    "Ephesians", "Philippians", "Colossians", "Thessalonians", "Timothy", "Titus", "Philemon", "Hebrews", "James", "Peter", "Revelation"
]

def scramble(word):
    word = word.lower()
    letters = list(word.replace(" ", ""))
    random.shuffle(letters)
    return ''.join(letters)

def start_countdown():
    countdown = st.empty()
    for i in range(10, -1, -1):
        countdown.markdown(f"<h1 style='text-align: center; color: red;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(1)
    st.success("⏱️ Time's up!")

# Session state to persist book across reruns
if 'current_book' not in st.session_state:
    st.session_state.current_book = None
if 'scrambled' not in st.session_state:
    st.session_state.scrambled = None

if st.button("🔀 Generate Scrambled Book"):
    chosen = random.randint(0, len(bible_books)-1)
    st.session_state.current_book = bible_books[chosen]
    st.session_state.scrambled = scramble(bible_books[chosen])

if st.session_state.scrambled:
    st.subheader("🧩 Unscramble this:")
    st.markdown(f"<h2 style='text-align: center; color: blue;'>{st.session_state.scrambled}</h2>", unsafe_allow_html=True)
    
    start_countdown()
    
    st.info(f"✅ The correct answer was: **{st.session_state.current_book}**")
