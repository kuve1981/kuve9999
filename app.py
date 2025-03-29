import streamlit as st
import calendar

# 대한민국 공휴일 데이터 (년도별로 다를 수 있음)
public_holidays = {
    2024: 16,
    2025: 16,
    2026: 15,  # 예제 데이터 (실제 공휴일 수는 확인 필요)
}

def is_leap_year(year):
    """윤년 판별 함수"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def calculate_holidays(year):
    """해당 년도의 총 휴일 수와 퍼센트 계산"""
    total_days = 366 if is_leap_year(year) else 365
    weekends = sum(1 for month in range(1, 13) for day in range(1, calendar.monthrange(year, month)[1] + 1) if calendar.weekday(year, month, day) in [5, 6])
    
    holidays = public_holidays.get(year, 16)  # 기본값 16일
    total_holidays = weekends + holidays
    percentage = (total_holidays / total_days) * 100

    return total_holidays, percentage

# Streamlit UI
st.title("📅 연도별 휴일 계산기")
st.write("입력한 연도의 주말과 공휴일을 포함한 총 휴일 수를 계산합니다.")

year = st.number_input("연도를 입력하세요:", min_value=2000, max_value=2100, value=2025, step=1)

if st.button("계산하기"):
    holidays, percentage = calculate_holidays(year)
    st.success(f"🗓️ {year}년의 총 휴일 수: **{holidays}일**")
    st.info(f"📊 휴일 비율: **{percentage:.2f}%**")

st.write("✅ 대한민국 기준으로 계산됩니다.")
