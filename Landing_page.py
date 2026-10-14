import streamlit as st
# from pathlib import Path

st.set_page_config(page_title="Bible Games", page_icon="📖")

st.title("📚 Welcome to Bible Games!")
st.subheader("Test your knowledge and have fun!")

st.markdown("---")

games = [
    ("🧩", "Unscramble That Book", "Beat the clock", "pages/1_Unscramble_that_chapter.py"),
    ("🧠", "Bible Quiz", "Four difficulty levels", "pages/2_Bible_quiz.py"),
    ("🕵️", "Who Am I?", "2 players · 3 clues", "pages/3_Who_Am_I.py"),
    ("💬", "Who Said It?", "2 players · name the speaker", "pages/4_Who_Said_It.py"),
    ("🎭", "Two Truths and a Lie", "1-2 players · spot the lie", "pages/5_Two_Truths_And_A_Lie.py"),
]


def game_card(column, icon, name, blurb, page):
    with column:
        st.markdown(
            f"<div style='text-align:center; min-height:132px; display:flex; flex-direction:column; "
            f"align-items:center; justify-content:flex-start'>"
            f"<div style='font-size:44px; line-height:1.2'>{icon}</div>"
            f"<div style='font-weight:600; margin-top:4px'>{name}</div>"
            f"<div style='color:#6b7280; font-size:0.82em'>{blurb}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        if st.button("Play", key=page, width="stretch"):
            st.switch_page(page)


for column, game in zip(st.columns(3, gap="medium"), games[:3]):
    game_card(column, *game)

st.write("")

bottom = st.columns(3, gap="medium")
for column, game in zip(bottom, games[3:]):
    game_card(column, *game)

st.markdown("---")

st.info("Choose a game from above to begin. Have fun and grow in the Word!")

st.caption("Made with ❤️ by Abatan Ayodeji • Built using Streamlit")