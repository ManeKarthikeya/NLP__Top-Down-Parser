import streamlit as st
from graphviz import Digraph
import time

# ----------------------------------
# PAGE CONFIG (PROFESSIONAL UI)
# ----------------------------------
st.set_page_config(page_title="Top-Down Parser Pro", layout="wide")

# ----------------------------------
# GRAMMAR (CLEAN)
# ----------------------------------
grammar = {

    "S": [["NP", "VP"]],

    "NP": [["Det", "N", "NP_TAIL"],
           ["Det", "Adj", "N", "NP_TAIL"],
           ["N"]],

    "NP_TAIL": [["PP", "NP_TAIL"], []],

    "VP": [["V", "VP_TAIL"],
           ["Aux", "V", "NP", "VP_TAIL"]],

    "VP_TAIL": [["NP", "VP_TAIL"],
                ["PP", "VP_TAIL"],
                ["Adv", "VP_TAIL"],
                []],

    "PP": [["P", "NP"]],

    "Det": [["the"], ["a"], ["an"]],

    "N": [["cat"], ["dog"], ["mouse"], ["boy"], ["girl"],
          ["teacher"], ["lesson"], ["ball"], ["apple"],
          ["garden"], ["man"], ["newspaper"], ["fox"],
          ["fence"], ["mat"], ["park"], ["friend"],
          ["table"], ["tree"], ["students"], ["homework"],
          ["library"], ["child"], ["bird"]],

    "V": [["chased"], ["barked"], ["kicked"], ["ate"],
          ["explained"], ["played"], ["read"], ["ran"],
          ["walked"], ["slept"], ["flew"], ["jumped"],
          ["gave"], ["sat"], ["reading"]],

    "Aux": [["is"]],

    "Adj": [["small"], ["frightened"], ["happy"],
            ["old"], ["clever"]],

    "Adv": [["quickly"], ["loudly"], ["away"]],

    "P": [["on"], ["in"], ["under"], ["over"], ["to"], ["with"]]
}

# ----------------------------------
# GLOBAL TRACKERS
# ----------------------------------
steps = []
max_index_reached = 0

# ----------------------------------
# PARSER
# ----------------------------------
def parse(symbol, words, index):

    global steps, max_index_reached

    max_index_reached = max(max_index_reached, index)

    steps.append(f"👉 {symbol} → {' '.join(words[index:])}")

    # Terminal
    if symbol not in grammar:
        if index < len(words) and words[index] == symbol:
            steps.append(f"✅ Match '{symbol}'")
            return [(index + 1, (symbol, []))]
        else:
            steps.append(f"❌ Fail '{symbol}'")
            return []

    results = []

    for production in grammar[symbol]:

        if production == []:
            results.append((index, (symbol, [])))
            continue

        steps.append(f"🔹 {symbol} → {' '.join(production)}")

        partial = [(index, [])]

        for sym in production:
            new_partial = []

            for idx, children in partial:
                parsed = parse(sym, words, idx)

                for new_idx, subtree in parsed:
                    new_partial.append((new_idx, children + [subtree]))

            partial = new_partial

        for idx, children in partial:
            results.append((idx, (symbol, children)))

    return results


# ----------------------------------
# DRAW TREE
# ----------------------------------
def draw_tree(tree, graph, parent=None, counter=[0]):
    node_id = str(counter[0])
    counter[0] += 1

    label, children = tree
    graph.node(node_id, label)

    if parent:
        graph.edge(parent, node_id)

    for child in children:
        draw_tree(child, graph, node_id, counter)


# ----------------------------------
# SIDEBAR (PRO UI)
# ----------------------------------
st.sidebar.title("⚙️ Controls")

sentence = st.sidebar.text_input(
    "Enter sentence:",
    "The small cat chased the mouse"
)

speed = st.sidebar.slider("Animation Speed", 0.01, 1.0, 0.2)

run = st.sidebar.button("▶ Run Parser")

# ----------------------------------
# MAIN UI
# ----------------------------------
st.title("🧠 Top-Down Parser Pro")

tab1, tab2, tab3 = st.tabs(["🌳 Parse Tree", "📜 Steps", "📊 Analysis"])

# ----------------------------------
# RUN
# ----------------------------------
if run:

    words = sentence.lower().replace(".", "").split()

    steps.clear()
    max_index_reached = 0

    results = parse("S", words, 0)

    valid = [tree for idx, tree in results if idx == len(words)]

    # ----------------------------------
    # METRICS
    # ----------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Words", len(words))
    col2.metric("Parsed", max_index_reached)

    if valid:
        col3.metric("Status", "VALID ✅")
    else:
        col3.metric("Status", "INVALID ❌")

    # ----------------------------------
    # TAB 1: TREE
    # ----------------------------------
    with tab1:

        if valid:
            graph = Digraph()
            draw_tree(valid[0], graph)
            st.graphviz_chart(graph)

        else:
            st.warning("No valid parse tree")

    # ----------------------------------
    # TAB 2: STEPS
    # ----------------------------------
    with tab2:
        for i, s in enumerate(steps):
            st.text(f"{i+1}. {s}")

    # ----------------------------------
    # TAB 3: ERROR ANALYSIS
    # ----------------------------------
    with tab3:

        if not valid:

            st.subheader("❌ Error Analysis")

            error_word = words[max_index_reached] if max_index_reached < len(words) else "END"

            # Highlight sentence
            highlighted = []

            for i, w in enumerate(words):
                if i == max_index_reached:
                    highlighted.append(f"❌ **{w}**")
                else:
                    highlighted.append(w)

            st.write("### Sentence Breakdown:")
            st.write(" ".join(highlighted))

            st.write(f"### 🔍 Error at word: **{error_word}**")

            st.write("### 💡 Possible Reasons:")
            st.write("- Word not expected in this position")
            st.write("- Missing grammar rule")
            st.write("- Incorrect sentence structure")

        else:
            st.success("No errors detected 🎉")