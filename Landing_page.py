import streamlit as st
# from pathlib import Path

st.set_page_config(page_title="Bible Games", page_icon="📖")

st.title("📚 Welcome to Bible Games!")
st.subheader("Test your knowledge and have fun!")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    # st.image("https://cdn.pixabay.com/photo/2014/12/21/23/57/book-576513_1280.png", width=200)
    if st.button("🧩 Play Unscramble That Bible Book!"):
        st.switch_page("pages/1_Unscramble_that_chapter.py")

with col2:
    # st.image("https://cdn.pixabay.com/photo/2017/01/31/13/14/question-mark-2027266_1280.png", width=200)
    if st.button("🧠 Take the Bible Quiz!"):
        st.switch_page("pages/2_Bible_quiz.py")

st.markdown("---")

st.info("Choose a game from above to begin. Have fun and grow in the Word!")

st.caption("Made with ❤️ by Abatan Ayodeji • Built using Streamlit")