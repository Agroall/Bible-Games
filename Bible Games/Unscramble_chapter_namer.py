import streamlit as st
import time
import random

st.title('📖 Unscramble That Bible Book!') # Page Title
st.write('Click to start!') # Page Description

bible_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Samuel", "Kings", "Chronicles", "Nehemiah", "Esther",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Obadiah", 
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Romans", "Corinthians", "Galatians", 
    "Ephesians", "Philippians", "Colossians", "Thessalonians", "Timothy", "Titus", "Philemon", "Hebrews", "James", "Peter", "Revelation",
    "Amos", "Ezra", "Joel", "John", "Jude", "Luke", "Mark", "Ruth"
]


def reset_list():
    global bible_books
    bible_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Samuel", "Kings", "Chronicles", "Nehemiah", "Esther",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Obadiah", 
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Romans", "Corinthians", "Galatians", 
    "Ephesians", "Philippians", "Colossians", "Thessalonians", "Timothy", "Titus", "Philemon", "Hebrews", "James", "Peter", "Revelation",
    "Amos", "Ezra", "Joel", "John", "Jude", "Luke", "Mark", "Ruth"
]

st.sidebar.header('Personalize Settings') # Control bar
timer = st.sidebar.number_input('How many seconds per round?', 5, 30, step=5) # Guessing time for each round
choice = st.sidebar.selectbox('Do you want chapters with four letter?: 0 for yes, 1 for no', options = ('Yes', 'No')) # Game difficulty
st.sidebar.button("Click here to reset the game.", on_click=reset_list)


if choice == "Yes":
    bible_books = [book for book in bible_books if len(book.replace(" ", "")) >= 4]
else:
    bible_books = [book for book in bible_books if len(book.replace(" ", "")) > 4]


def scramble(word):
    """
    Unscrambles the chosen book.
    input: word --> str
    """

    word = word.lower() # Sets all the letter in lowercase to improve difficulty.
    letters = list(word.replace(" ", "")) # Removes the blank spaces for multi word books.
    random.shuffle(letters) # Scramble the word.
    if random.shuffle(letters) == letters:
        random.shuffle(letters)
    return ''.join(letters) # Rearranges the scrambled word

def start_countdown(timer=timer):
    """
    Set the timer for each guessing round.
    input: timer --> int
    input set from the sidebar
    """

    countdown = st.empty()
    for i in range(timer, -1, -1):
        countdown.markdown(f"<h1 style='text-align: center; color: red;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(1)
    st.success("⏱️ Time's up!")

if 'current_book' not in st.session_state:
    st.session_state.current_book = None
if 'scrambled' not in st.session_state:
    st.session_state.scrambled = None

if 'used_books' not in st.session_state:
    st.session_state.used_books = []

remaining_books = [book for book in bible_books if book not in st.session_state.used_books]

if st.button("🔀 Generate Scrambled Book"):
    if not remaining_books:
        st.warning("🎉 You've unscrambled all books! Please reset to play again.")
    else:
        chosen = random.choice(remaining_books)
        st.session_state.current_book = chosen
        st.session_state.scrambled = scramble(chosen)
        st.session_state.used_books.append(chosen)


if st.session_state.scrambled:
    st.subheader("🧩 Unscramble this:")
    st.markdown(
    f"<div style='text-align: center; font-size: 120px; color: blue;'>{st.session_state.scrambled}</div>",
    unsafe_allow_html=True
)

    
    start_countdown()
    
    st.info(f"✅ The correct answer was: **{st.session_state.current_book}**")

st.markdown("---")
st.caption("Developed with ❤️ by Abatan Ayodeji (Agroall) • Built using Streamlit")