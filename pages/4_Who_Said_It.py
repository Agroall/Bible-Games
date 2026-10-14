import streamlit as st
import random
import game_utils

st.title("💬 Who Said It?")
st.write(
    "A two-player game of attribution. A line from Scripture appears, and the player "
    "on the clock names who said it. Get it right straight away for **2 points**. "
    "Miss, and your opponent can steal it for **1 point** with the help of a hint."
)

DIRECT_POINTS = 2
STEAL_POINTS = 1


@st.cache_data
def load_quotes():
    return game_utils.load_json("who_said_it.json", "quotes")


quotes = load_quotes()
NAME_INDEX = game_utils.build_name_index(quotes)


def is_correct(guess, quote):
    return game_utils.is_correct(guess, quote, NAME_INDEX)


def start_game(player_one, player_two, rounds):
    st.session_state.wsi_players = [player_one.strip() or "Player 1", player_two.strip() or "Player 2"]
    st.session_state.wsi_scores = [0, 0]
    st.session_state.wsi_deck = random.sample(range(len(quotes)), rounds)
    st.session_state.wsi_round = 0
    st.session_state.wsi_first = 0
    begin_round()


def begin_round():
    st.session_state.wsi_phase = "playing"
    st.session_state.wsi_stealing = False
    st.session_state.wsi_misses = []
    st.session_state.wsi_winner = None
    st.session_state.wsi_earned = 0


def current_quote():
    return quotes[st.session_state.wsi_deck[st.session_state.wsi_round]]


def current_player():
    offset = 1 if st.session_state.wsi_stealing else 0
    return (st.session_state.wsi_first + offset) % 2


def submit_guess(guess):
    """
    Score the guess, then either hand the question over as a steal or end
    the round once both players have had their turn.
    input: guess --> str
    """
    player = current_player()
    quote = current_quote()

    if is_correct(guess, quote):
        points = STEAL_POINTS if st.session_state.wsi_stealing else DIRECT_POINTS
        st.session_state.wsi_scores[player] += points
        st.session_state.wsi_winner = player
        st.session_state.wsi_earned = points
        st.session_state.wsi_phase = "reveal"
        return

    st.session_state.wsi_misses.append((st.session_state.wsi_players[player], guess.strip()))

    if st.session_state.wsi_stealing:
        st.session_state.wsi_phase = "reveal"
    else:
        st.session_state.wsi_stealing = True


def next_round():
    st.session_state.wsi_round += 1
    st.session_state.wsi_first = (st.session_state.wsi_first + 1) % 2

    if st.session_state.wsi_round >= len(st.session_state.wsi_deck):
        st.session_state.wsi_phase = "gameover"
    else:
        begin_round()


if "wsi_phase" not in st.session_state:
    st.session_state.wsi_phase = "setup"


if st.session_state.wsi_phase == "setup":
    st.markdown("---")
    st.subheader("Who is playing?")

    with st.form("wsi_setup"):
        left, right = st.columns(2)
        player_one = left.text_input("Player 1", placeholder="Player 1")
        player_two = right.text_input("Player 2", placeholder="Player 2")
        rounds = st.slider("How many quotes this game?", 3, 25, 10)

        if st.form_submit_button("▶️ Start Game", type="primary"):
            start_game(player_one, player_two, rounds)
            st.rerun()

    st.info("Answers are forgiving: 'Simon Peter', 'Peter' and 'Cephas' all count.")


elif st.session_state.wsi_phase in ("playing", "reveal"):
    players = st.session_state.wsi_players
    scores = st.session_state.wsi_scores
    quote = current_quote()

    st.sidebar.header("Scoreboard")
    st.sidebar.metric(players[0], scores[0])
    st.sidebar.metric(players[1], scores[1])
    st.sidebar.caption(f"Quote {st.session_state.wsi_round + 1} of {len(st.session_state.wsi_deck)}")
    if st.sidebar.button("🔄 End game and start over"):
        st.session_state.wsi_phase = "setup"
        st.rerun()

    st.markdown("---")
    st.markdown(
        f"<div style='border-left:4px solid #3b82f6; padding:12px 18px; "
        f"font-size:1.25em; font-style:italic; background:rgba(59,130,246,0.06)'>"
        f"&ldquo;{quote['quote']}&rdquo;</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    if st.session_state.wsi_misses:
        misses = ", ".join(f"{who} said *{what or '(blank)'}*" for who, what in st.session_state.wsi_misses)
        st.caption(f"❌ Already tried — {misses}")

    if st.session_state.wsi_phase == "playing":
        player = current_player()

        if st.session_state.wsi_stealing:
            st.warning(f"🔓 Steal chance for **{players[player]}** — worth {STEAL_POINTS} point.")
            st.info(f"💡 Hint: {quote['context']}")
        else:
            st.markdown(f"#### 🎤 {players[player]}, who said it? ({DIRECT_POINTS} pts)")

        with st.form("wsi_guess", clear_on_submit=True):
            guess = st.text_input("Speaker", placeholder="Type a name", label_visibility="collapsed")
            if st.form_submit_button("Submit answer", type="primary"):
                submit_guess(guess)
                st.rerun()

    else:
        winner = st.session_state.wsi_winner
        if winner is None:
            st.error(f"😬 Neither of you got it. It was **{quote['answer']}**.")
        else:
            st.success(
                f"🎉 **{players[winner]}** got it — it was **{quote['answer']}** "
                f"for **+{st.session_state.wsi_earned}** point(s)."
            )

        st.caption(f"{quote['context']}  ·  _{quote['reference']}_")
        st.markdown(f"**Score:** {players[0]} {scores[0]} — {scores[1]} {players[1]}")

        last = st.session_state.wsi_round + 1 >= len(st.session_state.wsi_deck)
        if st.button("🏁 See final result" if last else "➡️ Next quote", type="primary"):
            next_round()
            st.rerun()


else:
    players = st.session_state.wsi_players
    scores = st.session_state.wsi_scores

    st.markdown("---")
    st.subheader("🏆 Final Result")

    left, right = st.columns(2)
    left.metric(players[0], scores[0])
    right.metric(players[1], scores[1])

    if scores[0] == scores[1]:
        st.info(f"🤝 Dead even at {scores[0]} point(s) each!")
    else:
        champion = players[0] if scores[0] > scores[1] else players[1]
        st.success(f"🥇 **{champion}** wins with {max(scores)} point(s)!")

    if st.button("🔁 Play again", type="primary"):
        st.session_state.wsi_phase = "setup"
        st.rerun()


st.markdown("---")
st.caption("Developed with ❤️ by Abatan Ayodeji (Agroall) • Built using Streamlit")
