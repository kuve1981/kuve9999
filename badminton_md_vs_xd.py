import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 질문 리스트 및 평가 기준
questions = [
    ("강한 스매시를 지속적으로 구사하며 공격을 주도할 수 있는가?", "MD"),
    ("후위에서 빠른 풋워크로 위치를 잡고 강력한 공격을 이어갈 수 있는가?", "XD"),
    ("후위에서 파워 있는 공격과 수비를 안정적으로 수행할 수 있는가?", "MD"),
    ("후위에서 강한 스매시와 각도 있는 공격을 구사할 수 있는가?", "MD"),
    ("혼합복식에서 여성 파트너가 전위에서 플레이할 때, 후위에서 공격적인 플레이를 할 수 있는가?", "XD"),
    ("상대의 수비를 흔드는 예리한 드롭샷을 구사할 수 있는가?", "Both"),
    ("빠른 랠리에서 상대의 공격을 받아넘기고 반격하는 능력이 뛰어난가?", "Both"),
    ("혼합복식에서 파트너가 상대의 공격을 버틸 수 있도록 안정적인 샷을 구사할 수 있는가?", "XD"),
    ("공격적인 플레이를 지속하면서도 경기 운영을 조절할 수 있는가?", "Both"),
    ("혼합복식에서 후위에서의 공격뿐만 아니라 전위에서의 유연한 움직임도 가능하다고 생각하는가?", "XD"),
    ("복식에서 빠른 포지션 전환과 파트너와의 협업을 원활하게 할 수 있는가?", "Both"),
    ("파트너가 실수했을 때 침착하게 경기를 운영할 수 있는가?", "Both"),
    ("혼합복식에서 여성 파트너를 배려하고 리드하는 역할을 수행할 수 있는가?", "XD"),
    ("랠리 중 파트너와의 거리와 위치를 정확하게 조정할 수 있는가?", "Both"),
    ("복식 경기에서 파트너의 스타일에 따라 자신의 플레이 방식을 조절할 수 있는가?", "Both"),
]

# Streamlit UI
st.title("배드민턴 남자복식 vs 혼합복식 적합성 평가")
st.write("아래 질문에 대해 1(전혀 아니다) ~ 5(매우 그렇다)로 점수를 입력하세요.")

# 점수 입력 받기
responses = []
for q, _ in questions:
    score = st.slider(q, 1, 5, 3)
    responses.append(score)

# 점수 계산
md_score = sum([responses[i] for i, (_, category) in enumerate(questions) if category in ["MD", "Both"]])
xd_score = sum([responses[i] for i, (_, category) in enumerate(questions) if category in ["XD", "Both"]])

# 결과 출력
st.subheader("결과 분석")
st.write(f"**남자복식(MD) 적합도 점수:** {md_score}")
st.write(f"**혼합복식(XD) 적합도 점수:** {xd_score}")

if md_score > xd_score:
    st.success("🎯 당신은 남자복식(MD)에 더 적합합니다!")
elif xd_score > md_score:
    st.success("🎯 당신은 혼합복식(XD)에 더 적합합니다!")
else:
    st.info("⚖️ 두 종목에 모두 적합한 자질을 가지고 있습니다!")

# 시각화
fig, ax = plt.subplots()
categories = ["MD", "XD"]
scores = [md_score, xd_score]
ax.bar(categories, scores, color=["blue", "orange"])
ax.set_ylabel("score")
ax.set_title("MD vs XD TEST")

st.pyplot(fig)
