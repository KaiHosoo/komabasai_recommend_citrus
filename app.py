import streamlit as st
from collections import defaultdict
import random

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# 柑橘テーマCSS（背景淡オレンジ、UI整形）
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #FFF5E6;
        margin-top: 20px;
        margin-bottom: 20px;
        margin-left: 40px;
        margin-right: 40px;
    }
    .stApp {
        background-color: #FFF5E6;
    }

    /* ▶ ボタン白化 */
    .stButton>button {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        border: 1px solid #CCC !important;
        box-shadow: none !important;
    }

    /* ▶ 選択肢白化 */
    .stRadio > div > label {
        background-color: white !important;
        padding: 6px 10px;
        border-radius: 6px;
        border: 1px solid #DDD;
    }

    /* ▶ 進捗テキスト装飾 */
    span[data-testid="stProgressText"] {
        color: #333 !important;
        font-weight: 600 !important;
    }

    /* ▶ 余計な白い背景トラックバーを完全除去（今回の主目的！） */
    div[data-testid="stProgressBar"] > div:first-child {
        display: none !important;
    }

    /* ▶ 青バー本体の見栄え調整 */
    div[data-testid="stProgressBar"] > div > div {
        border-radius: 8px !important;
    }

    /* ▶ 進捗ラップの背景を透明化 */
    .progress-wrap {
        background-color: transparent !important;
        padding: 4px 0px;
        margin-bottom: 8px;
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
# 同点ランダム含むスコア計算
# ----------------------------------------------------------
def compute_scores(answers_dict):
    scores = defaultdict(int)

    for qid, opt in answers_dict.items():
        q = next(q for q in QUESTIONS if q["id"] == qid)
        mapping = q["options"][opt]
        for variety, pt in mapping.items():
            scores[variety] += pt

    if scores:
        max_total = max(scores.values())
        candidates = [v for v, s in scores.items() if s == max_total]
        winner = random.choice(candidates)
    else:
        winner = None

    return winner

# ----------------------------------------------------------
# プログレスバー表示
# ----------------------------------------------------------
def render_progress():
    total = len(QUESTIONS)
    step = st.session_state.step
    st.markdown('<div class="progress-wrap">', unsafe_allow_html=True)
    st.progress(step / total, text=f"進捗: {step}/{total} 問回答済み")
    st.markdown('</div>', unsafe_allow_html=True)

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

    if idx < total:
        q = QUESTIONS[idx]
        st.subheader(f"{q['id']}  {q['q']}")
        opts = list(q["options"].keys())

        prev = st.session_state.answers.get(q["id"], None)
        choice = st.radio("選択肢を選んでください",
                          options=opts,
                          index=opts.index(prev) if prev in opts else None)

        cols = st.columns(2)
        with cols[0]:
            if st.button("← 戻る", disabled=(idx == 0)):
                if idx > 0:
                    st.session_state.step -= 1
                st.rerun()
        with cols[1]:
            label = "診断結果を見る" if idx + 1 == total else "次へ →"
            if st.button(label, disabled=(choice is None)):
                st.session_state.answers[q["id"]] = choice
                if idx + 1 < total:
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True
                st.rerun()

# ---------------- 結果画面 ----------------
else:
    winner = compute_scores(st.session_state.answers)

    st.success("診断が完了しました！ あなたの推しみかんは・・・")

    if winner:
        st.header(f" {winner}")
        st.image(VARIETY_IMG[winner])
    else:
        st.warning("最初からやり直してください。")

    st.divider()
    cols = st.columns([1,1])
    with cols[1]:
        if st.button("もう一度診断する"):
            reset_all()
            st.rerun()