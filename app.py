import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="CarValue India – AI Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background: #060b14;
    color: #e2e8f0;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f3c 50%, #0a0f1e 100%);
    border: 1px solid rgba(0,255,200,0.15);
    border-radius: 24px;
    padding: 0;
    margin-bottom: 2rem;
    overflow: hidden;
    position: relative;
}
.hero-inner { padding: 2.5rem 2.5rem 2rem; position: relative; z-index: 2; }
.hero::before {
    content: '';
    position: absolute; top: -100px; right: -80px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(0,255,180,0.12) 0%, transparent 65%);
    border-radius: 50%; z-index: 1;
}
.hero::after {
    content: '';
    position: absolute; bottom: -80px; left: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,140,255,0.1) 0%, transparent 65%);
    border-radius: 50%; z-index: 1;
}
.hero-car {
    font-size: 5rem; line-height: 1; display: block; margin-bottom: 0.8rem;
    filter: drop-shadow(0 0 30px rgba(0,255,180,0.5)) drop-shadow(0 0 60px rgba(0,140,255,0.3));
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0px) rotate(-2deg); }
    50%      { transform: translateY(-12px) rotate(2deg); }
}
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.6rem; font-weight: 900; color: #fff;
    line-height: 1.1; margin: 0 0 0.4rem; letter-spacing: 1px;
}
.hero-title .ac1 { color: #00ffc8; }
.hero-title .ac2 { color: #0099ff; }
.hero-sub { font-size: 1.05rem; color: #5a7fa0; font-weight: 400; margin: 0 0 1.5rem; }
.badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    background: rgba(0,255,200,0.07); border: 1px solid rgba(0,255,200,0.2);
    color: #00ffc8; padding: 4px 14px; border-radius: 30px;
    font-size: 0.75rem; font-weight: 600; letter-spacing: 0.5px;
}
.badge.b { background: rgba(0,153,255,0.07); border-color: rgba(0,153,255,0.2); color: #0099ff; }

/* ── Section Cards ── */
.scard {
    background: linear-gradient(145deg, #0d1628, #0a1220);
    border: 1px solid rgba(0,255,200,0.1);
    border-radius: 18px; padding: 1.6rem 1.8rem; margin-bottom: 1.3rem;
    position: relative; overflow: hidden;
}
.scard::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #00ffc8, #0099ff);
    border-radius: 4px 0 0 4px;
}
.shead { display: flex; align-items: center; gap: 12px; margin-bottom: 1.2rem; }
.sicon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, rgba(0,255,200,0.15), rgba(0,153,255,0.15));
    border: 1px solid rgba(0,255,200,0.2); border-radius: 12px;
    display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
}
.stitle {
    font-family: 'Orbitron', sans-serif; font-size: 0.82rem; font-weight: 700;
    color: #00ffc8; margin: 0; letter-spacing: 0.5px; text-transform: uppercase;
}
.sdesc { font-size: 0.8rem; color: #3a5570; margin: 0; }

/* ── Result ── */
.result-wrap {
    background: linear-gradient(135deg, #061a2e, #0a2040);
    border: 2px solid #00ffc8; border-radius: 20px; padding: 2rem 1.8rem;
    text-align: center; position: relative; overflow: hidden;
    box-shadow: 0 0 40px rgba(0,255,200,0.1);
}
.rlabel {
    font-family: 'Orbitron', sans-serif; font-size: 0.68rem; letter-spacing: 3px;
    color: #3a6080; text-transform: uppercase; margin-bottom: 0.5rem;
}
.rprice {
    font-family: 'Orbitron', sans-serif; font-size: 3rem; font-weight: 900;
    color: #00ffc8; line-height: 1; margin-bottom: 0.3rem;
    text-shadow: 0 0 30px rgba(0,255,200,0.4);
}
.rsub { font-size: 0.88rem; color: #3a5570; margin-bottom: 1.4rem; }
.rrange { display: flex; justify-content: space-around; border-top: 1px solid rgba(0,255,200,0.15); padding-top: 1.2rem; }
.rrange-item { text-align: center; }
.rrange-label { font-size: 0.7rem; color: #2a4560; margin-bottom: 3px; }
.rrange-val { font-family: 'Orbitron', sans-serif; font-size: 1rem; font-weight: 700; color: #a0c8e0; }

/* ── Summary ── */
.sum-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 0; border-bottom: 1px solid rgba(0,255,200,0.05);
}
.sum-key { font-size: 0.82rem; color: #3a5570; }
.sum-val { font-size: 0.85rem; color: #c0d8e8; font-weight: 600; }

/* ── Contact ── */
.contact-wrap {
    background: linear-gradient(145deg, #0d1628, #0a1220);
    border: 1px solid rgba(0,255,200,0.12); border-radius: 18px;
    padding: 1.8rem; margin-top: 1.3rem; position: relative; overflow: hidden;
}
.contact-wrap::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #00ffc8, #0099ff);
    border-radius: 4px 0 0 4px;
}
.contact-head {
    font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 700;
    color: #00ffc8; letter-spacing: 1px; text-transform: uppercase;
    margin-bottom: 1.3rem; display: flex; align-items: center; gap: 8px;
}
.contact-avatar {
    width: 70px; height: 70px;
    background: linear-gradient(135deg, #00ffc8, #0099ff);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 900;
    color: #060b14; margin: 0 auto 1rem;
    box-shadow: 0 0 25px rgba(0,255,200,0.3);
}
.contact-name {
    font-family: 'Orbitron', sans-serif; font-size: 1rem; font-weight: 700;
    color: #e2e8f0; text-align: center; margin-bottom: 0.2rem;
}
.contact-role { font-size: 0.8rem; color: #3a5570; text-align: center; margin-bottom: 1.4rem; }
.citem {
    display: flex; align-items: center; gap: 12px;
    background: rgba(0,255,200,0.04); border: 1px solid rgba(0,255,200,0.08);
    border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;
}
.citem-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, rgba(0,255,200,0.12), rgba(0,153,255,0.12));
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 1rem; flex-shrink: 0;
}
.citem-label { font-size: 0.7rem; color: #3a5570; letter-spacing: 0.5px; margin-bottom: 1px; }
.citem-val { font-size: 0.88rem; color: #a0c8e0; font-weight: 600; }

/* ── Placeholder ── */
.placeholder {
    background: rgba(0,255,200,0.03); border: 1px dashed rgba(0,255,200,0.12);
    border-radius: 18px; padding: 3rem 2rem; text-align: center;
}

/* ── Streamlit Overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    color: #5a7fa0 !important; font-size: 0.82rem !important;
    font-weight: 600 !important; letter-spacing: 0.3px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00ffc8, #0099ff) !important;
    color: #060b14 !important; border: none !important;
    border-radius: 14px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important; font-size: 0.88rem !important;
    padding: 0.85rem 2rem !important; width: 100% !important;
    letter-spacing: 1px; text-transform: uppercase;
    box-shadow: 0 0 25px rgba(0,255,200,0.2);
}
.stButton > button:hover { opacity: 0.88 !important; }
footer, #MainMenu, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open('car_price_model.pkl', 'rb') as f:
        return pickle.load(f)
try:
    model = load_model()
    model_loaded = True
except:
    model_loaded = False

# ── Data ──────────────────────────────────────────────────────────────────────
CAR_BRANDS = {
    "Maruti Suzuki": ["Swift","Baleno","Dzire","Alto","WagonR","Vitara Brezza","Ertiga","Celerio","Ignis","S-Cross","XL6","Ciaz","Grand Vitara"],
    "Hyundai":       ["i20","Creta","Verna","i10","Tucson","Venue","Aura","Alcazar","Exter","Ioniq 5"],
    "Tata":          ["Nexon","Harrier","Safari","Tiago","Altroz","Punch","Tigor","Curvv"],
    "Mahindra":      ["XUV700","Scorpio","Thar","XUV300","Bolero","KUV100","Marazzo","Scorpio-N","BE 6e"],
    "Honda":         ["City","Amaze","WR-V","Jazz","CR-V","Elevate","Accord"],
    "Toyota":        ["Innova Crysta","Fortuner","Glanza","Urban Cruiser","Camry","Hyryder","Hilux"],
    "Kia":           ["Seltos","Sonet","Carnival","EV6","Carens","Syros"],
    "Renault":       ["Kwid","Triber","Kiger","Duster"],
    "Volkswagen":    ["Polo","Vento","Taigun","Tiguan","Virtus"],
    "Skoda":         ["Rapid","Octavia","Superb","Kushaq","Slavia"],
    "MG":            ["Hector","Astor","Gloster","ZS EV","Comet EV","Windsor EV"],
    "Jeep":          ["Compass","Meridian","Wrangler","Grand Cherokee"],
    "BMW":           ["3 Series","5 Series","X1","X3","X5","7 Series","i4"],
    "Mercedes-Benz": ["C-Class","E-Class","GLA","GLC","S-Class","EQS"],
    "Audi":          ["A4","A6","Q3","Q5","Q7","e-tron GT"],
    "Nissan":        ["Magnite","Kicks","Sunny","GT-R"],
    "Ford":          ["EcoSport","Figo","Aspire","Endeavour"],
    "Citroen":       ["C3","C3 Aircross","C5 Aircross"],
}
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
YEARS  = list(range(2026, 1994, -1))

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <span class="hero-car">🚗</span>
    <div class="hero-title"><span class="ac1">Car</span><span class="ac2">Value</span> India</div>
    <p class="hero-sub">AI-powered used car resale price estimator for the Indian market</p>
    <div class="badge-row">
      <span class="badge">✦ ML Powered</span>
      <span class="badge">✦ 18+ Brands</span>
      <span class="badge b">✦ Real-time Estimate</span>
      <span class="badge b">✦ Indian Market</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85], gap="large")

# ════════════════════════ LEFT COLUMN ════════════════════════
with left:

    # — Car Identity —
    st.markdown("""<div class="scard"><div class="shead">
      <div class="sicon">🏷️</div>
      <div><p class="stitle">Car Identity</p><p class="sdesc">Brand, model & purchase info</p></div>
    </div></div>""", unsafe_allow_html=True)

    brand        = st.selectbox("Select Brand", list(CAR_BRANDS.keys()))
    model_name   = st.selectbox("Select Model", CAR_BRANDS[brand])
    col_m, col_y = st.columns(2)
    with col_m: purchase_month = st.selectbox("Month of Purchase", MONTHS)
    with col_y: purchase_year  = st.selectbox("Year of Purchase", YEARS, index=5)
    present_price = st.number_input("Ex-showroom Price (₹ Lakhs)", min_value=1.0, max_value=300.0, value=8.0, step=0.5)

    # — Usage Details —
    st.markdown("""<div class="scard"><div class="shead">
      <div class="sicon">📊</div>
      <div><p class="stitle">Usage Details</p><p class="sdesc">Mileage, fuel & transmission</p></div>
    </div></div>""", unsafe_allow_html=True)

    kms_driven   = st.number_input("Kilometres Driven", min_value=100, max_value=1000000, value=35000, step=1000)
    col_f, col_t = st.columns(2)
    with col_f: fuel_type    = st.selectbox("Fuel Type", ["Petrol","Diesel","CNG","Electric","Hybrid"])
    with col_t: transmission = st.selectbox("Transmission", ["Manual","Automatic","AMT","CVT","DCT"])
    seller_type  = st.selectbox("Seller Type", ["Individual","Dealer","Trustmark Dealer"])

    # — Ownership —
    st.markdown("""<div class="scard"><div class="shead">
      <div class="sicon">👤</div>
      <div><p class="stitle">Ownership History</p><p class="sdesc">Previous owners & condition</p></div>
    </div></div>""", unsafe_allow_html=True)

    owner     = st.selectbox("Number of Previous Owners", [0,1,2,3,4],
                    format_func=lambda x: "First Owner — No previous owners" if x==0 else f"{x} Previous Owner{'s' if x>1 else ''}")
    condition = st.select_slider("Overall Car Condition",
                    options=["Poor","Fair","Good","Very Good","Excellent"], value="Good")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    predict_clicked = st.button("⚡  PREDICT RESALE PRICE")


# ════════════════════════ RIGHT COLUMN ════════════════════════
with right:

    # — Summary —
    st.markdown("""<div class="scard"><div class="shead">
      <div class="sicon">📋</div>
      <div><p class="stitle">Your Car Summary</p><p class="sdesc">Live preview of entered details</p></div>
    </div>""", unsafe_allow_html=True)

    for k, v in {
        "🏷️ Brand": brand, "🚘 Model": model_name,
        "📅 Purchased": f"{purchase_month} {purchase_year}",
        "💰 Ex-showroom": f"₹ {present_price} L",
        "🛣️ KMs Driven": f"{kms_driven:,} km",
        "⛽ Fuel": fuel_type, "⚙️ Transmission": transmission,
        "🤝 Seller": seller_type, "👤 Prev. Owners": str(owner),
        "✨ Condition": condition,
    }.items():
        st.markdown(f'<div class="sum-row"><span class="sum-key">{k}</span><span class="sum-val">{v}</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # — Result —
    if predict_clicked:
        car_age      = 2026 - purchase_year
        cond_mult    = {"Poor":0.72,"Fair":0.86,"Good":1.0,"Very Good":1.09,"Excellent":1.17}
        mult         = cond_mult[condition]
        fuel_diesel  = 1 if fuel_type == "Diesel"     else 0
        fuel_petrol  = 1 if fuel_type == "Petrol"     else 0
        seller_ind   = 1 if seller_type == "Individual" else 0
        trans_manual = 1 if transmission == "Manual"  else 0
        inp          = np.array([[present_price, kms_driven, owner, car_age, fuel_diesel, fuel_petrol, seller_ind, trans_manual]])

        if model_loaded:
            pred = round(model.predict(inp)[0] * mult, 2)
        else:
            dep  = max(0.25, 1 - (car_age * 0.075) - (kms_driven / 600000))
            pred = round(present_price * dep * mult, 2)

        low     = round(pred * 0.91, 2)
        high    = round(pred * 1.09, 2)
        dep_pct = round((1 - pred / present_price) * 100, 1) if present_price > 0 else 0

        st.markdown(f"""
        <div class="result-wrap">
          <p class="rlabel">Estimated Resale Price</p>
          <p class="rprice">₹ {pred} L</p>
          <p class="rsub">{brand} {model_name} &nbsp;·&nbsp; {purchase_year} &nbsp;·&nbsp; {fuel_type}</p>
          <div class="rrange">
            <div class="rrange-item"><p class="rrange-label">Low Estimate</p><p class="rrange-val">₹ {low} L</p></div>
            <div class="rrange-item"><p class="rrange-label">Depreciation</p><p class="rrange-val">{dep_pct}%</p></div>
            <div class="rrange-item"><p class="rrange-label">High Estimate</p><p class="rrange-val">₹ {high} L</p></div>
          </div>
        </div>""", unsafe_allow_html=True)

        if not model_loaded:
            st.warning("⚠️ Model not found — showing demo estimate. Save your trained model as `car_price_model.pkl`.")
    else:
        st.markdown("""
        <div class="placeholder">
          <div style="font-size:3.5rem;margin-bottom:1rem;filter:drop-shadow(0 0 20px rgba(0,255,200,0.4))">🚗</div>
          <p style="color:#1e3a50;font-size:0.9rem;margin:0">
            Fill in all details on the left<br>and click <strong style="color:#2a5570">⚡ Predict Resale Price</strong>
          </p>
        </div>""", unsafe_allow_html=True)

    # ── Contact Section ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="contact-wrap">
      <div class="contact-head"><span>📡</span> Contact Developer</div>
      <div class="contact-avatar">AK</div>
      <p class="contact-name">Ayush Ranjan Keshri</p>
      <p class="contact-role">Data Science Student &nbsp;·&nbsp; ML Developer</p>

      <div class="citem">
        <div class="citem-icon">📧</div>
        <div><p class="citem-label">EMAIL ADDRESS</p><p class="citem-val">ayushkeshri5932@gmail.com</p></div>
      </div>
      <div class="citem">
        <div class="citem-icon">📱</div>
        <div><p class="citem-label">PHONE NUMBER</p><p class="citem-val">+91 8986000171</p></div>
      </div>
      <div class="citem">
        <div class="citem-icon">📍</div>
        <div><p class="citem-label">LOCATION</p><p class="citem-val">Ludhiana, Punjab, India</p></div>
      </div>
      <div class="citem">
        <div class="citem-icon">🐙</div>
        <div><p class="citem-label">GITHUB</p><p class="citem-val">github.com/ayushkeshri</p></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1.5rem;border-top:1px solid rgba(0,255,200,0.07);">
  <p style="color:#1a3a50;font-size:0.82rem;margin:0;font-family:'Rajdhani',sans-serif">
    CarValue India &nbsp;·&nbsp; ML-Powered Resale Price Estimator &nbsp;·&nbsp; Built with Streamlit & scikit-learn
  </p>
  <p style="color:#122a3a;font-size:0.75rem;margin:4px 0 0;font-family:'Rajdhani',sans-serif">
    Estimates only — actual resale value may vary based on market conditions &amp; negotiation
  </p>
</div>
""", unsafe_allow_html=True)