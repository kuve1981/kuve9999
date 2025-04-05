import streamlit as st
import random

# 로또 번호 생성 함수
def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

# 당첨 여부 확인 함수
def check_results(user_numbers, winning_numbers, bonus_number):
    matched = set(user_numbers) & set(winning_numbers)
    match_count = len(matched)
    bonus_matched = bonus_number in user_numbers

    if match_count == 6:
        return "1등! 🎉"
    elif match_count == 5 and bonus_matched:
        return "2등! 🎉"
    elif match_count == 5:
        return "3등!"
    elif match_count == 4:
        return "4등!"
    elif match_count == 3:
        return "5등!"
    else:
        return "꽝! 다음 기회에!"

# Streamlit UI
st.title("로또 계산기 🎰")

# 사용자 번호 입력
user_numbers = st.text_input("6개의 숫자를 입력하세요 (쉼표로 구분)", "")

if user_numbers:
    try:
        user_numbers = list(map(int, user_numbers.split(',')))
        if len(user_numbers) != 6 or any(n < 1 or n > 45 for n in user_numbers):
            st.error("1~45 사이의 숫자 6개를 입력하세요.")
        else:
            # 로또 당첨 번호 생성
            winning_numbers = generate_lotto_numbers()
            bonus_number = random.choice([n for n in range(1, 46) if n not in winning_numbers])

            # 결과 확인
            result = check_results(user_numbers, winning_numbers, bonus_number)

            # 당첨 번호 출력
            st.write(f"당첨 번호: {winning_numbers}, 보너스 번호: {bonus_number}")
            st.subheader(f"결과: {result}")
    except ValueError:
        st.error("숫자를 올바르게 입력하세요.")

