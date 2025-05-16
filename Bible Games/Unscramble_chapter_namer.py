import streamlit as st
import time
import random

st.title('📖 Unscramble That Bible Book!')
st.write('Click to start!')

bible_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Samuel", "Kings", "Chronicles", "Nehemiah", "Esther",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Obadiah", 
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Romans", "Corinthians", "Galatians", 
    "Ephesians", "Philippians", "Colossians", "Thessalonians", "Timothy", "Titus", "Philemon", "Hebrews", "James", "Peter", "Revelation",
    "Amos", "Ezra", "Joel", "John", "Jude", "Luke", "Mark", "Ruth"
]

st.sidebar.header('Personalize Settings')
timer = st.sidebar.number_input('How many seconds per round?', 5, 30, step=5)
choice = st.sidebar.selectbox('Do you want chapeter with four letter?: 0 for yes, 1 for no', options = ('Yes', 'No'))

if choice == "No":
    bible_books = bible_books[0:46]

def scramble(word):
    word = word.lower()
    letters = list(word.replace(" ", ""))
    random.shuffle(letters)
    return ''.join(letters)

def start_countdown(timer=timer):
    countdown = st.empty()
    for i in range(timer, -1, -1):
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