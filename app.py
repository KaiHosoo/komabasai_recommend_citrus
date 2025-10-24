import streamlit as st
import altair as alt
from collections import defaultdict

# ----------------------------------------------------------
# ページ設定
# ----------------------------------------------------------
st.set_page_config(page_title="推しみかん診断", page_icon="🍊", layout="centered")

# ----------------------------------------------------------
# 質問データ（ユーザー提供の配点設計をそのまま実装）
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

# 結果表示用の解説と（任意）画像URLをここで定義
VARIETY_INFO = {
    "温州みかん": {
        "caption": "手軽に食べられる定番。なんだかんだ一番愛されてる。",
        "season": "11月〜1月",
        "note": "バランス派・実用派・そのまま派と相性◎",
        "image_url": None,  # 画像を使う場合はURLを入れる
    },
    "不知火": {
        "caption": "ぽこんとした見た目が特徴。ジューシーで食べ応え◎",
        "season": "3月〜4月",
        "note": "安定志向だけどちょい攻めたい人に。",
        "image_url": None,
    },
    "せとか": {
        "caption": "『柑橘の女王』とろける食感とリッチな甘さ。",
        "season": "2月〜3月",
        "note": "甘党・高級志向・映え好きに刺さる。",
        "image_url": None,
    },
    "甘平": {
        "caption": "薄皮×強い甘み。シャリっと心地よい果肉。",
        "season": "2月〜3月",
        "note": "甘さ重視＆そのまま派に。",
        "image_url": None,
    },
    "甘夏": {
        "caption": "爽やかな香りと酸味。夏にキンッと冷やすと最高。",
        "season": "4月〜6月",
        "note": "酸味・香り・料理活用が好きな人へ。",
        "image_url": None,
    },
    "ブラッドオレンジ": {
        "caption": "赤い果肉とワインのような香り。見た目も華やか。",
        "season": "3月〜5月",
        "note": "個性派・香り重視・デザート映えを求める人に。",
        "image_url": None,
    },
}

# ----------------------------------------------------------
# ユーティリティ
# ----------------------------------------------------------

def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "finished" not in st.session_state:
        st.session_state.finished = False


def reset_all():
    st.session_state.clear()
    init_state()


def compute_scores(answers_dict):
    scores = defaultdict(int)
    # 高配点(2点)と低配点(1点)の内訳も保持しておく（タイブレークに使用）
    hi = defaultdict(int)
    lo = defaultdict(int)
    for qid, opt in answers_dict.items():
        # 該当質問の選択肢→品種配点を取得
        q = next(q for q in QUESTIONS if q["id"] == qid)
        mapping = q["options"][opt]
        for variety, pt in mapping.items():
            scores[variety] += pt
            if pt >= 2:
                hi[variety] += pt
            else:
                lo[variety] += pt
    # タイブレーク：総点 → 高配点合計 → 低配点合計 → 事前順序
    if scores:
        max_total = max(scores.values())
        candidates = [v for v, s in scores.items() if s == max_total]
        if len(candidates) > 1:
            # 高配点
            max_hi = max(hi[v] for v in candidates)
            candidates = [v for v in candidates if hi[v] == max_hi]
        if len(candidates) > 1:
            # 低配点
            max_lo = max(lo[v] for v in candidates)
            candidates = [v for v in candidates if lo[v] == max_lo]
        if len(candidates) > 1:
            # 定義順の優先
            for v in VARIETIES:
                if v in candidates:
                    winner = v
                    break
        else:
            winner = candidates[0]
    else:
        winner = None
    return dict(scores), winner, dict(hi), dict(lo)


def render_progress():
    total = len(QUESTIONS)
    step = st.session_state.step
    st.progress((step) / total, text=f"進捗: {step}/{total} 問回答済み")


# ----------------------------------------------------------
# UI
# ----------------------------------------------------------
init_state()

st.title("🍊 推しみかん診断")
st.caption("すべての質問(Q1〜Q12)に答えると、あなたにぴったりの柑橘をおすすめします！")

with st.expander("診断のルール", expanded=False):
    st.write("""
- 質問ごとに選択肢を1つ選びます。
- 選択肢ごとに、特定の品種へポイントが加算されます。
- 合計ポイントが最も高い品種があなたの“推しみかん”です。
- 同点のときは高配点(2点)の多さ→低配点(1点)の多さ→品種の定義順で決定します。
    """)

if not st.session_state.finished:
    render_progress()
    idx = st.session_state.step
    total = len(QUESTIONS)

    if idx < total:
        q = QUESTIONS[idx]
        st.subheader(f"{q['id']}  {q['q']}")
        opts = list(q["options"].keys())

        # 既に選んだ回答があれば復元
        prev = st.session_state.answers.get(q["id"], None)
        choice = st.radio("選択肢を選んでください", options=opts, index=opts.index(prev) if prev in opts else None)

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

else:
    # 結果ページ
else:
    scores, winner, hi, lo = compute_scores(st.session_state.answers)

    st.success("診断が完了しました！ あなたの推しみかんは・・・")
    if winner:
        st.header(f"🎉 {winner}")
        # PDF画像を一枚だけ表示
        img_path = VARIETY_IMG.get(winner)
        if img_path:
            st.pdf(img_path)
    else:
        st.warning("スコアがありません。最初からやり直してください。")

    st.divider()("診断が完了しました！ あなたの推しみかんは・・・")
    if winner:
        st.header(f"🎉 {winner}")
        info = VARIETY_INFO.get(winner, {})
        st.write(f"**キャッチコピー**：{info.get('caption', '')}")
        st.write(f"**旬**：{info.get('season', '-')}")
        st.write(f"**ひとこと**：{info.get('note', '')}")
        if info.get("image_url"):
            st.image(info["image_url"], use_column_width=True)
    else:
        st.warning("スコアがありません。最初からやり直してください。")

    # スコア表・チャート
    st.subheader("スコア内訳")
    # 辞書を安定順に整形
    chart_data = [{"品種": v, "合計": scores.get(v, 0)} for v in VARIETIES]
    chart = (
        alt.Chart(alt.Data(values=chart_data))
        .mark_bar()
        .encode(x=alt.X("品種:N", sort=VARIETIES), y=alt.Y("合計:Q"))
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)

    with st.expander("タイブレーク詳細", expanded=False):
        st.write("高配点(2点)・低配点(1点)の内訳です。")
        tb_data = [{"品種": v, "高配点合計": hi.get(v, 0), "低配点合計": lo.get(v, 0)} for v in VARIETIES]
        st.dataframe(tb_data, hide_index=True, use_container_width=True)

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
        if st.button("最初の質問に戻る", use_container_width=True):
            st.session_state.finished = False
            st.session_state.step = 0
            st.rerun()

# ----------------------------------------------------------
# （任意）ページ下部のスタイル微調整
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    /* モバイルでのタップしやすさ向上 */
    div.stRadio > div { gap: 0.5rem; }
    label.css-1cpxqw2 { padding: 0.4rem 0.6rem; }
    /* ボタン角丸＆やわらかい影 */
    button[kind="primary"], .stButton>button { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)
