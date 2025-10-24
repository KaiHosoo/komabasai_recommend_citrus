import streamlit as st
from collections import defaultdict
import random

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# CSS（レスポンシブ美デザイン＋中央寄せ＋スマホ最適化）
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

    /* 選択肢 */
    .stRadio > div > label {
        background-color: #fff !important;
        padding: 14px 12px !important;
        border-radius: 10px;
        border: 1px solid #EBEBEB;
        margin-bottom: 10px;
        text-align: center !important;
        font-size: 1.05rem;
        width: 100% !important;
    }

    .stRadio > div > label:hover {
        background-color: #FFF4E2 !important;
        border-color: #FFA726 !important;
    }

    .stButton>button {
        width: 100% !important;
        background-color: #ffffff !important;
        border: 1px solid #CCC !important;
        color: #333 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1.05rem !important;
        margin-top: 4px !important;
    }

    /* プログレスバー */
    div[data-testid="stProgressBar"] > div > div {
        height: 14px !important;
        border-radius: 8px !important;
    }

    /* 余計な白バー除去 */
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
        line-height: 1.5 !important;
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

# 結果画像
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
# スコア処理（同点ランダム）
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

# ----------------------------------------
# トップページ
# ----------------------------------------
if not st.session_state.started:
    st.write("あなたにぴったりの柑橘を診断します😆")
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

    # ✅ダミー選択肢を先頭に追加
    options = ["▼ 選択してください"] + list(q["options"].keys())

    # ✅前の回答があれば反映
    prev = st.session_state.answers.get(q["id"], None)
    index = options.index(prev) if prev in options else 0

    choice = st.radio("", options=options, index=index)

    # 前ページへ
    if idx > 0:
        if st.button("← 戻る"):
            st.session_state.step -= 1

    # 次へ
    label = "診断結果を見る" if idx == len(QUESTIONS) - 1 else "次へ →"

    # ✅本物の選択肢が選ばれたときだけ進行
    if st.button(label, disabled=(choice == "▼ 選択してください")):
        if choice != "▼ 選択してください":
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
    st.success("診断完了✨あなたにぴったりの柑橘は…")
    st.header(winner)
    st.image(VARIETY_IMG[winner], use_container_width=True)

    if st.button("もう一度診断する"):
        reset_all()