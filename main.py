import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 생성 (가상의 데이터)
# @st.cache_data를 사용하여 데이터 로드 시간을 최적화합니다.
# 이 데코레이터는 Streamlit 1.18.0 버전부터 도입되었으며, 이전 버전에서는 @st.cache로 사용되었습니다.
# Python 3.10 환경에서는 최신 Streamlit 사용을 권장합니다.
@st.cache_data
def generate_data():
    mbti_types = [
        "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]
    # 각 MBTI 유형에 대한 가상의 국어 성취도 점수 (0-100)
    # 실제 데이터가 아니므로 참고용입니다.
    data = {
        'MBTI': mbti_types,
        '국어_성취도': [
            85, 90, 92, 88, 78, 82, 95, 87,
            75, 80, 93, 89, 83, 91, 94, 90
        ]
    }
    df = pd.DataFrame(data)
    return df

# 데이터 로드
df = generate_data()

# 2. Streamlit 앱 구성
st.title("📚 MBTI별 국어 과목 성취도 분석기 📊")
st.write("가상의 데이터를 활용하여 MBTI 유형별 국어 과목 성취도를 시각화합니다. 아래에서 MBTI 유형을 선택해 보세요!")

# 3. MBTI 유형 선택 (스크롤)
st.sidebar.header("MBTI 유형 선택 🕵️‍♀️")
# '전체 보기' 옵션을 가장 위에 추가합니다.
selected_mbti = st.sidebar.selectbox(
    "궁금한 MBTI 유형을 선택하세요:",
    options=['전체 보기'] + sorted(df['MBTI'].tolist()) # MBTI 유형을 정렬하여 보여줍니다.
)

# 4. 선택된 MBTI에 따른 결과 표시
st.subheader(f"✨ **{selected_mbti}** 유형의 국어 성취도 결과")

if selected_mbti == '전체 보기':
    # 모든 데이터를 표로 표시
    st.dataframe(df.set_index('MBTI'))
    st.markdown("---")
    st.write("📈 **모든 MBTI 유형의 국어 성취도 현황입니다.**")

    # 모든 MBTI 유형에 대한 막대 그래프
    fig_bar = px.bar(df, x='MBTI', y='국어_성취도',
                     title='📊 모든 MBTI 유형별 국어 과목 성취도',
                     labels={'MBTI': 'MBTI 유형', '국어_성취도': '국어 성취도 점수'},
                     color='국어_성취도', # 성취도 점수에 따라 색상 변화
                     color_continuous_scale=px.colors.sequential.Plasma) # 색상 스케일
    st.plotly_chart(fig_bar)

else:
    # 선택된 MBTI 유형의 데이터만 필터링하여 표로 표시
    filtered_df = df[df['MBTI'] == selected_mbti]
    st.dataframe(filtered_df.set_index('MBTI'))
    st.markdown("---")
    # 선택된 유형의 성취도 점수를 명확히 표시
    st.write(f"🌟 **{selected_mbti}** 유형의 국어 성취도 점수는 **{filtered_df['국어_성취도'].iloc[0]}점** 입니다.")

    # 전체 MBTI 유형에 대한 파이 차트 (선택된 유형을 강조)
    fig_pie = px.pie(df, names='MBTI', values='국어_성취도',
                     title=f'pie chart of 전체 MBTI 유형별 국어 성취도 (선택: {selected_mbti})',
                     hole=0.3) # 도넛 형태로 표시
    # 선택된 MBTI 조각의 색상을 다르게 하여 강조합니다.
    # update_traces를 사용하여 파이 차트의 색상을 동적으로 변경
    colors = [
        'gold' if mbti == selected_mbti else 'lightgrey' for mbti in df['MBTI']
    ]
    fig_pie.update_traces(marker=dict(colors=colors))
    st.plotly_chart(fig_pie)

st.markdown(
    """
    ---
    **참고:**
    * 이 데이터는 **가상**으로 생성된 것이며, 실제 MBTI와 학업 성취도 간의 연관성을 나타내지 않습니다.
    * MBTI는 개인의 선호를 나타내는 지표이며, 학업 능력을 직접적으로 측정하는 도구가 아닙니다.
    """
)
