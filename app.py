import streamlit as st
import pandas as pd
import joblib

# ---------- ตั้งค่าหน้าเว็บ ----------
st.set_page_config(page_title="Mobile Price Predictor", page_icon="📱", layout="centered")

# ---------- สีและสไตล์ ----------
INK = "#16213A"
SLATE = "#5E6B85"
BLUE = "#2B59C3"
LINE = "#DCE3EF"
AMBER = "#F2A93B"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap');

    html, body, .stApp, .stMarkdown, button, input, label {{
        font-family: 'IBM Plex Sans Thai', 'Noto Sans Thai', sans-serif !important;
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ padding-top: 2.2rem; max-width: 820px; }}

    /* พื้นหลังทั้งหน้า */
    .stApp {{
        background:
            radial-gradient(circle at 12% 8%, #C9D8FF 0, transparent 38%),
            radial-gradient(circle at 92% 30%, #E3D4FF 0, transparent 35%),
            radial-gradient(circle at 20% 95%, #C8EEF0 0, transparent 40%),
            #DCE4F7;
        background-attachment: fixed;
    }}

    /* ส่วนหัว */
    .hero {{
        position: relative; overflow: hidden;
        display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
        background: linear-gradient(120deg, #2B59C3 0%, #5B3FD0 60%, #8A3FD0 100%);
        color: #fff; border-radius: 28px; padding: 2.2rem 2.2rem 2.2rem 2.4rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 18px 40px -18px rgba(59, 50, 180, .55);
    }}
    .hero::before, .hero::after {{
        content: ""; position: absolute; border-radius: 50%; pointer-events: none;
    }}
    .hero::before {{ width: 260px; height: 260px; right: -60px; top: -90px; background: rgba(255,255,255,.12); }}
    .hero::after  {{ width: 180px; height: 180px; left: 38%; bottom: -120px; background: rgba(255,255,255,.08); }}
    .hero-text {{ position: relative; z-index: 1; }}
    .hero-badge {{
        display: inline-flex; align-items: center; gap: .4rem;
        background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28);
        border-radius: 99px; padding: .25rem .8rem; font-size: .85rem; margin-bottom: .8rem;
    }}
    .hero h1 {{
        color: #fff; font-size: 2.3rem; font-weight: 700; line-height: 1.2;
        margin: 0; padding: 0; letter-spacing: -.01em;
    }}
    .hero p {{ color: #E4E2FF; margin: .5rem 0 1rem; font-size: 1.02rem; max-width: 30rem; }}
    .hero-tags {{ display: flex; flex-wrap: wrap; gap: .45rem; }}
    .hero-tags span {{
        background: rgba(255,255,255,.95); color: #3A2FA8;
        border-radius: 10px; padding: .22rem .7rem; font-size: .85rem; font-weight: 600;
    }}

    /* มือถือจำลองในส่วนหัว */
    .hero-phone {{
        position: relative; z-index: 1; flex-shrink: 0;
        width: 104px; height: 196px; border-radius: 24px;
        background: #0F1530; border: 5px solid #0F1530;
        box-shadow: 0 14px 30px rgba(10, 8, 60, .45);
        transform: rotate(8deg);
    }}
    .hero-phone .scr {{
        height: 100%; border-radius: 19px;
        background: linear-gradient(170deg, #FFE7A8, {AMBER} 55%, #EE7B3B);
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .5rem;
    }}
    .hero-phone .scr b {{ color: #3A1F00; font-size: 1.3rem; }}
    .hero-phone .signal span {{ background: rgba(58,31,0,.2); }}
    .hero-phone .signal span.on {{ background: #3A1F00; }}

    /* แท่งสัญญาณ = ระดับราคา */
    .signal {{ display: flex; align-items: flex-end; gap: 6px; height: 56px; }}
    .signal span {{ width: 14px; border-radius: 4px; background: #34426A; }}
    .signal span.on {{ background: {AMBER}; }}
    .signal.light span {{ background: {LINE}; }}
    .signal.light span.on {{ background: {BLUE}; }}

    /* กล่องกรอกข้อมูล */
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stColumn"] div:has(> [data-testid="stElementContainer"] .group-title) {{
        background: #fff; border-radius: 18px !important; border-color: {LINE} !important;
    }}
    [data-testid="stNumberInputContainer"], [data-testid="stNumberInputContainer"] * {{ background-color: #F6F8FC !important; }}
    .group-title {{ font-weight: 600; font-size: 1.05rem; color: {INK}; margin-bottom: .1rem; }}
    .group-note {{ color: {SLATE}; font-size: .88rem; margin-bottom: .6rem; }}

    /* ปุ่ม */
    [data-testid="stElementContainer"]:has(.stButton) {{ width: 100% !important; }}
    .stButton, .stButton > button {{
        width: 100%; border-radius: 14px; padding: .75rem 1rem;
        font-size: 1.05rem; font-weight: 600;
    }}
    .stButton > button[kind="primary"], [data-testid="stBaseButton-primary"] {{
        background: linear-gradient(120deg, #2B59C3, #5B3FD0 60%, #8A3FD0) !important;
        border: none !important; color: #fff !important;
        box-shadow: 0 10px 24px -12px rgba(59, 50, 180, .7);
    }}
    [data-testid="stBaseButton-primary"]:hover {{ filter: brightness(1.08); }}

    /* การ์ดผลลัพธ์ */
    .result {{
        display: grid; grid-template-columns: 150px 1fr; gap: 1.6rem; align-items: center;
        background: #fff; border: 1px solid {LINE}; border-radius: 22px;
        padding: 1.6rem; margin-top: 1.2rem;
    }}
    .phone {{
        width: 130px; height: 250px; margin: 0 auto;
        border: 7px solid {INK}; border-radius: 28px; background: {INK};
        position: relative; box-sizing: border-box;
    }}
    .phone::before {{
        content: ""; position: absolute; top: 7px; left: 50%; transform: translateX(-50%);
        width: 38px; height: 7px; border-radius: 6px; background: #000; z-index: 2;
    }}
    .screen {{
        height: 100%; border-radius: 20px; background: linear-gradient(170deg, #2B59C3, #16213A);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        color: #fff; text-align: center; padding: .5rem;
    }}
    .screen .emoji {{ font-size: 2.3rem; }}
    .screen .tier {{ font-weight: 700; font-size: 1.05rem; margin-top: .35rem; }}
    .screen .en {{ font-size: .78rem; color: #C9D5F0; }}
    .result h3 {{ margin: 0 0 .2rem; color: {INK}; font-size: 1.35rem; }}
    .result .sub {{ color: {SLATE}; margin-bottom: 1rem; }}

    .prob-row {{ display: grid; grid-template-columns: 120px 1fr 52px; gap: .7rem;
                 align-items: center; margin: .45rem 0; font-size: .93rem; color: {INK}; }}
    .prob-track {{ background: #EEF2F8; border-radius: 99px; height: 10px; overflow: hidden; }}
    .prob-fill {{ background: #AEBEDF; height: 100%; border-radius: 99px; }}
    .prob-row.top .prob-fill {{ background: {BLUE}; }}
    .prob-row.top {{ font-weight: 600; }}
    .prob-val {{ text-align: right; font-variant-numeric: tabular-nums; }}

    .specs {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }}
    .chip {{ background: #EEF2F8; color: {INK}; border-radius: 99px; padding: .25rem .8rem; font-size: .85rem; }}

    .footer {{
        margin-top: 2.4rem; padding-top: 1rem; border-top: 1px solid {LINE};
        color: {SLATE}; font-size: .9rem; text-align: center;
    }}
    .footer b {{ color: {INK}; font-weight: 600; }}

    @media (max-width: 640px) {{
        .hero {{ padding: 1.6rem; }}
        .hero h1 {{ font-size: 1.6rem; }}
        .hero-phone {{ display: none; }}
        .result {{ grid-template-columns: 1fr; }}
        .prob-row {{ grid-template-columns: 95px 1fr 46px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def signal_bars(level: int, light: bool = False) -> str:
    """แท่งสัญญาณ 4 ขีด เติมตามระดับราคา (0-3)"""
    heights = [14, 26, 40, 56]
    bars = "".join(
        f'<span class="{"on" if i <= level else ""}" style="height:{h}px"></span>'
        for i, h in enumerate(heights)
    )
    return f'<div class="signal{" light" if light else ""}">{bars}</div>'


# ---------- โหลดโมเดล ----------
@st.cache_resource
def load_model():
    return joblib.load("mobile_price_tree.joblib")

model = load_model()

# ---------- ป้ายกำกับระดับราคา ----------
PRICE_LABELS = {
    0: ("💰", "ถูก", "Low Cost"),
    1: ("💵", "ปานกลาง", "Medium Cost"),
    2: ("💸", "แพง", "High Cost"),
    3: ("💎", "แพงมาก", "Very High Cost"),
}

# ---------- ส่วนหัว ----------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-text">
            <div class="hero-badge">📱 Decision Tree Model</div>
            <h1>ทำนายระดับราคามือถือ</h1>
            <p>ใส่สเปกเครื่อง แล้วดูว่าโมเดลจัดให้อยู่ในระดับราคาไหน</p>
            <div class="hero-tags">
                <span>RAM</span><span>แบตเตอรี่</span><span>หน้าจอ</span><span>น้ำหนัก</span>
            </div>
        </div>
        <div class="hero-phone"><div class="scr">
            {signal_bars(3)}
            <b>฿฿฿</b>
        </div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- ฟอร์มรับข้อมูล ----------
col1, col2 = st.columns(2, gap="medium")

with col1:
    with st.container(border=True):
        st.markdown('<div class="group-title">⚡ ประสิทธิภาพ</div>'
                    '<div class="group-note">หน่วยความจำและแบตเตอรี่</div>', unsafe_allow_html=True)
        ram = st.number_input("RAM (MB)", min_value=0, max_value=8000, value=2000, step=64,
                              help="หน่วยความจำ RAM ของเครื่อง หน่วยเป็น MB")
        battery_power = st.number_input("ความจุแบตเตอรี่ (mAh)", min_value=0, max_value=6000, value=1500, step=50)
        mobile_wt = st.number_input("น้ำหนักเครื่อง (กรัม)", min_value=0, max_value=500, value=150, step=1)

with col2:
    with st.container(border=True):
        st.markdown('<div class="group-title">🖥️ หน้าจอ</div>'
                    '<div class="group-note">ความละเอียดเป็นพิกเซล</div>', unsafe_allow_html=True)
        px_width = st.number_input("ความกว้าง (px)", min_value=0, max_value=3000, value=1080, step=10)
        px_height = st.number_input("ความสูง (px)", min_value=0, max_value=3000, value=1920, step=10)
        st.caption(f"ความละเอียดรวม {px_width:,} × {px_height:,} px")

st.write("")
predict = st.button("🔮 ทำนายระดับราคา", type="primary")

# ---------- ทำนายผล ----------
if predict:
    # เรียงคอลัมน์ตามลำดับที่โมเดลถูกเทรนมา: ram, battery_power, px_width, px_height, mobile_wt
    input_df = pd.DataFrame([{
        "ram": ram,
        "battery_power": battery_power,
        "px_width": px_width,
        "px_height": px_height,
        "mobile_wt": mobile_wt,
    }])[list(model.feature_names_in_)]

    prediction = int(model.predict(input_df)[0])
    proba = model.predict_proba(input_df)[0]
    emoji, th, en = PRICE_LABELS.get(prediction, ("📱", str(prediction), ""))

    rows = ""
    for c, p in zip(model.classes_, proba):
        e, t, _ = PRICE_LABELS[int(c)]
        top = " top" if int(c) == prediction else ""
        rows += (
            f'<div class="prob-row{top}"><div>{e} {t}</div>'
            f'<div class="prob-track"><div class="prob-fill" style="width:{p*100:.1f}%"></div></div>'
            f'<div class="prob-val">{p*100:.1f}%</div></div>'
        )

    chips = "".join(f'<span class="chip">{t}</span>' for t in [
        f"RAM {ram:,} MB", f"แบต {battery_power:,} mAh",
        f"จอ {px_width:,}×{px_height:,}", f"{mobile_wt} กรัม",
    ])

    st.markdown(
        f"""
        <div class="result">
            <div class="phone"><div class="screen">
                <div class="emoji">{emoji}</div>
                <div class="tier">{th}</div>
                <div class="en">{en}</div>
            </div></div>
            <div>
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
                    <div>
                        <h3>ระดับราคา: {th}</h3>
                        <div class="sub">ระดับ {prediction + 1} จาก 4 ({en})</div>
                    </div>
                    {signal_bars(prediction, light=True)}
                </div>
                {rows}
                <div class="specs">{chips}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("ดูข้อมูลที่ส่งเข้าโมเดล"):
        st.dataframe(input_df, hide_index=True, use_container_width=True)

# ---------- ชื่อสมาชิก ----------
st.markdown(
    '<div class="footer">สมาชิก &nbsp; <b>จิรารัตน์ รอดเพชร</b> 007 &nbsp;|&nbsp; <b>ชลธิชา มามาตร</b> 010</div>',
    unsafe_allow_html=True,
)