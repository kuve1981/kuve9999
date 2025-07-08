import streamlit as st
from itertools import combinations
from collections import defaultdict
import random

st.title("🏸 배드민턴 대진표 생성기 (급수 + 성별 기반)")

# 사용자 입력
st.sidebar.header("🛠️ 설정")

num_players = st.sidebar.number_input("총 참가 인원 수", min_value=4, max_value=40, value=12, step=1)
games_per_player = st.sidebar.slider("1인당 경기 수", min_value=1, max_value=4, value=2)

# 총 경기 수 계산
total_matches_needed = (num_players * games_per_player) // 4
st.sidebar.markdown(f"🧮 예상 총 경기 수: **{total_matches_needed}게임**")

# 선수 입력
st.header("👤 선수 정보 입력")
players = []

with st.form("player_form"):
    for i in range(num_players):
        cols = st.columns([4, 2, 2])
        name = cols[0].text_input(f"이름 {i+1}", key=f"name_{i}")
        gender = cols[1].selectbox("성별", ["남", "여"], key=f"gender_{i}")
        grade = cols[2].selectbox("급수", ["A", "B", "C", "D"], key=f"grade_{i}")
        players.append({'name': name.strip(), 'gender': gender, 'grade': grade})
    submitted = st.form_submit_button("🎮 대진표 생성")

if submitted:
    players = [p for p in players if p['name']]  # 이름 있는 선수만 포함
    if len(players) < 4:
        st.error("⚠️ 최소 4명 이상의 유효한 선수가 필요합니다.")
        st.stop()

    st.success(f"✅ 유효 선수 수: {len(players)}명")

    player_games = defaultdict(int)
    used_combinations = set()
    matches = []

    grade_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    def grade_diff(p1, p2):
        return abs(grade_order[p1['grade']] - grade_order[p2['grade']])

    def team_key(team):
        return tuple(sorted(p['name'] for p in team))

    def is_valid_match(t1, t2):
        names = {p['name'] for p in t1 + t2}
        if len(names) < 4:
            return False
        if any(player_games[name] >= games_per_player for name in names):
            return False
        if tuple(sorted(names)) in used_combinations:
            return False
        return True

    def add_match(t1, t2, match_type):
        names = [p['name'] for p in t1 + t2]
        for name in names:
            player_games[name] += 1
        used_combinations.add(tuple(sorted(names)))
        matches.append((t1, t2, match_type))

    def create_matches_by_gender(gender):
        group = [p for p in players if p['gender'] == gender and player_games[p['name']] < games_per_player]
        team_pairs = list(combinations(group, 2))
        team_pairs.sort(key=lambda t: grade_diff(t[0], t[1]))  # 급수 차이 최소 우선
        for t1 in team_pairs:
            for t2 in team_pairs:
                if is_valid_match(t1, t2):
                    add_match(t1, t2, f"{gender}복식")
                    return True
        return False

    def create_mixed_matches():
        males = [p for p in players if p['gender'] == '남' and player_games[p['name']] < games_per_player]
        females = [p for p in players if p['gender'] == '여' and player_games[p['name']] < games_per_player]
        pairs_male = [(m, f) for m in males for f in females if m['name'] != f['name']]
        pairs_male.sort(key=lambda t: grade_diff(t[0], t[1]))
        for t1 in pairs_male:
            for t2 in pairs_male:
                if len({t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}) < 4:
                    continue
                if is_valid_match(t1, t2):
                    add_match(t1, t2, "혼합복식")
                    return True
        return False

    # 경기 생성 루프
    while len(matches) < total_matches_needed:
        made_match = create_matches_by_gender("남")
        if not made_match:
            made_match = create_matches_by_gender("여")
        if not made_match:
            made_match = create_mixed_matches()
        if not made_match:
            st.warning("⚠️ 더 이상 유효한 조합이 없습니다. 경기 수가 부족할 수 있습니다.")
            break

    # 출력
    st.header("📋 생성된 대진표")
    for i, (t1, t2, mtype) in enumerate(matches, 1):
        team1 = f"{t1[0]['name']}({t1[0]['grade']}) & {t1[1]['name']}({t1[1]['grade']})"
        team2 = f"{t2[0]['name']}({t2[0]['grade']}) & {t2[1]['name']}({t2[1]['grade']})"
        st.markdown(f"""**게임 {i} - {mtype}**
{team1} 🆚 {team2}""")

    st.subheader("👤 개인별 경기 수")
    for p in players:
        st.markdown(f"- {p['name']} : {player_games[p['name']]}경기")
