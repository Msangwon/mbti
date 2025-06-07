import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 생성 (가상의 데이터)
@st.cache_data
def generate_data():
    mbti_types = [
        "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]
    data = {
        'MBTI': mbti_types,
        '국어_성취도': [
            85, 90, 92, 88, 78, 82, 95, 87,
            75, 80, 93, 89, 83, 91, 94, 90
        ]
    }
    df = pd.DataFrame(data)
    return df

df = generate_data()

# 2. Streamlit 앱 구성
st.title("📚 MBTI별 국어 과목 성취도 분석기 📊")
st.write("가상의 데이터를 활용하여 MBTI 유형별 국어 과목 성취도를 시각화합니다. 아래에서 MBTI 유형을 선택해 보세요!")

# 3. MBTI 유형 선택 (스크롤)
st.sidebar.header("MBTI 유형 선택 🕵️‍♀️")
selected_mbti = st.sidebar.selectbox(
    "궁금한 MBTI 유형을 선택하세요:",
    options=['전체 보기'] + df['MBTI'].tolist() # '전체 보기' 옵션 추가
)

# 4. 선택된 MBTI에 따른 결과 표시
st.subheader(f"✨ {selected_mbti} 유형의 국어 성취도 결과")

if selected_mbti == '전체 보기':
    st.dataframe(df.set_index('MBTI')) # MBTI를 인덱스로 설정하여 깔끔하게 표시
    st.markdown("---")
    st.write("📈 **모든 MBTI 유형의 국어 성취도 현황입니다.**")
    # 전체 데이터에 대한 시각화 (막대 그래프)
    fig = px.bar(df, x='MBTI', y='국어_성취도',
                 title='📊 모든 MBTI 유형별 국어 과목 성취도',
                 labels={'MBTI': 'MBTI 유형', '국어_성취도': '국어 성취도 점수'},
                 color='국어_성취도',
                 color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig)

else:
    # 선택된 MBTI 유형의 데이터만 필터링
    filtered_df = df[df['MBTI'] == selected_mbti]
    st.dataframe(filtered_df.set_index('MBTI')) # 선택된 데이터만 표로 보여줌
    st.markdown("---")
    st.write(f"🌟 **{selected_mbti} 유형의 국어 성취도 점수는 {filtered_df['국어_성취도'].iloc[0]}점 입니다.**")
    # 선택된 MBTI에 대한 파이 차트 (해당 유형 하나만 강조)
    fig = px.pie(df, names='MBTI', values='국어_성취도',
                 title=f'pie chart of 국어 성취도 for all MBTI types',
                 hole=0.3)
    # 선택된 MBTI 조각에 특별한 색상 적용 (선택적)
    # fig.update_traces(marker=dict(colors=[
    #     'blue' if m == selected_mbti else 'lightgrey' for m in df['MBTI']
    # ]))
    st.plotly_chart(fig)

st.markdown(
    """
    ---
    **참고:**
    * 이 데이터는 **가상**으로 생성된 것이며, 실제 MBTI와 학업 성취도 간의 연관성을 나타내지 않습니다.
    * MBTI는 개인의 선호를 나타내는 지표이며, 학업 능력을 직접적으로 측정하는 도구가 아닙니다.
    """
)
