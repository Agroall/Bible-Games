import streamlit as st
import random
import game_utils

st.title("🕵️ Who Am I?")
st.write(
    "A two-player guessing game. Each round, a Bible character speaks in riddles. "
    "Up to **three clues** are given, and they get easier as they go. "
    "After every clue each player gets one guess, so answer early to score big: "
    "**3 points** on the first clue, **2** on the second, **1** on the third."
)

CLUES_PER_ROUND = 3
PLAYERS_PER_CLUE = 2
POINTS_BY_CLUE = [3, 2, 1]


@st.cache_data
def load_characters():
    return game_utils.load_json("who_am_i.json", "characters")


characters = load_characters()
NAME_INDEX = game_utils.build_name_index(characters)


def is_correct(guess, character):
    return game_utils.is_correct(guess, character, NAME_INDEX)


def start_game(team_one, team_two, rounds):
    """
    Deal a fresh shuffled deck and zero the scoreboard.
    input: team_one --> str, team_two --> str, rounds --> int
    """

    st.session_state.wai_teams = [team_one.strip() or "Player 1", team_two.strip() or "Player 2"]
    st.session_state.wai_scores = [0, 0]
    st.session_state.wai_deck = random.sample(range(len(characters)), rounds)
    st.session_state.wai_round = 0
    st.session_state.wai_first = 0
    begin_round()


def begin_round():
    """Reset the per-round counters without touching the scoreboard."""

    st.session_state.wai_phase = "playing"
    st.session_state.wai_clue = 0
    st.session_state.wai_slot = 0
    st.session_state.wai_misses = []
    st.session_state.wai_winner = None
    st.session_state.wai_earned = 0


def current_player():
    """Index of whoever is on the clock, alternating who leads each round."""

    return (st.session_state.wai_first + st.session_state.wai_slot) % PLAYERS_PER_CLUE


def submit_guess(guess):
    """
    Score a guess, then advance the turn, the clue, or the round.
    input: guess --> str
    """

    player = current_player()
    character = characters[st.session_state.wai_deck[st.session_state.wai_round]]

    if is_correct(guess, character):
        points = POINTS_BY_CLUE[st.session_state.wai_clue]
        st.session_state.wai_scores[player] += points
        st.session_state.wai_winner = player
        st.session_state.wai_earned = points
        st.session_state.wai_phase = "reveal"
        return

    st.session_state.wai_misses.append((st.session_state.wai_teams[player], guess.strip()))
    st.session_state.wai_slot += 1

    if st.session_state.wai_slot < PLAYERS_PER_CLUE:
        return

    st.session_state.wai_slot = 0
    st.session_state.wai_clue += 1

    if st.session_state.wai_clue >= CLUES_PER_ROUND:
        st.session_state.wai_phase = "reveal"


def next_round():
    """Move to the next character, or end the game if the deck is spent."""

    st.session_state.wai_round += 1
    st.session_state.wai_first = (st.session_state.wai_first + 1) % PLAYERS_PER_CLUE

    if st.session_state.wai_round >= len(st.session_state.wai_deck):
        st.session_state.wai_phase = "gameover"
    else:
        begin_round()


if "wai_phase" not in st.session_state:
    st.session_state.wai_phase = "setup"


# ---- Setup -------------------------------------------------------------------
if st.session_state.wai_phase == "setup":
    st.markdown("---")
    st.subheader("Who is playing?")

    with st.form("wai_setup"):
        name_col1, name_col2 = st.columns(2)
        team_one = name_col1.text_input("Player 1", placeholder="Player 1")
        team_two = name_col2.text_input("Player 2", placeholder="Player 2")
        rounds = st.slider("How many characters this game?", 3, 20, 10)

        if st.form_submit_button("▶️ Start Game", type="primary"):
            start_game(team_one, team_two, rounds)
            st.rerun()

    st.info("Player 1 guesses first in round one, and the lead swaps every round.")


# ---- Playing and reveal ------------------------------------------------------
elif st.session_state.wai_phase in ("playing", "reveal"):
    teams = st.session_state.wai_teams
    scores = st.session_state.wai_scores
    character = characters[st.session_state.wai_deck[st.session_state.wai_round]]

    st.sidebar.header("Scoreboard")
    st.sidebar.metric(teams[0], scores[0])
    st.sidebar.metric(teams[1], scores[1])
    st.sidebar.caption(f"Round {st.session_state.wai_round + 1} of {len(st.session_state.wai_deck)}")
    if st.sidebar.button("🔄 End game and start over"):
        st.session_state.wai_phase = "setup"
        st.rerun()

    st.markdown("---")

    revealed = (
        CLUES_PER_ROUND
        if st.session_state.wai_phase == "reveal"
        else st.session_state.wai_clue + 1
    )
    for index in range(revealed):
        st.markdown(f"**Clue {index + 1} ({POINTS_BY_CLUE[index]} pts):** _{character['clues'][index]}_")

    if st.session_state.wai_misses:
        misses = ", ".join(f"{name} said *{guess or '(blank)'}*" for name, guess in st.session_state.wai_misses)
        st.caption(f"❌ Already tried — {misses}")

    if st.session_state.wai_phase == "playing":
        player = current_player()
        st.markdown(f"#### 🎤 {teams[player]}, your guess")

        with st.form("wai_guess", clear_on_submit=True):
            guess = st.text_input("Who am I?", placeholder="Type a name", label_visibility="collapsed")
            if st.form_submit_button("Submit guess", type="primary"):
                submit_guess(guess)
                st.rerun()

    else:
        winner = st.session_state.wai_winner
        if winner is None:
            st.error(f"😬 Nobody got it. The answer was **{character['answer']}**.")
        else:
            st.success(
                f"🎉 **{teams[winner]}** got it! The answer was **{character['answer']}** "
                f"— that's **+{st.session_state.wai_earned}** point(s)."
            )

        st.markdown(f"**Score:** {teams[0]} {scores[0]} — {scores[1]} {teams[1]}")

        last_round = st.session_state.wai_round + 1 >= len(st.session_state.wai_deck)
        if st.button("🏁 See final result" if last_round else "➡️ Next character", type="primary"):
            next_round()
            st.rerun()


# ---- Game over ---------------------------------------------------------------
else:
    teams = st.session_state.wai_teams
    scores = st.session_state.wai_scores

    st.markdown("---")
    st.subheader("🏆 Final Result")

    score_col1, score_col2 = st.columns(2)
    score_col1.metric(teams[0], scores[0])
    score_col2.metric(teams[1], scores[1])

    if scores[0] == scores[1]:
        st.info(f"🤝 It's a tie at {scores[0]} point(s) each!")
    else:
        champion = teams[0] if scores[0] > scores[1] else teams[1]
        st.success(f"🥇 **{champion}** wins with {max(scores)} point(s)!")

    if st.button("🔁 Play again", type="primary"):
        st.session_state.wai_phase = "setup"
        st.rerun()


st.markdown("---")
st.caption("Developed with ❤️ by Abatan Ayodeji (Agroall) • Built using Streamlit")
