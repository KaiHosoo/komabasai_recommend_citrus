import streamlit as st
import altair as alt
from collections import defaultdict

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# 質問データ
# ----------------------------------------------------------
QUESTIONS = [
    {
        "id": "Q1",
        "q": "みかんを食べる時、甘さと酸味のどちらを重視しますか？",
        "options": {
            "とにかく甘いのが好き": {"せとか": 2, "甘平": 2},
            "甘さと酸味のバランスが大事": {"温州みかん": 2, "ブラッドオレンジ": 2, "不知火": 2},
            "酸味強めが好き": {"甘夏": 2},
        },
    },
    {
        "id": "Q2",
        "q": "みかんを食べるシーンといえば？",
        "options": {
            "のんびりおやつに！": {"温州みかん": 2, "不知火": 2},
            "勉強や仕事の合間のリフレッシュ！": {"甘夏": 2, "ブラッドオレンジ": 2},
            "食後のデザートに！": {"せとか": 2, "甘平": 2},
        },
    },
    {
        "id": "Q3",
        "q": "みかんを食べるときに大事なことは？",
        "options": {
            "皮がむきやすいこと": {"温州みかん": 2, "不知火": 2},
            "香りや風味が良いこと": {"甘夏": 2, "ブラッドオレンジ": 2},
            "種がないこと": {"せとか": 2, "甘平": 2},
        },
    },
    {
        "id": "Q4",
        "q": "みかんの見た目で惹かれるのは？",
        "options": {
            "小ぶりでかわいいサイズ感": {"温州みかん": 2},
            "ふっくら丸くて存在感のあるもの": {"不知火": 2, "甘夏": 2, "ブラッドオレンジ": 2},
            "濃い色で『美味しそう！』と思えるもの": {"せとか": 2, "甘平": 2},
        },
    },
    {
        "id": "Q5",
        "q": "柑橘の食べ方は？",
        "options": {
            "そのままが一番！": {"温州みかん": 2, "甘平": 2},
            "柑橘スイーツ大好き！": {"不知火": 2, "せとか": 2},
            "料理に入れてみたい！": {"甘夏": 2, "ブラッドオレンジ": 2},
        },
    },
    {
        "id": "Q6",
        "q": "あなたが求める人生は？",
        "options": {
            "刺激のある人生": {"せとか": 1, "甘平": 1, "ブラッドオレンジ": 1},
            "安定な人生": {"温州みかん": 1, "不知火": 1, "甘夏": 1},
        },
    },
    {
        "id": "Q7",
        "q": "好きな季節は？",
        "options": {
            "春": {"甘平": 1, "ブラッドオレンジ": 1},
            "夏": {"甘夏": 1},
            "秋": {"温州みかん": 1},
            "冬": {"不知火": 1, "せとか": 1},
        },
    },
    {
        "id": "Q8",
        "q": "誕生日にもらって嬉しいのは？",
        "options": {
            "高級なもの": {"せとか": 1, "甘平": 1},
            "ユニークなもの": {"甘夏": 1, "ブラッドオレンジ": 1},
            "実用的なもの": {"温州みかん": 1, "不知火": 1},
        },
    },
    {
        "id": "Q9",
        "q": "好きなタイプは？",
        "options": {
            "あまあま": {"温州みかん": 1, "せとか": 1, "甘平": 1},
            "ツンデレ": {"不知火": 1, "甘夏": 1, "ブラッドオレンジ": 1},
        },
    },
    {
        "id": "Q10",
        "q": "好きな空は？",
        "options": {
            "青空": {"不知火": 1, "甘夏": 1},
            "夕焼け": {"温州みかん": 1, "せとか": 1},
            "星空": {"甘平": 1, "ブラッドオレンジ": 1},
        },
    },
    {
        "id": "Q11",
        "q": "新しい友達グループに入るとき、あなたはどうする？",
        "options": {
            "まずは様子を見て、少しずつ輪に入る": {"不知火": 1, "甘夏": 1},
            "自分から話しかけて、場を盛り上げる": {"温州みかん": 1, "せとか": 1},
            "特定の1人とじっくり仲良くなる": {"甘平": 1, "ブラッドオレンジ": 1},
        },
    },
    {
        "id": "Q12",
        "q": "目の前にお菓子がたくさんあります。持って帰るなら？",
        "options": {
            "大きなお菓子を1個": {"甘夏": 1, "不知火": 1},
            "中くらいのお菓子を3個": {"せとか": 1, "甘平": 1, "ブラッドオレンジ": 1},
            "小さなお菓子を5個": {"温州みかん": 1},
        },
    },
]

VARIETIES = ["温州みかん", "不知火", "せとか", "甘平", "甘夏", "ブラッドオレンジ"]

# 結果PDF
VARIETY_IMG = {
    "温州みかん": "citrus_images/推しみかん診断_page_温州みかん.pdf",
    "不知火":     "citrus_images/推しみかん診断_page_不知火.pdf",
    "せとか":     "citrus_images/推しみかん診断_page_せとか.pdf",
    "甘平":       "citrus_images/推しみかん診断_page_甘平.pdf",
    "甘夏":       "citrus_images/推しみかん診断_page_甘夏.pdf",
    "ブラッドオレンジ": "citrus_images/推しみかん診断_page_ブラッドオレンジ.pdf",
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
    hi = defaultdict(int)
    lo = defaultdict(int)

    for qid, opt in answers_dict.items():
        q = next(q for q in QUESTIONS if q["id"] == qid)
        mapping = q["options"][opt]
        for variety, pt in mapping.items():
            scores[variety] += pt
            if pt >= 2:
                hi[variety] += pt
            else:
                lo[variety] += pt

    if scores:
        max_total = max(scores.values())
        candidates = [v for v, s in scores.items() if s == max_total]

        # tie-break 1: high-point
        if len(candidates) > 1:
            max_hi = max(hi[v] for v in candidates)
            candidates = [v for v in candidates if hi[v] == max_hi]

        # tie-break 2: low-point
        if len(candidates) > 1:
            max_lo = max(lo[v] for v in candidates)
            candidates = [v for v in candidates if lo[v] == max_lo]

        # tie-break 3: defined order
        if len(candidates) > 1:
            for v in VARIETIES:
                if v in candidates:
                    winner = v
                    break
        else:
            winner = candidates[0]
    else:
        winner = None

    return dict(scores), winner, dict(hi), dict(lo)

# ----------------------------------------------------------
# プログレスバー
# ----------------------------------------------------------
def render_progress():
    total = len(QUESTIONS)
    step = st.session_state.step
    st.progress(step / total, text=f"進捗: {step}/{total} 問回答済み")

# ----------------------------------------------------------
# UI開始
# ----------------------------------------------------------
init_state()

st.title("🍊 推しみかん診断")

# ---------------- トップページ ----------------
if not st.session_state.started:
    st.write("あなたにぴったりの柑橘を診断します！")
    if st.button("診断を開始する", use_container_width=True):
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
            if st.button("← 戻る", use_container_width=True, disabled=(idx == 0)):
                if idx > 0:
                    st.session_state.step -= 1
                st.rerun()
        with cols[1]:
            if st.button("次へ →", use_container_width=True, disabled=(choice is None)):
                st.session_state.answers[q["id"]] = choice
                if idx + 1 < total:
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True
                st.rerun()

# ---------------- 結果画面 ----------------
else:
    scores, winner, hi, lo = compute_scores(st.session_state.answers)

    st.success("診断が完了しました！ あなたの推しみかんは・・・")

    if winner:
        st.header(f"🎉 {winner}")
        img_path = VARIETY_IMG.get(winner)
        if img_path:
            st.pdf(img_path)
    else:
        st.warning("スコアがありません。最初からやり直してください。")

    # スコア可視化
    st.subheader("スコア内訳")
    chart_data = [{"品種": v, "合計": scores.get(v, 0)} for v in VARIETIES]
    chart = (
        alt.Chart(alt.Data(values=chart_data))
        .mark_bar()
        .encode(x=alt.X("品種:N", sort=VARIETIES),
                y=alt.Y("合計:Q"))
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)

    # 回答確認
    with st.expander("あなたの回答", expanded=False):
        for q in QUESTIONS:
            ans = st.session_state.answers.get(q["id"], "-")
            st.write(f"{q['id']}: {q['q']}\n- あなたの選択: {ans}")

    st.divider()
    cols = st.columns([1,1])
    with cols[0]:
        if st.button("もう一度診断する", use_container_width=True):
            reset_all()
            st.rerun()
    with cols[1]:
        if st.button("最初に戻る", use_container_width=True):
            st.session_state.finished = False
            st.session_state.step = 0
            st.rerun()