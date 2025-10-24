import streamlit as st
from collections import defaultdict
import random

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# CSS（スマホ対応強化）
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #FFF5E6;
        margin: 0;
        padding: 0;
    }

    /* 全体のコンテナ余白をスマホ寄りに */
    .stApp {
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-top: 20px !important;
        background-color: #FFF5E6;
    }

    /* タイトルをスマホサイズに調整 */
    .st-emotion-cache-1wivap2 {
        font-size: 1.8rem !important;
    }

    /* ボタン大きめタッチ領域 */
    .stButton>button {
        background-color: white !important;
        color: black !important;
        border-radius: 10px !important;
        border: 1px solid #CCC !important;
        padding: 12px 0 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
    }

    /* ラジオボタン：タッチ領域拡大 */
    .stRadio > div > label {
        background-color: white !important;
        padding: 12px 12px !important;
        border-radius: 8px;
        border: 1px solid #DDD;
        margin-bottom: 6px;
        font-size: 1.05rem !important;
        display: block !important;
    }

    /* プログレスバー太く */
    div[data-testid="stProgressBar"] > div > div {
        height: 14px !important;
        border-radius: 8px !important;
    }

    /* 余計なバー消去 */
    div[data-testid="stProgressBar"] > div:first-child {
        display: none !important;
    }

    /* 進捗テキスト */
    span[data-testid="stProgressText"] {
        font-size: 0.9rem !important;
        color: #444 !important;
    }

    /* 質問文字サイズ */
    h2, .stSubheader {
        font-size: 1.2rem !important;
        line-height: 1.3 !important;
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

# 表示画像
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
# スコア計算
# ----------------------------------------------------------
def compute_scores(answers_dict):
    scores = defaultdict(int)

    for qid, opt in answers_dict.items():
        q = next(q for q in QUESTIONS if q["id"] == qid)
        mapping = q["options"][opt]
        for variety, pt in mapping.items():
            scores[variety] += pt

    max_total = max(scores.values())
    candidates = [v for v, s in scores.items() if s == max_total]
    return random.choice(candidates)

# ----------------------------------------------------------
# プログレスバー
# ----------------------------------------------------------
def render_progress():
    total = len(QUESTIONS)
    step = st.session_state.step
    st.progress(step / total, text=f"進捗: {step}/{total}")

# ----------------------------------------------------------
# UI開始
# ----------------------------------------------------------
init_state()
st.title("🍊 推しみかん診断")

# ---------------- トップページ ----------------
if not st.session_state.started:
    st.write("あなたにぴったりの柑橘を診断します！")
    if st.button("診断を開始する"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# ---------------- 質問画面 ----------------
if not st.session_state.finished:
    render_progress()
    idx = st.session_state.step
    total = len(QUESTIONS)

    q = QUESTIONS[idx]
    st.subheader(f"{q['id']}  {q['q']}")

    opts = list(q["options"].keys())
    prev = st.session_state.answers.get(q["id"], None)
    choice = st.radio("",
                      options=opts,
                      index=opts.index(prev) if prev in opts else None)

    # ナビゲーション
    if idx > 0:
        st.button("← 戻る",
                  on_click=lambda: (setattr(st.session_state, "step", idx - 1), st.rerun()),
                  use_container_width=True)

    label = "診断結果を見る" if idx + 1 == total else "次へ →"
    st.button(label,
              disabled=(choice is None),
              on_click=lambda: (
                  st.session_state.answers.update({q["id"]: choice}),
                  setattr(st.session_state, "step", idx + 1)
                  if idx + 1 < total
                  else setattr(st.session_state, "finished", True),
                  st.rerun()
              ),
              use_container_width=True)

# ---------------- 結果画面 ----------------
else:
    winner = compute_scores(st.session_state.answers)
    st.success("診断完了！あなたの推しみかんは…")
    st.header(winner)
    st.image(VARIETY_IMG[winner], use_container_width=True)

    st.divider()
    if st.button("もう一度診断する", use_container_width=True):
        reset_all()
        st.rerun()