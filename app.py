import streamlit as st
from collections import defaultdict
import random

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# CSS（レスポンシブ美デザイン＋中央揃え＋スマホ最適化）
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

    /* 全体コンテナ（中央寄せ＆スマホ最適化） */
    .stApp {
        padding: 16px 12px !important;
        background-color: #FFF9ED;
        max-width: 520px;
        margin-left: auto;
        margin-right: auto;
    }

    /* 選択肢（カード風） */
    .stRadio > div > label {
        background-color: #ffffff !important;
        padding: 13px 10px !important;
        border-radius: 10px;
        border: 1px solid #EBEBEB;
        margin-bottom: 10px;
        text-align: center !important;
        font-size: 1rem;
        width: 100% !important;
    }

    .stRadio > div > label:hover {
        background-color: #FFF4E2 !important;
        border-color: #FFA726 !important;
    }

    /* ボタン（上下広がり改善） */
        .stButton>button {
        width: 100% !important;
        background-color: #ffffff !important;
        border: 2px solid #FFA726 !important;
        color: #333 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1.05rem !important;
        margin-top: 5px !important;
        margin-bottom: 6px !important;
        cursor: pointer !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15) !important;
        transition: 0.12s ease-in-out !important;
    }

    /* ホバー時：ふわっと明るく */
    .stButton>button:hover {
        background-color: #FFF3D6 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 10px rgba(0,0,0,0.20) !important;
        border-color: #FF8A00 !important;
    }

    /* 押したとき：沈む感じ */
    .stButton>button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 3px rgba(0,0,0,0.12) !important;
        background-color: #FFE9C4 !important;
        border-color: #F57C00 !important;
    }

    /* プログレスバー太く */
    div[data-testid="stProgressBar"] > div > div {
        height: 14px !important;
        border-radius: 8px !important;
    }

    /* 謎の白バー除去 */
    div[data-testid="stProgressBar"] > div:first-child {
        display: none !important;
    }

    /* テキスト整形 */
    span[data-testid="stProgressText"] {
        text-align: center !important;
        display: block !important;
        font-size: 0.92rem;
        margin-bottom: 3px !important;
        color: #444 !important;
    }

    /* 質問文 */
    .question-header {
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-top: 6px !important;
        margin-bottom: 12px !important;
        color: #333 !important;
        line-height: 1.4 !important;
    }

    /* 背景が緑になる success を透明に */
    div[data-testid="stNotification"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
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
    {"id": "Q1", "q": "みかんを食べる時、甘さと酸味のどちらを重視しますか？",
     "options": {"とにかく甘いのが好き": {"せとか": 2, "甘平": 2},
                 "甘さと酸味のバランスが大事": {"温州みかん": 2, "ブラッドオレンジ": 2, "不知火": 2},
                 "酸味強めが好き": {"甘夏": 2}}},
    {"id": "Q2", "q": "みかんを食べるシーンといえば？",
     "options": {"のんびりおやつに！": {"温州みかん": 2, "不知火": 2},
                 "勉強や仕事の合間のリフレッシュ！": {"甘夏": 2, "ブラッドオレンジ": 2},
                 "食後のデザートに！": {"せとか": 2, "甘平": 2}}},
    {"id": "Q3", "q": "みかんを食べるときに大事なことは？",
     "options": {"皮がむきやすいこと": {"温州みかん": 2, "不知火": 2},
                 "香りや風味が良いこと": {"甘夏": 2, "ブラッドオレンジ": 2},
                 "種がないこと": {"せとか": 2, "甘平": 2}}},
    {"id": "Q4", "q": "みかんの見た目で惹かれるのは？",
     "options": {"小ぶりでかわいいサイズ感": {"温州みかん": 2},
                 "ふっくら丸くて存在感のあるもの": {"不知火": 2, "甘夏": 2, "ブラッドオレンジ": 2},
                 "濃い色で『美味しそう！』と思えるもの": {"せとか": 2, "甘平": 2}}},
    {"id": "Q5", "q": "柑橘の食べ方は？",
     "options": {"そのままが一番！": {"温州みかん": 2, "甘平": 2},
                 "柑橘スイーツ大好き！": {"不知火": 2, "せとか": 2},
                 "料理に入れてみたい！": {"甘夏": 2, "ブラッドオレンジ": 2}}},
    {"id": "Q6", "q": "あなたが求める人生は？",
     "options": {"刺激のある人生": {"せとか": 1, "甘平": 1, "ブラッドオレンジ": 1},
                 "安定な人生": {"温州みかん": 1, "不知火": 1, "甘夏": 1}}},
    {"id": "Q7", "q": "好きな季節は？",
     "options": {"春": {"甘平": 1, "ブラッドオレンジ": 1},
                 "夏": {"甘夏": 1},
                 "秋": {"温州みかん": 1},
                 "冬": {"不知火": 1, "せとか": 1}}},
    {"id": "Q8", "q": "誕生日にもらって嬉しいのは？",
     "options": {"高級なもの": {"せとか": 1, "甘平": 1},
                 "ユニークなもの": {"甘夏": 1, "ブラッドオレンジ": 1},
                 "実用的なもの": {"温州みかん": 1, "不知火": 1}}},
    {"id": "Q9", "q": "好きなタイプは？",
     "options": {"あまあま": {"温州みかん": 1, "せとか": 1, "甘平": 1},
                 "ツンデレ": {"不知火": 1, "甘夏": 1, "ブラッドオレンジ": 1}}},
    {"id": "Q10", "q": "好きな空は？",
     "options": {"青空": {"不知火": 1, "甘夏": 1},
                 "夕焼け": {"温州みかん": 1, "せとか": 1},
                 "星空": {"甘平": 1, "ブラッドオレンジ": 1}}},
    {"id": "Q11", "q": "新しい友達グループに入るとき、あなたはどうする？",
     "options": {"まずは様子を見て、少しずつ輪に入る": {"不知火": 1, "甘夏": 1},
                 "自分から話しかけて、場を盛り上げる": {"温州みかん": 1, "せとか": 1},
                 "特定の1人とじっくり仲良くなる": {"甘平": 1, "ブラッドオレンジ": 1}}},
    {"id": "Q12", "q": "目の前にお菓子がたくさんあります。持って帰るなら？",
     "options": {"大きなお菓子を1個": {"甘夏": 1, "不知火": 1},
                 "中くらいのお菓子を3個": {"せとか": 1, "甘平": 1, "ブラッドオレンジ": 1},
                 "小さなお菓子を5個": {"温州みかん": 1}}}
]

# 結果カード画像
VARIETY_IMG = {
    "温州みかん": "citrus_images/推しみかん診断_page_温州みかん.png",
    "不知火": "citrus_images/推しみかん診断_page_不知火.png",
    "せとか": "citrus_images/推しみかん診断_page_せとか.png",
    "甘平": "citrus_images/推しみかん診断_page_甘平.png",
    "甘夏": "citrus_images/推しみかん診断_page_甘夏.png",
    "ブラッドオレンジ": "citrus_images/推しみかん診断_page_ブラッドオレンジ.png",
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
# スコア処理（同点はランダム）
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
st.title("推しみかん診断")

# ----------------------------------------
# トップページ
# ----------------------------------------
if not st.session_state.started:
    st.write(
        "あなたにぴったりの柑橘を診断します！\n\n"
        "12個の質問に答えて、あなただけの『推しみかん』を見つけましょう🍊"
    )

    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("診断を開始する"):
            st.session_state.started = True
    st.stop()

# ----------------------------------------
# 質問ページ
# ----------------------------------------
if not st.session_state.finished:
    render_progress()
    idx = st.session_state.step
    q = QUESTIONS[idx]

    st.markdown(f'<div class="question-header">{q["q"]}</div>', unsafe_allow_html=True)

    opts = list(q["options"].keys())
    prev = st.session_state.answers.get(q["id"], None)
    choice = st.radio("", options=opts, index=None, key=f"q{idx}")

    col1, col2 = st.columns(2)

    with col1:
        if idx > 0:
            if st.button("← 戻る"):
                st.session_state.step -= 1

    label = "診断結果を見る" if idx == len(QUESTIONS) - 1 else "次へ →"
    with col2:
        if st.button(label, disabled=(choice is None)):
            if choice is not None:
                st.session_state.answers[q["id"]] = choice
                if idx + 1 < len(QUESTIONS):
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True

# ----------------------------------------
# 結果ページ
# ----------------------------------------
else:
    winner = compute_scores(st.session_state.answers)

    st.markdown("### 診断完了！\nあなたにぴったりの柑橘は…")
    st.header(winner)
    st.image(VARIETY_IMG[winner], use_container_width=True)

    with st.expander("あなたの回答一覧を見る 👀"):
        for q in QUESTIONS:
            ans = st.session_state.answers.get(q["id"], "-")
            st.write(f"**{q['id']}｜{q['q']}**")
            st.write(f"👉 あなたの選択：{ans}")
            st.divider()

    if st.button("もう一度診断する"):
        reset_all()