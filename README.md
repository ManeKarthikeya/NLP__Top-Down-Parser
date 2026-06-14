
# 🧠 Top-Down Parser 

A professional Streamlit-based implementation of a **Top-Down Recursive Descent Parser** for Context-Free Grammars (CFGs). The application parses English-like sentences, generates parse trees, visualizes parsing steps, and provides error analysis for invalid inputs. 

## Features

* 🌳 Parse Tree Visualization using Graphviz
* 🔄 Recursive Top-Down Parsing
* 📜 Step-by-Step Parsing Trace
* ❌ Error Detection and Analysis
* 📊 Parsing Metrics Dashboard
* ⚡ Adjustable Animation Speed
* 🎨 Interactive Streamlit UI

## Grammar Supported

The parser supports:

* Noun Phrases (NP)
* Verb Phrases (VP)
* Prepositional Phrases (PP)
* Determiners, Adjectives, Nouns
* Verbs, Adverbs, Auxiliary Verbs

Example sentence:

```text
The small cat chased the mouse
```

## Technologies Used

* Python
* Streamlit
* Graphviz

## Installation

```bash
pip install streamlit graphviz
```

## Run the Application

```bash
streamlit run top_down_parser_app.py
```

## How It Works

1. User enters a sentence.
2. The parser recursively expands grammar productions.
3. Matching terminals are validated against input tokens.
4. A parse tree is generated for valid sentences.
5. Invalid sentences trigger detailed error analysis highlighting the failure point.

## Output

The application provides:

* Parse Tree Visualization
* Parsing Steps Log
* Word & Parsing Metrics
* Error Location Detection
* Grammar-Based Validation

## Educational Applications

* Compiler Design Labs
* Natural Language Processing Courses
* Context-Free Grammar Demonstrations
* Recursive Descent Parsing Visualization
* Syntax Analysis Learning Tools

---
