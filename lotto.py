import streamlit as st
import random
import time

st.set_page_config(page_title="로또 번호 생성기", page_icon="🎰")
st.title("🎰 로또 번호 생성기")

st.write("버튼을 누르면 슬롯머신처럼 번호가 하나씩 나타납니다!")

if st.button("번호 생성하기"):
    lotto_numbers = sorted(random.sample(range(1, 46), 6))
    displayed_numbers = []

    number_placeholder = st.empty()

    for num in lotto_numbers:
        # 슬롯머신 느낌: 중간 숫자들을 빠르게 보여주기
        for _ in range(10):
            temp = random.randint(1, 45)
            number_placeholder.markdown(f"<h1 style='text-align: center; color: gray;'>{temp}</h1>", unsafe_allow_html=True)
            time.sleep(0.05)

        # 진짜 숫자 보여주기
        displayed_numbers.append(num)
        number_placeholder.markdown(
            f"<h1 style='text-align: center; color: green;'>{'  '.join(str(n) for n in displayed_numbers)}</h1>",
            unsafe_allow_html=True
        )
        time.sleep(0.3)

    st.success("번호 생성 완료! 🎉")
