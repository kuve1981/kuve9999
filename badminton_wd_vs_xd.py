import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 질문 리스트 및 평가 기준
questions = [
    ("네트 앞에서 빠르게 반응하고 셔틀을 컨트롤할 수 있는가?", "XD"),
    ("장기적인 랠리를 견딜 수 있는 체력과 지구력이 있는가?", "WD"),
    ("순간적인 스텝 이동이 빠르고 민첩한가?", "XD"),
    ("강한 드라이브와 푸시를 활용한 공격적인 플레이를 선호하는가?", "WD"),
    ("전위에서 네트 드롭과 헤어핀을 정교하게 구사할 수 있는가?", "XD"),
    ("후위에서 클리어와 스매시를 적극적으로 활용할 수 있는가?", "WD"),
    ("상대의 움직임을 빠르게 읽고 빈 공간을 공략하는 능력이 뛰어난가?", "XD"),
    ("수비적인 랠리 운영보다는 공격적으로 경기를 풀어가는 편인가?", "WD"),
    ("경기 중 파트너와의 역할 분담을 빠르게 이해하고 수행할 수 있는가?", "XD"),
    ("압박 상황에서도 침착하게 플레이할 수 있는가?", "Both"),
    ("긴 랠리에서도 꾸준히 집중력을 유지할 수 있는가?", "WD"),
    ("파트너와 빠르게 의사소통하고 협력할 수 있는가?", "XD"),
    ("게임 중 파트너의 플레이 스타일에 맞춰 유연하게 적응할 수 있는가?", "XD"),
    ("상대적으로 후위보다는 전위에서 플레이하는 것을 선호하는가?", "XD"),
    ("경기 중 실수했을 때 파트너를 격려하며 긍정적인 분위기를 유지할 수 있는가?", "XD"),
]

# Streamlit UI
st.title("배드민턴 여자복식 & 혼합복식 적합성 평가")
st.write("아래 질문에 대해 1(전혀 아니다) ~ 5(매우 그렇다)로 점수를 입력하세요.")

# 점수 입력 받기
responses = []
for q, _ in questions:
    score = st.slider(q, 1, 5, 3)
    responses.append(score)

# 점수 계산
wd_score = sum([responses[i] for i, (_, category) in enumerate(questions) if category in ["WD", "Both"]])
xd_score = sum([responses[i] for i, (_, category) in enumerate(questions) if category in ["XD", "Both"]])

# 결과 출력
st.subheader("결과 분석")
st.write(f"**여자복식(WD) 적합도 점수:** {wd_score}")
st.write(f"**혼합복식(XD) 적합도 점수:** {xd_score}")

if wd_score > xd_score:
    st.success("🎯 당신은 여자복식(WD)에 더 적합합니다!")
elif xd_score > wd_score:
    st.success("🎯 당신은 혼합복식(XD)에 더 적합합니다!")
else:
    st.info("⚖️ 두 종목에 모두 적합한 자질을 가지고 있습니다!")

# 시각화
fig, ax = plt.subplots()
categories = ["WD", "XD"]
scores = [wd_score, xd_score]
ax.bar(categories, scores, color=["purple", "orange"])
ax.set_ylabel("score")
ax.set_title("MD vs XD TEST")

st.pyplot(fig)
