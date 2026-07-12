import streamlit as st
import requests

st.set_page_config(page_title="Learning Agent", page_icon="✦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 3rem 2rem 5rem; max-width: 720px; }
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 15% 0%, #14142b 0%, #0a0a0c 45%);
}

/* ---- Hero ---- */
.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: .9rem;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(167,139,250,.08);
    border: 1px solid rgba(167,139,250,.25);
}
.hero-title {
    font-size: 34px;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #b3b3c6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: .5rem;
}
.hero-sub { font-size: 14.5px; color: #8a8a95; margin-bottom: 2.25rem; }

/* ---- Step indicator ---- */
.steps { display: flex; align-items: center; gap: 0; margin-bottom: 2rem; }
.step { display: flex; align-items: center; gap: 8px; font-size: 12.5px; color: #4b4b55; }
.step.active { color: #fff; font-weight: 600; }
.step.done { color: #a78bfa; }
.step-num {
    width: 22px; height: 22px; border-radius: 50%;
    border: 1px solid #2a2a35; background: transparent;
    font-size: 10.5px; font-weight: 600;
    display: flex; align-items: center; justify-content: center; color: #4b4b55;
    transition: all .2s;
}
.step.active .step-num { background: linear-gradient(135deg,#8b5cf6,#6366f1); color: #fff; border-color: transparent; box-shadow: 0 0 0 4px rgba(139,92,246,.15); }
.step.done .step-num { background: rgba(167,139,250,.12); color: #a78bfa; border-color: rgba(167,139,250,.35); }
.step-line { flex: 1; height: 1px; background: #22222c; margin: 0 10px; min-width: 16px; }
.step-line.done { background: linear-gradient(90deg,#a78bfa,#22222c); }

/* ---- Cards ---- */
.card {
    background: linear-gradient(180deg, #131318 0%, #101014 100%);
    border: 1px solid #232330;
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,.25);
}
.field-label {
    font-size: 11.5px; font-weight: 600; color: #7d7d8a;
    letter-spacing: .06em; text-transform: uppercase; margin-bottom: .7rem;
}

/* ---- Divider ---- */
.divider { height: 1px; background: linear-gradient(90deg, transparent, #232330, transparent); margin: 2.25rem 0; }

/* ---- Section label ---- */
.section-label {
    display: flex; align-items: center; gap: 8px;
    font-size: 11.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
    color: #6b6b78; margin-bottom: 1rem;
}
.section-label .dot { width: 6px; height: 6px; border-radius: 50%; background: #6366f1; box-shadow: 0 0 8px #6366f1; }

/* ---- Topic tag ---- */
.topic-tag {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 12.5px; font-weight: 600; padding: 6px 13px; border-radius: 999px;
    background: rgba(99,102,241,.1); color: #a5b4fc;
    border: 1px solid rgba(99,102,241,.28); margin-bottom: 1.1rem;
}

/* ---- Explanation card ---- */
.explanation-card {
    background: #0e0e13; border: 1px solid #1e1e28; border-radius: 12px;
    padding: 1.4rem 1.6rem; font-size: 14.5px; line-height: 1.85; color: #d4d4dc;
}

/* ---- MCQ ---- */
.mcq-item {
    background: #0e0e13; border: 1px solid #1e1e28; border-radius: 14px;
    padding: 1.25rem 1.4rem; margin-bottom: .85rem;
}
.mcq-q { font-size: 14.5px; font-weight: 600; color: #f0f0f3; margin-bottom: .9rem; line-height: 1.5; }
.mcq-opt {
    font-size: 13.5px; color: #8f8f9c; padding: 7px 10px; margin-bottom: 4px;
    display: flex; align-items: center; gap: 10px; border-radius: 8px; background: #131319;
}
.mcq-opt.correct { color: #86efac; background: rgba(74,222,128,.08); border: 1px solid rgba(74,222,128,.25); }
.mcq-letter {
    width: 20px; height: 20px; border-radius: 6px; background: #1c1c26; color: #6b6b78;
    font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.mcq-opt.correct .mcq-letter { background: rgba(74,222,128,.2); color: #4ade80; }
.mcq-check { margin-left: auto; color: #4ade80; font-size: 13px; }

/* ---- Review banner ---- */
.review-pass, .review-fail {
    border-radius: 12px; padding: .9rem 1.15rem; font-size: 13.5px; font-weight: 600;
    margin-bottom: 1.1rem; display: flex; align-items: center; gap: 10px;
}
.review-pass { background: rgba(74,222,128,.08); border: 1px solid rgba(74,222,128,.3); color: #4ade80; }
.review-fail { background: rgba(248,113,113,.08); border: 1px solid rgba(248,113,113,.3); color: #f87171; }

/* ---- Feedback ---- */
.feedback-item {
    font-size: 13.5px; color: #a0a0ac; padding: 6px 0; display: flex;
    align-items: flex-start; gap: 10px; line-height: 1.6;
}
.feedback-bullet { width: 5px; height: 5px; border-radius: 50%; background: #6366f1; flex-shrink: 0; margin-top: 8px; }

/* ---- Refined badge ---- */
.refined-badge {
    display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 700;
    padding: 5px 12px; border-radius: 999px;
    background: linear-gradient(135deg, rgba(167,139,250,.15), rgba(99,102,241,.15));
    color: #c4b5fd; border: 1px solid rgba(167,139,250,.35); margin-bottom: 1.1rem;
}

/* ---- Grade selector (segmented control fallback styling) ---- */
div[data-testid="stSegmentedControl"] label {
    border-radius: 8px !important;
}

/* ---- Streamlit input overrides ---- */
.stTextInput > div > div > input {
    background: #0e0e13 !important; border: 1px solid #232330 !important; border-radius: 10px !important;
    color: #e5e5ec !important; font-size: 14px !important; padding: .75rem 1rem !important;
}
.stTextInput > div > div > input:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important; }
.stTextInput > div > div > input::placeholder { color: #55555f !important; }

.stButton > button {
    width: 100%; background: linear-gradient(135deg, #8b5cf6, #6366f1) !important; color: #fff !important;
    font-weight: 600 !important; font-size: 14.5px !important; border: none !important; border-radius: 11px !important;
    padding: .8rem 1.5rem !important; transition: all .15s !important; box-shadow: 0 4px 16px rgba(99,102,241,.25) !important;
}
.stButton > button:hover { opacity: .92 !important; box-shadow: 0 6px 20px rgba(99,102,241,.35) !important; transform: translateY(-1px); }
.stButton > button:active { transform: scale(.98) !important; }

button[kind="secondary"] {
    background: transparent !important; color: #9d9da8 !important; box-shadow: none !important;
    border: 1px solid #232330 !important;
}
button[kind="secondary"]:hover { border-color: #3a3a48 !important; color: #d4d4dc !important; transform: none; }

.stSpinner > div { border-top-color: #8b5cf6 !important; }
.stDownloadButton > button {
    background: transparent !important; color: #9d9da8 !important; border: 1px solid #232330 !important;
    box-shadow: none !important; font-weight: 500 !important;
}
.stDownloadButton > button:hover { border-color: #3a3a48 !important; color: #d4d4dc !important; }
</style>
""", unsafe_allow_html=True)


# ---- SESSION STATE ----
if "grade" not in st.session_state:
    st.session_state.grade = 4
if "result" not in st.session_state:
    st.session_state.result = None
if "submitted_topic" not in st.session_state:
    st.session_state.submitted_topic = ""


# ---- HELPERS ----
def render_mcqs(mcqs):
    letters = ["A", "B", "C", "D", "E", "F"]
    for i, mcq in enumerate(mcqs, 1):
        opts_html = ""
        for j, o in enumerate(mcq["options"]):
            is_correct = str(o).strip() == str(mcq["answer"]).strip()
            letter = letters[j] if j < len(letters) else str(j + 1)
            check = '<span class="mcq-check">✓</span>' if is_correct else ""
            cls = "mcq-opt correct" if is_correct else "mcq-opt"
            opts_html += f'<div class="{cls}"><div class="mcq-letter">{letter}</div><span>{o}</span>{check}</div>'
        st.markdown(f"""
        <div class="mcq-item">
            <div class="mcq-q">Q{i}. {mcq['question']}</div>
            {opts_html}
        </div>
        """, unsafe_allow_html=True)


def step_indicator(active: int):
    steps = ["Configure", "Generated", "Reviewed", "Refined"]
    html = '<div class="steps">'
    for i, label in enumerate(steps, 1):
        if i < active:
            cls, num = "step done", "✓"
        elif i == active:
            cls, num = "step active", str(i)
        else:
            cls, num = "step", str(i)
        html += f'<div class="{cls}"><div class="step-num">{num}</div>{label}</div>'
        if i < len(steps):
            line_cls = "step-line done" if i < active else "step-line"
            html += f'<div class="{line_cls}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ---- HEADER ----
st.markdown('<div class="eyebrow">✦ AI-powered education</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Learning agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Generate, review, and refine educational content in seconds</div>', unsafe_allow_html=True)

data = st.session_state.result
active_step = 1 if not data else (4 if data.get("refined_output") else 3)
step_indicator(active_step)


# ============================
# FORM
# ============================
if not data:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="field-label">Grade level</div>', unsafe_allow_html=True)
    try:
        grade = st.segmented_control(
            "Grade level",
            options=list(range(1, 11)),
            default=st.session_state.grade,
            label_visibility="collapsed",
            format_func=lambda g: f"Grade {g}",
        )
        st.session_state.grade = grade if grade else st.session_state.grade
    except Exception:
        st.session_state.grade = st.select_slider(
            "Grade level", options=list(range(1, 11)),
            value=st.session_state.grade, label_visibility="collapsed",
        )

    st.markdown('<div class="field-label" style="margin-top:1.4rem">Topic</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Topic", placeholder="e.g. Fractions, Photosynthesis, World War II",
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
    generate = st.button("Generate content", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if generate:
        if not topic.strip():
            st.warning("Please enter a topic first.")
            st.stop()

        with st.spinner("AI agents working…"):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={"grade": st.session_state.grade, "topic": topic.strip()},
                    timeout=60,
                )
            except Exception as e:
                st.error(f"Backend not reachable: {e}")
                st.stop()

            if response.status_code != 200:
                st.error(f"Backend error {response.status_code}")
                st.text(response.text)
                st.stop()

            try:
                st.session_state.result = response.json()
                st.session_state.submitted_topic = topic.strip()
            except Exception:
                st.error("Invalid response from backend.")
                st.text(response.text)
                st.stop()

        st.rerun()


# ============================
# OUTPUT
# ============================
if data:
    topic_label = st.session_state.submitted_topic
    grade_label = st.session_state.grade

    # ---- Generated content ----
    st.markdown('<div class="section-label"><div class="dot"></div>Generated content</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="topic-tag">📘 {topic_label} · Grade {grade_label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="explanation-card">{data["initial_output"]["explanation"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:-.5rem"><div class="dot"></div>Quiz</div>', unsafe_allow_html=True)
    render_mcqs(data["initial_output"]["mcqs"])

    # ---- AI Review ----
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><div class="dot"></div>AI review</div>', unsafe_allow_html=True)

    status = data["review"]["status"]
    if status == "pass":
        st.markdown('<div class="review-pass">✓ Content approved — meets educational standards</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="review-fail">⚠ Needs improvement — see feedback below</div>', unsafe_allow_html=True)

    feedback_html = ""
    for fb in data["review"].get("feedback", []):
        feedback_html += f'<div class="feedback-item"><div class="feedback-bullet"></div><span>{fb}</span></div>'
    if feedback_html:
        st.markdown(f'<div class="card">{feedback_html}</div>', unsafe_allow_html=True)

    # ---- Refined output ----
    if data.get("refined_output"):
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label"><div class="dot"></div>Improved content</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="refined-badge">✦ Refined by AI</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="explanation-card">{data["refined_output"]["explanation"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:-.5rem"><div class="dot"></div>Updated quiz</div>', unsafe_allow_html=True)
        render_mcqs(data["refined_output"]["mcqs"])

    # ---- Actions ----
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↺ Start over", type="secondary"):
            st.session_state.result = None
            st.session_state.submitted_topic = ""
            st.rerun()
    with col2:
        final = data.get("refined_output") or data["initial_output"]
        export_lines = [f"{topic_label} — Grade {grade_label}", "", final["explanation"], "", "Quiz:"]
        for i, mcq in enumerate(final["mcqs"], 1):
            export_lines.append(f"\nQ{i}. {mcq['question']}")
            for o in mcq["options"]:
                export_lines.append(f"  - {o}")
            export_lines.append(f"  Answer: {mcq['answer']}")
        st.download_button(
            "⬇ Download as text",
            data="\n".join(export_lines),
            file_name=f"{topic_label.replace(' ', '_').lower()}_grade{grade_label}.txt",
            mime="text/plain",
        )