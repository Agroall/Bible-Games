import streamlit as st
import random
import game_utils

st.title("🎭 Two Truths and a Lie")

st.write(
    "Three statements appear about a Bible person or event. Two are true and one "
    "is not. Players take turns spotting the lie, **1 point** for each one caught, "
    "and every round ends with the reason it was false."
)


@st.cache_data
def load_rounds():
    return game_utils.load_json("two_truths.json", "rounds")


rounds_data = load_rounds()


def start_game(player_one, player_two, rounds, solo):
    names = [player_one.strip() or "Player 1"]
    if not solo:
        names.append(player_two.strip() or "Player 2")

    st.session_state.ttl_players = names
    st.session_state.ttl_scores = [0] * len(names)
    st.session_state.ttl_deck = random.sample(range(len(rounds_data)), rounds)
    st.session_state.ttl_round = 0
    begin_round()


def begin_round():
    """Shuffle the three statements so the lie is not always in the same slot."""
    item = rounds_data[st.session_state.ttl_deck[st.session_state.ttl_round]]
    statements = list(item["truths"]) + [item["lie"]]
    order = random.sample(range(len(statements)), len(statements))

    st.session_state.ttl_statements = [statements[i] for i in order]
    st.session_state.ttl_lie_slot = order.index(len(statements) - 1)
    st.session_state.ttl_phase = "playing"
    st.session_state.ttl_picked = None


def current_item():
    return rounds_data[st.session_state.ttl_deck[st.session_state.ttl_round]]


def current_player():
    """Players alternate by round, so each gets a fresh item to judge."""
    return st.session_state.ttl_round % len(st.session_state.ttl_players)


def submit_pick(slot):
    """
    input: slot --> int, index of the statement the player believes is false
    """
    st.session_state.ttl_picked = slot
    if slot == st.session_state.ttl_lie_slot:
        st.session_state.ttl_scores[current_player()] += 1
    st.session_state.ttl_phase = "reveal"


def next_round():
    st.session_state.ttl_round += 1
    if st.session_state.ttl_round >= len(st.session_state.ttl_deck):
        st.session_state.ttl_phase = "gameover"
    else:
        begin_round()


if "ttl_phase" not in st.session_state:
    st.session_state.ttl_phase = "setup"


if st.session_state.ttl_phase == "setup":
    st.markdown("---")
    st.subheader("Who is playing?")

    with st.form("ttl_setup"):
        solo = st.checkbox("Playing alone")
        left, right = st.columns(2)
        player_one = left.text_input("Player 1", placeholder="Player 1")
        player_two = right.text_input("Player 2", placeholder="Player 2")
        rounds = st.slider("How many rounds?", 3, 25, 10)

        if st.form_submit_button("▶️ Start Game", type="primary"):
            start_game(player_one, player_two, rounds, solo)
            st.rerun()

    st.info("In two-player mode you alternate rounds, so you each judge different statements.")


elif st.session_state.ttl_phase in ("playing", "reveal"):
    players = st.session_state.ttl_players
    scores = st.session_state.ttl_scores
    item = current_item()
    player = current_player()

    st.sidebar.header("Scoreboard")
    for name, score in zip(players, scores):
        st.sidebar.metric(name, score)
    st.sidebar.caption(f"Round {st.session_state.ttl_round + 1} of {len(st.session_state.ttl_deck)}")
    if st.sidebar.button("🔄 End game and start over"):
        st.session_state.ttl_phase = "setup"
        st.rerun()

    st.markdown("---")
    st.markdown(f"### 📜 {item['subject']}")

    if st.session_state.ttl_phase == "playing":
        st.markdown(f"**{players[player]}** — which one is the lie?")
        for slot, statement in enumerate(st.session_state.ttl_statements):
            if st.button(f"{chr(65 + slot)}.  {statement}", key=f"ttl_{st.session_state.ttl_round}_{slot}", width="stretch"):
                submit_pick(slot)
                st.rerun()

    else:
        picked = st.session_state.ttl_picked
        lie_slot = st.session_state.ttl_lie_slot

        for slot, statement in enumerate(st.session_state.ttl_statements):
            label = f"**{chr(65 + slot)}.** {statement}"
            if slot == lie_slot:
                st.error(f"🚫 {label}  ← the lie")
            elif slot == picked:
                st.warning(f"❌ {label}  ← you picked this")
            else:
                st.success(f"✅ {label}")

        if picked == lie_slot:
            st.success(f"🎉 **{players[player]}** caught it! **+1** point.")
        else:
            st.info(f"😬 Not this time, {players[player]}.")

        st.caption(f"**Why it's false:** {item['why']}")

        last = st.session_state.ttl_round + 1 >= len(st.session_state.ttl_deck)
        if st.button("🏁 See final result" if last else "➡️ Next round", type="primary"):
            next_round()
            st.rerun()


else:
    players = st.session_state.ttl_players
    scores = st.session_state.ttl_scores
    total = len(st.session_state.ttl_deck)

    st.markdown("---")
    st.subheader("🏆 Final Result")

    for column, name, score in zip(st.columns(len(players)), players, scores):
        column.metric(name, score)

    if len(players) == 1:
        st.success(f"🎯 You caught **{scores[0]}** of **{total}** lies.")
    elif scores[0] == scores[1]:
        st.info(f"🤝 Dead even at {scores[0]} point(s) each!")
    else:
        champion = players[0] if scores[0] > scores[1] else players[1]
        st.success(f"🥇 **{champion}** wins with {max(scores)} point(s)!")

    if st.button("🔁 Play again", type="primary"):
        st.session_state.ttl_phase = "setup"
        st.rerun()


st.markdown("---")
st.caption("Developed with ❤️ by Abatan Ayodeji (Agroall) • Built using Streamlit")
