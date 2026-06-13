"미국 TOP10":

    st.title("🚀 미국 대표 주식 TOP 10")

    tickers = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Nvidia": "NVDA",
        "Amazon": "AMZN",
        "Google": "GOOGL",
        "Tesla": "TSLA",
        "Meta": "META",
        "Netflix": "NFLX",
        "AMD": "AMD",
        "Broadcom": "AVGO"
    }

    price_df = pd.DataFrame()

    with st.spinner("📈 데이터를 수집중..."):

        for name, ticker in tickers.items():

            data = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if not data.empty:
                price_df[name] = data["Close"]

    normalized = price_df.div(
        price_df.iloc[0]
    ).mul(100)

    fig = px.line(
        normalized,
        x=normalized.index,
        y=normalized.columns,
        title="최근 1년 주가 흐름 (시작=100)"
    )

    fig.update_layout(
        height=700,
        hovermode="x unified",
        legend_title="종목"
    )

    fig.update_xaxes(
        rangeslider_visible=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    returns = (
        (price_df.iloc[-1] / price_df.iloc[0] - 1)
        * 100
    ).round(2)

    result = pd.DataFrame({
        "종목": returns.index,
        "수익률(%)": returns.values
    })

    result = result.sort_values(
        "수익률(%)",
        ascending=False
    )

    st.subheader("🏆 수익률 랭킹")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    winner = result.iloc[0]

    st.success(
        f"🥇 1위: {winner['종목']} ({winner['수익률(%)']}%)"
    )
