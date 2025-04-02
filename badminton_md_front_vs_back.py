import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 질문 리스트 및 평가 기준
questions = [
    ("스매시 파워가 강하고 후위에서 강한 공격을 지속적으로 할 수 있는가?", "Back"),
    ("네트 앞에서 빠른 반응 속도로 셔틀을 컨트롤할 수 있는가?", "Front"),
    ("순간적인 스텝 이동이 빠르고 민첩한가?", "Front"),
    ("강한 드라이브와 푸시를 활용한 공격적인 플레이를 선호하는가?", "Front"),
    ("전위에서 네트 드롭과 헤어핀을 정교하게 구사할 수 있는가?", "Front"),
    ("후위에서 클리어와 스매시를 적극적으로 활용할 수 있는가?", "Back"),
    ("점프 스매시를 구사할 수 있는가?", "Back"),
    ("네트에서 상대의 공격을 카운터하고 주도권을 잡는 플레이를 잘하는가?", "Front"),
    ("공격 기회에서 자연스럽게 전위와 후위를 교대할 수 있는가?", "Both"),
    ("랠리 중 적절한 타이밍에 네트 앞으로 전진할 수 있는가?", "Front"),
    ("후위에서의 수비적인 드라이브와 클리어를 안정적으로 할 수 있는가?", "Back"),
    ("상대의 플레이 스타일을 빠르게 분석하고 전략을 조정할 수 있는가?", "Both"),
    ("압박 상황에서도 침착하게 플레이할 수 있는가?", "Both"),
    ("파트너의 플레이 스타일에 맞춰 유연하게 적응할 수 있는가?", "Both"),
    ("경기 중 실수했을 때 파트너를 격려하며 긍정적인 분위기를 유지할 수 있는가?", "Both"),
]

# Streamlit UI
st.title("배드민턴 남자복식 전위 & 후위 포지션 적합성 평가")
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
ax.bar(categories, scores, color=["green", "red"])
ax.set_ylabel("score")
ax.set_title("MD  Front vs Back TEST")

st.pyplot(fig)
