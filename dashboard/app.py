import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pickle
import yfinance as yf

engine = create_engine("sqlite:///behavioral_finance.db")

st.set_page_config(
    page_title="AI Behavioral Finance Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0B1020 0%, #111827 45%, #0F172A 100%);
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0F172A 100%);
    border-right: 1px solid #1E293B;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #F8FAFC;
}

.hero-box {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    padding: 28px;
    border-radius: 22px;
    border: 1px solid #334155;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 16px;
    color: #CBD5E1;
}

.kpi-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid #334155;
    box-shadow: 0 8px 24px rgba(0,0,0,0.28);
}

.kpi-label {
    color: #94A3B8;
    font-size: 14px;
    font-weight: 600;
}

.kpi-value {
    color: #F8FAFC;
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-note {
    color: #38BDF8;
    font-size: 13px;
    margin-top: 8px;
}

.insight-box {
    background: rgba(6, 78, 59, 0.25);
    padding: 18px;
    border-radius: 16px;
    border-left: 5px solid #10B981;
    margin-top: 14px;
}

.warning-box {
    background: rgba(127, 29, 29, 0.32);
    padding: 18px;
    border-radius: 16px;
    border-left: 5px solid #EF4444;
    margin-top: 14px;
}

.sidebar-header {
    background: linear-gradient(135deg, #111827 0%, #1E293B 70%, #312E81 100%);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #2563EB;
    box-shadow: 0 10px 30px rgba(37,99,235,0.22);
    margin-bottom: 18px;
}

.sidebar-title {
    color: #F8FAFC;
    font-size: 20px;
    font-weight: 800;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.sidebar-subtitle {
    color: #CBD5E1;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 10px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #111827;
    border-radius: 14px;
    color: #CBD5E1;
    padding: 10px 18px;
    border: 1px solid #334155;
}

.stTabs [aria-selected="true"] {
    background-color: #2563EB !important;
    color: white !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

hr {
    border-color: #334155;
}
</style>
""", unsafe_allow_html=True)

with open("models/risk_prediction_model.pkl", "rb") as file:
    risk_model = pickle.load(file)

with open("models/risk_model_features.pkl", "rb") as file:
    model_features = pickle.load(file)

transactions = pd.read_sql("SELECT * FROM transactions", engine)
segments = pd.read_sql("SELECT * FROM user_segments", engine)
anomalies = pd.read_sql("SELECT * FROM transaction_anomalies", engine)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">AI Behavioral Finance Intelligence Platform</div>
    <div class="hero-subtitle">
        Advanced analytics system for financial stress, impulse spending, marketing triggers, ML risk prediction, and anomaly detection.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------

st.sidebar.markdown("""
<div class="sidebar-header">
    <div class="sidebar-title">⚙️ Control Panel</div>
    <div class="sidebar-subtitle">
        Filter financial behavior, payment risk, and user segments.
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar.container(border=True):
    st.markdown("#### 🔎 SPENDING FILTERS")

    category_choice = st.selectbox(
        "Category",
        options=["All Categories"] + sorted(transactions["category"].unique()),
        index=0
    )

    payment_choice = st.selectbox(
        "Payment Method",
        options=["All Payment Methods"] + sorted(transactions["payment_method"].unique()),
        index=0
    )

with st.sidebar.container(border=True):
    st.markdown("#### 👥 USER FILTERS")

    segment_choice = st.selectbox(
        "User Segment",
        options=["All Segments"] + sorted(segments["segment"].unique()),
        index=0
    )

with st.sidebar.container(border=True):
    st.markdown("#### 📊 DATA SUMMARY")

    st.metric("Total Transactions", f"{len(transactions):,}")
    st.metric("Total Users", f"{segments['user_id'].nunique():,}")
    st.metric("Anomalies Detected", f"{int(anomalies['is_anomaly'].sum()):,}")

with st.sidebar.container(border=True):
    st.markdown("""
    💡 **Pro Tip**  
    Use filters to analyze spending patterns and identify high-risk behavior segments.
    """)

filtered_transactions = transactions.copy()
filtered_segments = segments.copy()

if category_choice != "All Categories":
    filtered_transactions = filtered_transactions[
        filtered_transactions["category"] == category_choice
    ]

if payment_choice != "All Payment Methods":
    filtered_transactions = filtered_transactions[
        filtered_transactions["payment_method"] == payment_choice
    ]

if segment_choice != "All Segments":
    filtered_segments = filtered_segments[
        filtered_segments["segment"] == segment_choice
    ]

if filtered_transactions.empty or filtered_segments.empty:
    st.warning("No data available for selected filters. Adjust filters from sidebar.")
    st.stop()

# ---------------- Helper Functions ----------------

def kpi_card(label, value, note):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def generate_recommendation(user):
    segment = user["segment"]
    impulse = user["impulse_purchase"]
    stress = user["financial_stress_level"]
    late_night = user["is_late_night"]
    ad_clicked = user["ad_clicked"]

    recommendations = []

    if impulse > 0.45:
        recommendations.append("Impulse spending is high. Reduce discretionary purchases like electronics, fashion, and entertainment.")

    if stress > 4:
        recommendations.append("Financial stress level is elevated. Build a fixed monthly budget and avoid high-ticket purchases.")

    if late_night > 0.25:
        recommendations.append("Late-night spending pattern is risky. Avoid shopping apps after 10 PM.")

    if ad_clicked > 0.35:
        recommendations.append("Ad-driven purchases are high. Limit exposure to promotional offers and impulse-triggering campaigns.")

    if segment == "High Risk User":
        recommendations.append("Reduce BNPL and credit card dependency to control debt-driven consumption.")

    if segment == "Stable Saver":
        recommendations.append("User shows controlled financial behavior. Increase investment allocation gradually.")

    if not recommendations:
        recommendations.append("User behavior is moderate. Maintain current spending discipline and monitor discretionary categories.")

    return recommendations

@st.cache_data(ttl=900)
def get_stock_data(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

# ---------------- Tabs ----------------
overview_tab, markets_tab, investment_tab, behavior_tab, ml_tab, anomaly_tab, chatbot_tab, users_tab = st.tabs([
    "Executive Overview",
    "Global Markets",
    "Investment Behavior",
    "Behavioral Insights",
    "ML Risk Engine",
    "Anomaly Detection",
    "Finance Chatbot",
    "User Explorer"
])

with overview_tab:
    total_spending = filtered_transactions["amount"].sum()
    avg_transaction = filtered_transactions["amount"].mean()
    impulse_rate = filtered_transactions["impulse_purchase"].mean() * 100
    avg_stress = filtered_transactions["financial_stress_level"].mean()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card("Total Spending", f"₹{total_spending:,.0f}", "Filtered transaction value")
    with c2:
        kpi_card("Avg Transaction", f"₹{avg_transaction:,.0f}", "Average ticket size")
    with c3:
        kpi_card("Impulse Rate", f"{impulse_rate:.2f}%", "Impulse purchase probability")
    with c4:
        kpi_card("Avg Stress", f"{avg_stress:.2f}/10", "Financial stress indicator")

    st.divider()

    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("Category Wise Spending")

        category_spending = (
            filtered_transactions
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#0F172A")
        ax.set_facecolor("#0F172A")
        category_spending.plot(kind="bar", ax=ax)
        ax.set_title("Total Spending by Category", color="white")
        ax.set_ylabel("Total Spending", color="white")
        ax.set_xlabel("Category", color="white")
        ax.tick_params(colors="white", rotation=45)
        st.pyplot(fig)

    with right:
        st.subheader("Impulse vs Normal Transactions")

        impulse_counts = filtered_transactions["impulse_purchase"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(7, 5))
        fig2.patch.set_facecolor("#0F172A")
        ax2.set_facecolor("#0F172A")
        impulse_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title("Impulse Purchase Split", color="white")
        st.pyplot(fig2)

    st.subheader("Payment Method Risk Analysis")

    payment_risk = filtered_transactions.groupby("payment_method").agg({
        "impulse_purchase": "mean",
        "financial_stress_level": "mean",
        "amount": "mean"
    }).reset_index()

    payment_risk["impulse_purchase"] = payment_risk["impulse_purchase"] * 100

    payment_risk.rename(columns={
        "impulse_purchase": "impulse_rate_percent",
        "financial_stress_level": "avg_stress_level",
        "amount": "avg_transaction_value"
    }, inplace=True)

    st.dataframe(payment_risk, use_container_width=True)

with markets_tab:
    st.subheader("Global Stock Market Tracker")

    stock_options = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Nvidia": "NVDA",
        "Tesla": "TSLA",
        "Amazon": "AMZN",
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Nifty 50": "^NSEI",
        "Sensex": "^BSESN",
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC"
    }

    selected_stock_name = st.selectbox(
        "Select Global Stock / Index",
        options=list(stock_options.keys())
    )

    selected_ticker = stock_options[selected_stock_name]

    stock_data = get_stock_data(selected_ticker, period="6mo")

    if stock_data.empty:
        st.warning("No stock data available. Try another ticker.")
    else:
        latest_price = stock_data["Close"].iloc[-1]
        first_price = stock_data["Close"].iloc[0]
        return_pct = ((latest_price - first_price) / first_price) * 100
        volatility = stock_data["Close"].pct_change().std() * 100

        s1, s2, s3 = st.columns(3)

        with s1:
            kpi_card("Latest Price", f"{latest_price:,.2f}", selected_ticker)

        with s2:
            kpi_card("6M Return", f"{return_pct:.2f}%", "Price performance")

        with s3:
            kpi_card("Volatility", f"{volatility:.2f}%", "Daily movement risk")

        st.subheader(f"{selected_stock_name} Price Trend")

        fig_market, ax_market = plt.subplots(figsize=(12, 5))
        fig_market.patch.set_facecolor("#0F172A")
        ax_market.set_facecolor("#0F172A")
        ax_market.plot(stock_data.index, stock_data["Close"])
        ax_market.set_title(f"{selected_stock_name} Closing Price", color="white")
        ax_market.set_xlabel("Date", color="white")
        ax_market.set_ylabel("Close Price", color="white")
        ax_market.tick_params(colors="white")
        st.pyplot(fig_market)

        st.subheader("Latest Market Data")
        st.dataframe(stock_data.tail(10), use_container_width=True)

with investment_tab:
    st.subheader("Investment Behavior Engine")

    investment_txns = filtered_transactions[
        filtered_transactions["category"] == "Investment"
    ]

    total_investment = investment_txns["amount"].sum()
    avg_investment = investment_txns["amount"].mean()
    investment_users = investment_txns["user_id"].nunique()

    total_spending_all = filtered_transactions["amount"].sum()
    investment_rate = (total_investment / total_spending_all) * 100 if total_spending_all > 0 else 0

    i1, i2, i3, i4 = st.columns(4)

    with i1:
        kpi_card("Total Investment", f"₹{total_investment:,.0f}", "Total amount invested")

    with i2:
        kpi_card("Avg Investment", f"₹{avg_investment:,.0f}", "Average investment transaction")

    with i3:
        kpi_card("Investing Users", f"{investment_users:,}", "Users who invested")

    with i4:
        kpi_card("Investment Rate", f"{investment_rate:.2f}%", "Investment as % of spending")

    st.divider()

    st.subheader("Investment by User Segment")

    investment_by_user = investment_txns.groupby("user_id")["amount"].sum().reset_index()
    investment_by_user.rename(columns={"amount": "total_investment"}, inplace=True)

    segment_investment = filtered_segments.merge(
        investment_by_user,
        on="user_id",
        how="left"
    )

    segment_investment["total_investment"] = segment_investment["total_investment"].fillna(0)

    segment_investment_summary = segment_investment.groupby("segment").agg({
        "total_investment": "mean",
        "impulse_purchase": "mean",
        "financial_stress_level": "mean"
    }).reset_index()

    segment_investment_summary.rename(columns={
        "total_investment": "avg_investment",
        "impulse_purchase": "avg_impulse_behavior",
        "financial_stress_level": "avg_stress_level"
    }, inplace=True)

    st.dataframe(segment_investment_summary, use_container_width=True)

    st.subheader("Segment-wise Investment Behavior")

    fig_inv, ax_inv = plt.subplots(figsize=(10, 5))
    fig_inv.patch.set_facecolor("#0F172A")
    ax_inv.set_facecolor("#0F172A")

    segment_investment_summary.set_index("segment")["avg_investment"].plot(
        kind="bar",
        ax=ax_inv
    )

    ax_inv.set_title("Average Investment by Segment", color="white")
    ax_inv.set_ylabel("Average Investment", color="white")
    ax_inv.set_xlabel("Segment", color="white")
    ax_inv.tick_params(colors="white", rotation=30)

    st.pyplot(fig_inv)

    if investment_rate < 10:
        st.markdown("""
        <div class="warning-box">
        <b>Investment Discipline Warning:</b><br>
        Investment allocation is low compared to total spending. Users may be prioritizing consumption over wealth creation.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="insight-box">
        <b>Investment Discipline Insight:</b><br>
        Users show a healthy investment allocation relative to spending behavior.
        </div>
        """, unsafe_allow_html=True)


with behavior_tab:
    st.subheader("User Segment Summary")

    segment_summary = filtered_segments.groupby("segment").agg({
        "user_id": "count",
        "amount": "mean",
        "impulse_purchase": "mean",
        "financial_stress_level": "mean"
    }).reset_index()

    segment_summary.rename(columns={
        "user_id": "total_users",
        "amount": "avg_spending",
        "impulse_purchase": "avg_impulse_behavior",
        "financial_stress_level": "avg_stress_level"
    }, inplace=True)

    st.dataframe(segment_summary, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Segment Distribution")

        segment_counts = filtered_segments["segment"].value_counts()

        fig3, ax3 = plt.subplots(figsize=(8, 5))
        fig3.patch.set_facecolor("#0F172A")
        ax3.set_facecolor("#0F172A")
        segment_counts.plot(kind="bar", ax=ax3)
        ax3.set_title("Users by Segment", color="white")
        ax3.tick_params(colors="white", rotation=30)
        st.pyplot(fig3)

    with col_b:
        st.subheader("Stress by Segment")

        stress_segment = filtered_segments.groupby("segment")["financial_stress_level"].mean().sort_values()

        fig4, ax4 = plt.subplots(figsize=(8, 5))
        fig4.patch.set_facecolor("#0F172A")
        ax4.set_facecolor("#0F172A")
        stress_segment.plot(kind="barh", ax=ax4)
        ax4.set_title("Average Stress Level by Segment", color="white")
        ax4.tick_params(colors="white")
        st.pyplot(fig4)

    late_night = filtered_transactions.groupby("is_late_night")["impulse_purchase"].mean() * 100

    st.markdown(
        f"""
        <div class="insight-box">
        <b>Behavioral Insight:</b><br>
        Late-night impulse purchase rate is <b>{late_night.get(1, 0):.2f}%</b>,
        compared to <b>{late_night.get(0, 0):.2f}%</b> during normal hours.
        This indicates emotionally-driven spending risk during low-control hours.
        </div>
        """,
        unsafe_allow_html=True
    )

with ml_tab:
    st.subheader("ML Financial Risk Prediction")

    selected_user_ml = st.selectbox(
        "Select User ID for ML Prediction",
        options=sorted(filtered_segments["user_id"].unique()),
        key="ml_user"
    )

    user_data_ml = filtered_segments[filtered_segments["user_id"] == selected_user_ml].iloc[0]

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        kpi_card("Segment", user_data_ml["segment"], "Behavioral cluster")
    with m2:
        kpi_card("Avg Spending", f"₹{user_data_ml['amount']:,.0f}", "Mean user spend")
    with m3:
        kpi_card("Impulse Score", f"{user_data_ml['impulse_purchase']*100:.2f}%", "User impulse rate")
    with m4:
        kpi_card("Stress Level", f"{user_data_ml['financial_stress_level']:.2f}/10", "Financial pressure")

    prediction_features = pd.DataFrame([{
        "amount": user_data_ml["amount"],
        "impulse_purchase": user_data_ml["impulse_purchase"],
        "financial_stress_level": user_data_ml["financial_stress_level"],
        "is_late_night": user_data_ml["is_late_night"],
        "ad_clicked": user_data_ml["ad_clicked"],
        "discount_used": user_data_ml["discount_used"],
        "cashback_used": user_data_ml["cashback_used"]
    }])

    prediction_features = prediction_features[model_features]

    risk_prediction = risk_model.predict(prediction_features)[0]
    risk_probability = risk_model.predict_proba(prediction_features)[0][1]

    if risk_prediction == 1:
        st.markdown(
            f"""
            <div class="warning-box">
            <b>HIGH FINANCIAL RISK</b><br>
            Model probability: <b>{risk_probability:.2%}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="insight-box">
            <b>LOW FINANCIAL RISK</b><br>
            Model probability: <b>{risk_probability:.2%}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("AI Recommendation Engine")

    recommendations = generate_recommendation(user_data_ml)

    for rec in recommendations:
        st.markdown(f"- {rec}")

with anomaly_tab:
    st.subheader("Anomaly Detection")

    total_anomalies = anomalies["is_anomaly"].sum()
    anomaly_rate = (total_anomalies / len(anomalies)) * 100
    avg_anomaly_amount = anomalies[anomalies["is_anomaly"] == 1]["amount"].mean()

    a1, a2, a3 = st.columns(3)

    with a1:
        kpi_card("Anomalous Transactions", f"{int(total_anomalies):,}", "Detected by Isolation Forest")
    with a2:
        kpi_card("Anomaly Rate", f"{anomaly_rate:.2f}%", "Share of total transactions")
    with a3:
        kpi_card("Avg Anomaly Amount", f"₹{avg_anomaly_amount:,.0f}", "Mean suspicious transaction")

    st.subheader("Top Suspicious Transactions")

    top_anomalies = anomalies[anomalies["is_anomaly"] == 1].sort_values(
        by="amount",
        ascending=False
    ).head(20)

    st.dataframe(top_anomalies, use_container_width=True)

    st.subheader("Anomaly Category Breakdown")

    anomaly_category = (
        anomalies[anomalies["is_anomaly"] == 1]
        .groupby("category")["transaction_id"]
        .count()
        .sort_values(ascending=False)
    )

    fig5, ax5 = plt.subplots(figsize=(10, 5))
    fig5.patch.set_facecolor("#0F172A")
    ax5.set_facecolor("#0F172A")
    anomaly_category.plot(kind="bar", ax=ax5)
    ax5.set_title("Anomalies by Category", color="white")
    ax5.tick_params(colors="white", rotation=45)
    st.pyplot(fig5)

with chatbot_tab:
    st.subheader("AI Financial Behavior Assistant")

    user_question = st.text_input(
        "Ask a finance behavior question",
        placeholder="Example: Why are users financially high risk?"
    )

    if user_question:
        q = user_question.lower()

        if "high risk" in q or "risk" in q:
            st.markdown("""
            <div class="warning-box">
            <b>Answer:</b><br>
            Users become high risk when impulse spending, financial stress, late-night spending,
            and debt-driven payment methods like BNPL or credit cards increase together.
            </div>
            """, unsafe_allow_html=True)

        elif "investment" in q or "invest" in q:
            st.markdown("""
            <div class="insight-box">
            <b>Answer:</b><br>
            Investment behavior is judged by comparing investment allocation against total spending.
            Low investment rate may indicate users are prioritizing consumption over wealth creation.
            </div>
            """, unsafe_allow_html=True)

        elif "late night" in q or "night" in q:
            st.markdown("""
            <div class="warning-box">
            <b>Answer:</b><br>
            Late-night spending often indicates lower self-control and emotional buying.
            In this dashboard, late-night behavior is treated as a behavioral risk signal.
            </div>
            """, unsafe_allow_html=True)

        elif "bnpl" in q or "credit card" in q:
            st.markdown("""
            <div class="warning-box">
            <b>Answer:</b><br>
            BNPL and credit card usage can increase impulse behavior because payment pain is delayed.
            This may create debt dependency if spending is not controlled.
            </div>
            """, unsafe_allow_html=True)

        elif "anomaly" in q or "fraud" in q:
            st.markdown("""
            <div class="insight-box">
            <b>Answer:</b><br>
            Anomaly detection identifies unusual transactions based on amount, timing,
            mood score, stress level, and impulse behavior.
            </div>
            """, unsafe_allow_html=True)

        elif "stock" in q or "market" in q:
            st.markdown("""
            <div class="insight-box">
            <b>Answer:</b><br>
            The Global Markets tab tracks selected stocks and indices using live market data.
            It shows latest price, 6-month return, and volatility.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="insight-box">
            <b>Answer:</b><br>
            This assistant currently explains behavioral finance signals such as impulse spending,
            financial stress, investment discipline, stock market tracking, and anomaly detection.
            </div>
            """, unsafe_allow_html=True)



with users_tab:
    st.subheader("User Risk Explorer")

    selected_user = st.selectbox(
        "Select User ID",
        options=sorted(filtered_segments["user_id"].unique()),
        key="explorer_user"
    )

    user_data = filtered_segments[filtered_segments["user_id"] == selected_user].iloc[0]

    u1, u2, u3, u4 = st.columns(4)

    with u1:
        kpi_card("User Segment", user_data["segment"], "Cluster result")
    with u2:
        kpi_card("Avg Spending", f"₹{user_data['amount']:,.0f}", "Mean user spend")
    with u3:
        kpi_card("Impulse Score", f"{user_data['impulse_purchase']*100:.2f}%", "Impulse behavior")
    with u4:
        kpi_card("Stress Level", f"{user_data['financial_stress_level']:.2f}/10", "Financial stress")

    st.subheader("Top 20 High Risk Users")

    high_risk_users = filtered_segments.sort_values(
        by=["financial_stress_level", "impulse_purchase"],
        ascending=False
    ).head(20)

    st.dataframe(high_risk_users, use_container_width=True)
