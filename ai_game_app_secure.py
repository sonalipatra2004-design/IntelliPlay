import streamlit as st
import tensorflow as tf
import numpy as np
import random
from PIL import Image
import os



# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Game Zone",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Design System ─────────────────────────────────────────────────────────────
# Midnight Teal-Blue 2.5D Glassmorphism
# BG:      #0a1628 → #0d2137 → #0f2a42  (deep midnight teal, no harsh blue light)
# Glass:   rgba(13,180,185,0.07) with backdrop-blur
# Accent:  #0db4b9 (teal), #38bdf8 (sky), #6ee7b7 (mint)
# Text:    #e0f4f4 (soft warm white), #94c9cc (muted teal)
# Shadow:  0 8px 32px rgba(0,0,0,0.4), inset highlight rgba(255,255,255,0.05)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    box-sizing: border-box;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(160deg, #0a1628 0%, #0d2137 45%, #0a1f35 100%);
    min-height: 100vh;
}

/* ── Floating orbs for depth ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -120px; left: -120px;
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(13,180,185,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -100px; right: -100px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(56,189,248,0.10) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}

/* ── Header ── */
.game-header {
    text-align: center;
    padding: 2.2rem 0 0.5rem;
    position: relative;
    z-index: 1;
}
.game-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0db4b9, #38bdf8, #6ee7b7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    margin: 0;
    text-shadow: none;
    filter: drop-shadow(0 2px 12px rgba(13,180,185,0.35));
}
.game-subtitle {
    color: #6cb8be;
    font-size: 0.88rem;
    margin-top: 0.25rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1px;
}

/* ── Glass Card (2.5D core element) ── */
.glass-card {
    background: rgba(13, 180, 185, 0.06);
    border: 1px solid rgba(13, 180, 185, 0.18);
    border-radius: 20px;
    padding: 1.6rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.06),
        inset 0 -1px 0 rgba(0,0,0,0.15);
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(13,180,185,0.4), transparent);
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 14px 40px rgba(0,0,0,0.4),
        0 0 0 1px rgba(13,180,185,0.25),
        inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ── Mode Cards ── */
.mode-card {
    background: rgba(10, 28, 50, 0.55);
    border: 1px solid rgba(13, 180, 185, 0.15);
    border-radius: 18px;
    padding: 1.8rem 1rem;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow:
        0 6px 24px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.28s ease;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
}
.mode-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0db4b9, #38bdf8);
    transform: scaleX(0);
    transition: transform 0.3s ease;
    transform-origin: left;
}
.mode-card:hover::after { transform: scaleX(1); }
.mode-card:hover {
    background: rgba(13, 180, 185, 0.1);
    border-color: rgba(13, 180, 185, 0.35);
    transform: translateY(-4px);
    box-shadow:
        0 12px 36px rgba(0,0,0,0.4),
        0 0 20px rgba(13,180,185,0.1),
        inset 0 1px 0 rgba(255,255,255,0.08);
}
.mode-icon { font-size: 2.6rem; margin-bottom: 0.6rem; display: block; }
.mode-name { color: #e0f4f4; font-size: 1.1rem; font-weight: 800; margin: 0 0 0.3rem; }
.mode-desc { color: #6cb8be; font-size: 0.82rem; line-height: 1.5; margin: 0; }

/* ── Score Badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(13,180,185,0.12);
    border: 1px solid rgba(13,180,185,0.3);
    color: #6ee7b7;
    padding: 0.35rem 1rem;
    border-radius: 50px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    box-shadow: 0 2px 12px rgba(13,180,185,0.15);
}

/* ── Question Box ── */
.question-box {
    background: rgba(10, 25, 45, 0.6);
    border-left: 3px solid #0db4b9;
    border-radius: 0 14px 14px 0;
    padding: 1.2rem 1.4rem;
    color: #d4eef0;
    font-size: 1.05rem;
    line-height: 1.75;
    margin: 1rem 0;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 18px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.04);
}

/* ── Result Boxes ── */
.answer-box {
    background: rgba(110, 231, 183, 0.07);
    border: 1px solid rgba(110, 231, 183, 0.3);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    color: #6ee7b7;
    margin-top: 1rem;
    box-shadow: 0 4px 16px rgba(110,231,183,0.08);
    backdrop-filter: blur(8px);
}
.wrong-box {
    background: rgba(251, 113, 133, 0.07);
    border: 1px solid rgba(251, 113, 133, 0.3);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    color: #fda4af;
    margin-top: 1rem;
    box-shadow: 0 4px 16px rgba(251,113,133,0.08);
    backdrop-filter: blur(8px);
}
.hint-box {
    background: rgba(251, 191, 36, 0.06);
    border: 1px solid rgba(251, 191, 36, 0.25);
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    color: #fcd34d;
    font-size: 0.92rem;
    margin-top: 0.8rem;
    backdrop-filter: blur(8px);
}

/* ── Section Label ── */
.section-label {
    color: #0db4b9;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-bottom: 0.6rem;
    display: block;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, rgba(13,180,185,0.18), rgba(56,189,248,0.12)) !important;
    border: 1px solid rgba(13,180,185,0.35) !important;
    border-radius: 12px !important;
    color: #e0f4f4 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(8px) !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(13,180,185,0.32), rgba(56,189,248,0.22)) !important;
    border-color: rgba(13,180,185,0.6) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(13,180,185,0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    color: #6ee7b7 !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stSelectSlider > div {
    background: rgba(10,28,50,0.6) !important;
    border: 1px solid rgba(13,180,185,0.2) !important;
    border-radius: 12px !important;
    color: #d4eef0 !important;
    font-family: 'Nunito', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(13,180,185,0.55) !important;
    box-shadow: 0 0 0 3px rgba(13,180,185,0.1) !important;
}

/* ── Radio ── */
.stRadio > div { gap: 0.6rem; }
.stRadio label {
    background: rgba(10,28,50,0.5) !important;
    border: 1px solid rgba(13,180,185,0.15) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.8rem !important;
    color: #c8e8ea !important;
    transition: all 0.2s !important;
}
.stRadio label:hover {
    background: rgba(13,180,185,0.1) !important;
    border-color: rgba(13,180,185,0.35) !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    backkground: rgba(10,28,50,0.5) !important;
    border: 2px dashed rgba(13,180,185,0.25) !important;
    border-radius: 16px !important;
}
.stFileUploader > div:hover {
    border-color: rgba(13,180,185,0.5) !important;
    background: rgba(13,180,185,0.05) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(13,180,185,0.3), transparent) !important;
    margin: 1.2rem 0 !important;
}

/* ── Info / spinner ── */
.stAlert {
    background: rgba(13,180,185,0.07) !important;
    border: 1px solid rgba(13,180,185,0.2) !important;
    border-radius: 12px !important;
    color: #94c9cc !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a1628; }
::-webkit-scrollbar-thumb { background: rgba(13,180,185,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(13,180,185,0.5); }
</style>
""", unsafe_allow_html=True)


# ─── Claude API ────────────────────────────────────────────────────────────────
d


# ─── Session State ─────────────────────────────────────────────────────────────
defaults = {
    "mode": None, "score": 0, "round": 0,
    "riddle": None, "riddle_answer": None, "riddle_hint": None,
    "riddle_revealed": False, "riddle_correct": False,
    "img_question": None, "img_label": None, "img_options": None,
    "img_answered": False, "img_selected": None,
    "draw_guess": None, "draw_score": None, "draw_feedback": None,
    "draw_description": None, "draw_confidence": None, "what_drew": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="game-header">
  <div class="game-title">🎮 AI Game Zone</div>
  <div class="game-subtitle">// three modes · powered by claude AI //</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HOME SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.mode is None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6cb8be; font-size:0.95rem; margin-bottom:1.5rem;'>Select a game mode to begin your challenge</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class="mode-card">
          <span class="mode-icon">🖼️</span>
          <p class="mode-name">Image Quiz</p>
          <p class="mode-desc">Upload any image. AI builds a quiz — can you beat it?</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Play Now", key="b_img", use_container_width=True):
            st.session_state.update({"mode":"image","score":0,"round":0,"img_label":None,"img_options":None,"img_answered":False})
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card">
          <span class="mode-icon">🤖</span>
          <p class="mode-name">AI Riddles</p>
          <p class="mode-desc">Solve clever riddles generated by AI. Use hints wisely!</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Play Now", key="b_rid", use_container_width=True):
            st.session_state.update({"mode":"riddle","score":0,"round":0,"riddle":None,"riddle_revealed":False})
            st.rerun()

    with col3:
        st.markdown("""
        <div class="mode-card">
          <span class="mode-icon">✏️</span>
          <p class="mode-name">Draw & Guess</p>
          <p class="mode-desc">Upload your sketch. AI guesses it and scores your art!</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Play Now", key="b_draw", use_container_width=True):
            st.session_state.update({"mode":"draw","score":0,"round":0,"draw_guess":None})
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-top:1rem;">
      <div class="glass-card" style="display:inline-block; padding:0.8rem 2rem; border-radius:50px;">
        <span style="color:#6cb8be; font-size:0.8rem; font-family:'JetBrains Mono',monospace;">
          🌙 Eye-friendly · Midnight Teal-Blue · 2.5D Glass UI
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GAME SCREENS
# ══════════════════════════════════════════════════════════════════════════════
else:
    # ── Top bar ──
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("← Menu", key="back"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()
    with c2:
        mode_labels = {"image":"🖼️ Image Quiz","riddle":"🤖 AI Riddles","draw":"✏️ Draw & Guess"}
        st.markdown(f"""
        <div style="text-align:right; padding-top:0.3rem;">
          <span class="score-badge">⭐ {st.session_state.score} pts &nbsp;·&nbsp; R{st.session_state.round} &nbsp;·&nbsp; {mode_labels.get(st.session_state.mode,'')}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ════════════════════════════
    # MODE 1 — IMAGE QUIZ
    # ════════════════════════════
    if st.session_state.mode == "image":
        st.markdown("<span class='section-label'>🖼️ Image Recognition Quiz</span>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94c9cc; font-size:0.92rem;'>Upload any image — AI will build a multiple-choice question about it.</p>", unsafe_allow_html=True)

        uploaded = st.file_uploader("Drop your image here", type=["jpg","jpeg","png","webp"], key="img_up")

        if uploaded and not st.session_state.img_options:
            img = Image.open(uploaded)
            st.image(img, use_container_width=True)
            b64 = base64.b64encode(uploaded.getvalue()).decode()

            if st.button("🎯 Generate Quiz Question", use_container_width=True):
                with st.spinner("AI is studying the image..."):
                    raw = call_claude_vision(
                        """Analyze this image carefully. Create one multiple-choice quiz question.
                        Return ONLY valid JSON, no extra text:
                        {
                          "question": "A specific question about the main subject",
                          "correct": "The correct answer (3-5 words)",
                          "options": ["correct answer", "wrong1", "wrong2", "wrong3"]
                        }
                        Shuffle options. Make wrong answers plausible but clearly incorrect.""",
                        b64, uploaded.type
                    )
                    try:
                        d = parse_json(raw)
                        random.shuffle(d["options"])
                        st.session_state.img_question = d["question"]
                        st.session_state.img_label    = d["correct"]
                        st.session_state.img_options  = d["options"]
                        st.session_state.img_answered = False
                        st.session_state.img_selected = None
                        st.session_state.round += 1
                        st.rerun()
                    except:
                        st.error("⚠️ Couldn't parse AI response. Try again!")

        elif uploaded and st.session_state.img_options:
            st.image(Image.open(uploaded), use_container_width=True)

        if st.session_state.img_options and not st.session_state.img_answered:
            st.markdown(f"<div class='question-box'>❓ {st.session_state.img_question}</div>", unsafe_allow_html=True)
            choice = st.radio("Choose your answer:", st.session_state.img_options, key="img_radio")
            if st.button("✅ Submit Answer", use_container_width=True):
                st.session_state.img_answered = True
                st.session_state.img_selected = choice
                if choice == st.session_state.img_label:
                    st.session_state.score += 10
                st.rerun()

        if st.session_state.img_answered:
            if st.session_state.img_selected == st.session_state.img_label:
                st.markdown(f"<div class='answer-box'>🎉 <b>Correct! +10 points</b><br>Answer: {st.session_state.img_label}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='wrong-box'>❌ <b>Wrong!</b> You chose: {st.session_state.img_selected}<br>✅ Correct: {st.session_state.img_label}</div>", unsafe_allow_html=True)
            if st.button("🔄 New Image Quiz", use_container_width=True):
                st.session_state.update({"img_question":None,"img_label":None,"img_options":None,"img_answered":False,"img_selected":None})
                st.rerun()

    # ════════════════════════════
    # MODE 2 — AI RIDDLES
    # ════════════════════════════
    elif st.session_state.mode == "riddle":
        st.markdown("<span class='section-label'>🤖 AI Riddle Challenge</span>", unsafe_allow_html=True)

        if st.session_state.riddle is None:
            st.markdown("<p style='color:#94c9cc; font-size:0.92rem;'>Pick a category and difficulty. AI crafts a fresh riddle just for you!</p>", unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                cat = st.selectbox("Category", ["Science","Nature","Technology","History","Mathematics","Animals","Space","General Knowledge"])
            with col_b:
                diff = st.select_slider("Difficulty", ["Easy","Medium","Hard"])

            if st.button("🎲 Give Me a Riddle!", use_container_width=True):
                with st.spinner("AI is crafting your riddle..."):
                    raw = call_claude(
                        f"""Create one {diff.lower()} riddle about {cat}.
                        Return ONLY valid JSON, no extra text:
                        {{
                          "riddle": "The full riddle text",
                          "answer": "One short answer (1-3 words)",
                          "hint": "A subtle hint without revealing the answer"
                        }}""",
                        "You are a witty riddle master. Create clever, satisfying riddles."
                    )
                    try:
                        d = parse_json(raw)
                        st.session_state.riddle         = d["riddle"]
                        st.session_state.riddle_answer  = d["answer"].strip().lower()
                        st.session_state.riddle_hint    = d["hint"]
                        st.session_state.riddle_revealed = False
                        st.session_state.riddle_correct  = False
                        st.session_state.round += 1
                        st.rerun()
                    except:
                        st.error("⚠️ Couldn't generate riddle. Try again!")

        else:
            st.markdown(f"<div class='question-box'>🧩 {st.session_state.riddle}</div>", unsafe_allow_html=True)

            if not st.session_state.riddle_revealed:
                ans = st.text_input("Your answer:", placeholder="Type here...", key="rid_in")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Submit", use_container_width=True, key="rid_sub"):
                        correct = st.session_state.riddle_answer
                        user    = ans.strip().lower()
                        st.session_state.riddle_correct  = (user in correct) or (correct in user)
                        st.session_state.riddle_revealed = True
                        if st.session_state.riddle_correct:
                            st.session_state.score += 10
                        st.rerun()
                with c2:
                    if st.button("💡 Hint (-3 pts)", use_container_width=True, key="rid_hint"):
                        st.session_state.score = max(0, st.session_state.score - 3)
                        st.markdown(f"<div class='hint-box'>💡 {st.session_state.riddle_hint}</div>", unsafe_allow_html=True)

            else:
                if st.session_state.riddle_correct:
                    st.markdown(f"<div class='answer-box'>🎉 <b>Correct! +10 points</b><br>Answer: <b>{st.session_state.riddle_answer.title()}</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='wrong-box'>❌ <b>Not quite!</b><br>✅ Answer: <b>{st.session_state.riddle_answer.title()}</b></div>", unsafe_allow_html=True)
                if st.button("🔄 Next Riddle", use_container_width=True):
                    st.session_state.update({"riddle":None,"riddle_answer":None,"riddle_hint":None,"riddle_revealed":False,"riddle_correct":False})
                    st.rerun()

    # ════════════════════════════
    # MODE 3 — DRAW & GUESS
    # ════════════════════════════
    elif st.session_state.mode == "draw":
        st.markdown("<span class='section-label'>✏️ Draw & Guess</span>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94c9cc; font-size:0.92rem;'>Upload a sketch or drawing. AI will guess what it is and score your artwork!</p>", unsafe_allow_html=True)

        st.info("🎨 Draw on paper and photograph it, use MS Paint, or any drawing app — then upload here.")

        drawing = st.file_uploader("Upload your drawing", type=["jpg","jpeg","png","webp"], key="draw_up")

        if drawing and not st.session_state.draw_guess:
            st.image(Image.open(drawing), caption="Your Drawing", use_container_width=True)
            what = st.text_input("What did you draw? (AI won't see this)", placeholder="e.g. a cat, a bicycle, a mountain...", key="what_in")

            if st.button("🔍 Let AI Guess!", use_container_width=True):
                b64 = base64.b64encode(drawing.getvalue()).decode()
                with st.spinner("AI is studying your masterpiece..."):
                    raw = call_claude_vision(
                        """This is a hand-drawn sketch or drawing. Analyze it and respond ONLY in valid JSON:
                        {
                          "guess": "Your best guess of the subject (2-4 words)",
                          "confidence": "High / Medium / Low",
                          "description": "What you see in the drawing (1 sentence, fun tone)",
                          "score": 7,
                          "feedback": "Encouraging, fun feedback on the drawing style (1-2 sentences)"
                        }
                        Score 1-10: 10=very clear and well-drawn, 1=very hard to identify.""",
                        b64, drawing.type
                    )
                    try:
                        d = parse_json(raw)
                        st.session_state.draw_guess       = d["guess"]
                        st.session_state.draw_confidence  = d["confidence"]
                        st.session_state.draw_description = d["description"]
                        st.session_state.draw_score       = d["score"]
                        st.session_state.draw_feedback    = d["feedback"]
                        st.session_state.what_drew        = what
                        st.session_state.round += 1
                        # Award points if close match
                        g = d["guess"].lower(); w = what.strip().lower()
                        if w and (w in g or g in w or any(word in g for word in w.split())):
                            st.session_state.score += d["score"]
                        st.rerun()
                    except:
                        st.error("⚠️ Couldn't analyze drawing. Try again!")

        elif drawing and st.session_state.draw_guess:
            st.image(Image.open(drawing), caption="Your Drawing", use_container_width=True)

        if st.session_state.draw_guess:
            st.markdown("<hr>", unsafe_allow_html=True)

            col_l, col_r = st.columns(2, gap="medium")
            with col_l:
                st.markdown(f"""
                <div class="glass-card">
                  <div style="color:#0db4b9; font-size:0.75rem; font-family:'JetBrains Mono',monospace; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.8rem;">AI Verdict</div>
                  <div style="color:#e0f4f4; font-size:1.4rem; font-weight:800;">"{st.session_state.draw_guess}"</div>
                  <div style="color:#6cb8be; font-size:0.85rem; margin-top:0.4rem;">Confidence: <b style="color:#38bdf8">{st.session_state.draw_confidence}</b></div>
                  <div style="margin-top:0.8rem;">
                    <span style="color:#6cb8be; font-size:0.85rem;">Art Score: </span>
                    <span style="font-size:1.5rem; font-weight:800; color:#6ee7b7;">{st.session_state.draw_score}<span style="font-size:0.9rem; color:#6cb8be;">/10</span></span>
                  </div>
                </div>""", unsafe_allow_html=True)

            with col_r:
                st.markdown(f"""
                <div class="glass-card" style="height:100%;">
                  <div style="color:#fcd34d; font-size:0.75rem; font-family:'JetBrains Mono',monospace; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.8rem;">AI Feedback</div>
                  <div style="color:#d4eef0; font-size:0.92rem; line-height:1.6;">💬 {st.session_state.draw_feedback}</div>
                  <div style="color:#6cb8be; font-size:0.82rem; margin-top:0.8rem; font-style:italic;">👁️ {st.session_state.draw_description}</div>
                </div>""", unsafe_allow_html=True)

            # Match result
            if st.session_state.what_drew:
                g = st.session_state.draw_guess.lower()
                w = st.session_state.what_drew.strip().lower()
                matched = w and (w in g or g in w or any(word in g for word in w.split() if len(word) > 2))
                if matched:
                    st.markdown(f"<div class='answer-box'>🎉 <b>AI guessed it!</b> You drew <b>{st.session_state.what_drew}</b> — +{st.session_state.draw_score} points awarded!</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='wrong-box'>😄 AI guessed <b>'{st.session_state.draw_guess}'</b> but you drew <b>'{st.session_state.what_drew}'</b>. Keep practicing!</div>", unsafe_allow_html=True)

            if st.button("🔄 Draw Something Else", use_container_width=True):
                st.session_state.update({"draw_guess":None,"draw_score":None,"draw_feedback":None,"draw_description":None,"draw_confidence":None,"what_drew":""})
                st.rerun()

    # ── Footer ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0;">
      <span style="color:#2a5f65; font-size:0.78rem; font-family:'JetBrains Mono',monospace;">
        🎮 AI Game Zone · Built with Streamlit · Powered by Claude AI
      </span>
    </div>""", unsafe_allow_html=True)
