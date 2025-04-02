import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 질문 리스트 및 평가 기준
questions = [
    ("네트 앞에서 빠르게 반응하고 셔틀을 컨트롤할 수 있는가?", "Front"),
    ("강한 클리어와 스매시를 활용하여 후위에서 공격을 주도할 수 있는가?", "Back"),
    ("순간적인 스텝 이동이 빠르고 네트에서 민첩하게 움직일 수 있는가?", "Front"),
    ("전위에서 헤어핀과 드롭샷을 정교하게 구사할 수 있는가?", "Front"),
    ("후위에서 스매시와 드라이브를 강하게 구사할 수 있는가?", "Back"),
    ("네트에서 상대의 공격을 빠르게 반응하여 받아낼 수 있는가?", "Front"),
    ("후위에서 디펜스를 안정적으로 수행할 수 있는가?", "Back"),
    ("전위에서 푸시와 드라이브로 빠른 속공 플레이를 할 수 있는가?", "Front"),
    ("상대의 움직임을 빠르게 파악하고 빈 공간을 공략하는 능력이 뛰어난가?", "Front"),
    ("랠리 중 적절한 타이밍에 후위에서 강한 공격을 구사할 수 있는가?", "Back"),
    ("공격적인 플레이보다 수비적으로 경기를 운영하는 것이 편한가?", "Back"),
    ("압박 상황에서도 침착하게 플레이할 수 있는가?", "Both"),
    ("경기 중 파트너와의 포지션을 자연스럽게 교대할 수 있는가?", "Both"),
    ("파트너의 스타일에 맞춰 유연하게 플레이할 수 있는가?", "Both"),
    ("경기 중 실수했을 때 파트너를 격려하며 긍정적인 분위기를 유지할 수 있는가?", "Both"),
]

# Streamlit UI
st.title("배드민턴 여자복식 전위 & 후위 포지션 적합성 평가")
st.write("아래 질문에 대해 1(전혀 아니다) ~ 5(매우 그렇다)로 점수를 입력하세요.")

# 점수 입력 받기
responses = []
for q, _ in questions:
    score = st.slider(q, 1, 5, 3)
    responses.append(score)

# 점수 계산
front_score = sum([responses[i] for i, (_, category) in enumerate(questions) if category in ["Front", "Both"]])
back_score = sum([responses[i] for i, (_, category) in enumerate(questions) if category in ["Back", "Both"]])

# 결과 출력
st.subheader("결과 분석")
st.write(f"**전위 플레이어(Front) 적합도 점수:** {front_score}")
st.write(f"**후위 플레이어(Back) 적합도 점수:** {back_score}")

if front_score > back_score:
    st.success("🎯 당신은 전위 플레이어(Front)에 더 적합합니다!")
elif back_score > front_score:
    st.success("🎯 당신은 후위 플레이어(Back)에 더 적합합니다!")
else:
    st.info("⚖️ 두 포지션에 모두 적합한 자질을 가지고 있습니다!")

# 시각화
fig, ax = plt.subplots()
categories = ["Front", "Back"]
scores = [front_score, back_score]
ax.bar(categories, scores, color=["pink", "purple"])
ax.set_ylabel("score")
ax.set_title("WD  Front vs Back TEST")

st.pyplot(fig)
