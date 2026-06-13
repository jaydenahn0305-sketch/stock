
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="글로벌 빅테크 주가 분석",
    page_icon="📈",
    layout="wide"
)

st.title("📈 글로벌 빅테크 주가 분석")
st.markdown("최근 1년간 주가 흐름을 비교합니다.")

tickers = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "구글": "GOOGL",
    "마이크로소프트": "MSFT",
    "애플": "AAPL"
}

with st.spinner("주가 데이터를 불러오는 중..."):

    price_df = pd.DataFrame()

    for name, ticker in tickers.items():
        data = yf.download(
            ticker,
            period="1y",
            auto_adjust=True,
            progress=False
        )

        if not data.empty:
            price_df[name] = data["Close"]

if price_df.empty:
    st.error("주가 데이터를 불러오지 못했습니다.")
    st.stop()

# --------------------------
# 정규화 그래프
# --------------------------

normalized = price_df / price_df.iloc[0] * 100

st.subheader("📊 최근 1년 주가 흐름 비교")

fig = px.line(
    normalized,
    x=normalized.index,
    y=normalized.columns,
    labels={
        "value": "기준가(100)",
        "variable": "종목",
        "index": "날짜"
    }
)

fig.update_layout(
    height=650,
    hovermode="x unified"
)

fig.update_xaxes(
    rangeslider_visible=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------
# 수익률 계산
# --------------------------

returns = (
    (price_df.iloc[-1] / price_df.iloc[0] - 1)
    * 100
).round(2)

summary = pd.DataFrame({
    "종목": returns.index,
    "1년 수익률(%)": returns.values
}).sort_values(
    "1년 수익률(%)",
    ascending=False
)

winner = summary.iloc[0]

# --------------------------
# 최고 성과 종목
# --------------------------

st.subheader("🏆 최고 성과 종목")

st.success(
    f"{winner['종목']} : {winner['1년 수익률(%)']}%"
)

# --------------------------
# 수익률 바 차트
# --------------------------

bar_fig = px.bar(
    summary,
    x="종목",
    y="1년 수익률(%)",
    text="1년 수익률(%)"
)

bar_fig.update_layout(
    height=500
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

# --------------------------
# 성과 테이블
# --------------------------

st.subheader("📋 종목별 성과")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# --------------------------
# 투자 인사이트
# --------------------------

st.subheader("💡 간단 분석")

best = summary.iloc[0]["종목"]
worst = summary.iloc[-1]["종목"]

st.write(
    f"""
    - 최근 1년간 가장 높은 수익률은 **{best}** 입니다.
    - 가장 부진한 성과는 **{worst}** 입니다.
    - 미국 빅테크와 한국 반도체 기업의 흐름을 한눈에 비교할 수 있습니다.
    - 그래프에서 특정 구간을 드래그하여 확대 분석할 수 있습니다.
    """
)

