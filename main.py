import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 생성 (가상의 데이터)
# @st.cache_data 데코레이터는 데이터 로드 및 처리 시간을 최적화하여 앱 성능을 향상시킵니다.
@st.cache_data
def generate_data():
    mbti_types = [
        "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]
    # 각 MBTI 유형에 대한 가상의 국어 성취도 점수 (0-100)
    # 이 데이터는 실제 연구 결과가 아니므로, 재미로만 활용해 주세요.
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
# '전체 보기' 옵션을 가장 위에 추가하고, MBTI 유형은 정렬하여 보여줍니다.
selected_mbti = st.sidebar.selectbox(
    "궁금한 MBTI 유형을 선택하세요:",
    options=['전체 보기'] + sorted(df['MBTI'].tolist())
)

# 4. 선택된 MBTI에 따른 결과 표시
st.subheader(f"✨ **{selected_mbti}** 유형의 국어 성취도 결과")

if selected_mbti == '전체 보기':
    # 모든 데이터를 표로 표시합니다. MBTI를 인덱스로 설정하여 가독성을 높입니다.
    st.dataframe(df.set_index('MBTI'))
    st.markdown("---")
    st.write("📈 **모든 MBTI 유형의 국어 성취도 현황입니다.**")

    # 모든 MBTI 유형에 대한 막대 그래프를 생성합니다.
    fig_bar = px.bar(df, x='MBTI', y='국어_성취도',
                     title='📊 모든 MBTI 유형별 국어 과목 성취도',
                     labels={'MBTI': 'MBTI 유형', '국어_성취도': '국어 성취도 점수'},
                     color='국어_성취도', # 성취도 점수에 따라 막대 색상이 변합니다.
                     color_continuous_scale=px.colors.sequential.Plasma) # 색상 스케일 설정
    st.plotly_chart(fig_bar)

else:
    # 선택된 MBTI 유형의 데이터만 필터링하여 표로 표시합니다.
    filtered_df = df[df['MBTI'] == selected_mbti]
    st.dataframe(filtered_df.set_index('MBTI'))
    st.markdown("---")
    # 선택된 유형의 국어 성취도 점수를 텍스트로 강조하여 보여줍니다.
    st.write(f"🌟 **{selected_mbti}** 유형의 국어 성취도 점수는 **{filtered_df['국어_성취도'].iloc[0]}점** 입니다.")

    # 전체 MBTI 유형에 대한 파이 차트를 생성하여, 선택된 유형을 강조합니다.
    fig_pie = px.pie(df, names='MBTI', values='국어_성취도',
                     title=f'pie chart of 전체 MBTI 유형별 국어 성취도 (선택: {selected_mbti})',
                     hole=0.3) # 도넛 형태로 표시
    # 선택된 MBTI 조각의 색상을 다르게 하여 시각적으로 강조합니다.
    colors = [
        'gold' if mbti == selected_mbti else 'lightgrey' for mbti in df['MBTI']
    ]
    fig_pie.update_traces(marker=dict(colors=colors))
    st.plotly_chart(fig_pie)

st.markdown(
    """
    ---
    **참고:**
    * 이 데이터는 **가상**으로 생성된 것이며, 실제 MBTI와 학업 성취도 간의 통계적인 연관성을 나타내지 않습니다.
    * MBTI는 개인의 선호를 나타내는 지표이며, 학업 능력을 직접적으로 측정하는 도구가 아닙니다.
    """
)
