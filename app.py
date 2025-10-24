import streamlit as st
from collections import defaultdict
import random

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# CSS（レスポンシブ美デザイン）
# ----------------------------------------------------------
st.markdown(
    """
    <style>

    body {
        background-color: #FFF9ED;
        margin: 0;
        padding: 0;
        font-family: "Helvetica Neue", sans-serif;
    }

    .stApp {
        padding: 20px 12px !important;
        background-color: #FFF9ED;
    }

    h1 {
        text-align: center !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
        font-weight: 800 !important;
    }

    .choice-card {
        background-color: #ffffff !important;
        padding: 16px 12px !important;
        border-radius: 10px !important;
        border: 1px solid #EBEBEB !important;
        margin-bottom: 10px !important;
        text-align: center !important;
        font-size: 1.05rem !important;
    }

    .choice-card:hover {
        border-color: #FFA726 !important;
        background-color: #FFF4E2 !important;
    }

    .stRadio > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    .stRadio > div > label {
        width: 92% !important;
    }

    .stButton > button {
        width: 100% !important;
        background-color: #ffffff !important;
        border: 1px solid #CCC !important;
        color: #333 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1.1rem !important;
        margin-top: 4px !important;
    }

    .stButton > button:hover {
        background-color: #FFF3D6 !important;
        border-color: #FFA726 !important;
    }

    div[data-testid="stProgressBar"] > div > div {
        height: 14px !important;
        border-radius: 8px !important;
    }

    div[data-testid="stProgressBar"] > div:first-child {
        display: none !important;
    }

    span[data-testid="stProgressText"] {
        text-align: center !important;
        display: block !important;
        font-size: 0.92rem;
        margin-bottom: 4px !important;
        color: #444 !important;
    }

    .question-header {
        text-align: center !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
        margin-bottom: 16px !important;
        color: #333 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------
# 質問データ
# ----------------------------------------------------------
QUESTIONS = [
    ...
]  # ← 中略（前と同じ質問リスト）※省略せず貼りたい場合は言って！

# PNG画像
VARIETY_IMG = {
    ...
}

# ----------------------------------------------------------
# セッション管理
# ----------------------------------------------------------
def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "started" not in st.session_state:
        st.session_state.started = False

def reset_all():
    st.session_state.clear()
    init_state()

# ----------------------------------------------------------
# スコア処理
# ----------------------------------------------------------
def compute_scores(answers_dict):
    scores = defaultdict(int)
    for qid, opt in answers_dict.items():
        mapping = next(q for q in QUESTIONS if q["id"] == qid)["options"][opt]
        for variety, pt in mapping.items():
            scores[variety] += pt
    maxv = max(scores.values())
    return random.choice([v for v, s in scores.items() if s == maxv])

# ----------------------------------------------------------
# プログレスバー
# ----------------------------------------------------------
def render_progress():
    step = st.session_state.step
    total = len(QUESTIONS)
    st.progress(step / total, text=f"進捗: {step}/{total}")

# ----------------------------------------------------------
# UI開始
# ----------------------------------------------------------
init_state()
st.title("🍊 推しみかん診断")

# トップ
if not st.session_state.started:
    st.write("あなたにぴったりの柑橘を診断します😆")
    if st.button("診断を開始する"):
        st.session_state.started = True
    st.stop()

# 質問フェーズ
if not st.session_state.finished:
    render_progress()
    idx = st.session_state.step
    q = QUESTIONS[idx]

    st.markdown(f'<div class="question-header">{q["q"]}</div>', unsafe_allow_html=True)

    opts = list(q["options"].keys())
    choice = st.radio("", options=opts)

    # 戻るボタン
    if idx > 0:
        if st.button("← 戻る"):
            st.session_state.step -= 1

    # 次へ or 結果
    label = "診断結果を見る" if idx == len(QUESTIONS) - 1 else "次へ →"
    if st.button(label, disabled=(choice is None)):
        st.session_state.answers[q["id"]] = choice
        if idx + 1 < len(QUESTIONS):
            st.session_state.step += 1
        else:
            st.session_state.finished = True

# 結果
else:
    winner = compute_scores(st.session_state.answers)
    st.success("診断完了✨あなたにぴったりの柑橘は…")
    st.header(winner)
    st.image(VARIETY_IMG[winner], use_container_width=True)

    if st.button("もう一度診断する"):
        reset_all()