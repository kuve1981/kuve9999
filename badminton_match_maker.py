import streamlit as st
import random
from itertools import combinations
from collections import defaultdict, Counter

st.title("🏸 배드민턴 대진표 생성기")

st.markdown("""
이 앱은 급수(a~d)와 성별(남/여)에 따라 등록된 선수 정보를 기반으로, 
한 사람당 N게임씩 참여하는 대진표를 생성합니다.
""")

# -----------------------
# 1. 선수 등록
# -----------------------
st.header("👤 선수 등록")

num_players = st.number_input("등록할 선수 수", min_value=4, max_value=40, value=12, step=1)

players = []
with st.form("player_form"):
    for i in range(num_players):
        cols = st.columns([3, 2, 2])
        with cols[0]:
            name = st.text_input(f"이름 {i+1}", key=f"name_{i}")
        with cols[1]:
            gender = st.selectbox("성별", ["남", "여"], key=f"gender_{i}")
        with cols[2]:
            grade = st.selectbox("급수", ["a", "b", "c", "d"], key=f"grade_{i}")

        if name:
            players.append({"name": name.strip(), "gender": gender, "grade": grade})

    games_per_person = st.slider("1인당 경기 수", min_value=1, max_value=4, value=2)
    submitted = st.form_submit_button("✅ 대진표 생성")

if submitted:
    total_games = (len(players) * games_per_person) // 4
    st.markdown(f"**총 {len(players)}명 × {games_per_person}게임 ÷ 4 = {total_games}경기 필요**")

    player_games = defaultdict(int)
    used_combos = set()
    matches = []

    def team_score(team):
        grade_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        return abs(grade_map[team[0]['grade']] - grade_map[team[1]['grade']])

    def match_score(t1, t2):
        return abs(team_score(t1) - team_score(t2))

    def is_valid(t1, t2):
        names = {t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}
        if len(names) < 4:
            return False
        if any(player_games[name] >= games_per_person for name in names):
            return False
        key = tuple(sorted(names))
        if key in used_combos:
            return False
        return True

    # 팀 조합 먼저 급수로 정렬
    teams = list(combinations(players, 2))
    teams.sort(key=lambda x: team_score(x))

    while len(matches) < total_games:
        found = False
        for t1 in teams:
            for t2 in teams:
                if is_valid(t1, t2):
                    matches.append((t1, t2))
                    for p in t1 + t2:
                        player_games[p['name']] += 1
                    used_combos.add(tuple(sorted([p['name'] for p in t1 + t2])))
                    found = True
                    break
            if found:
                break
        if not found:
            break

    # -----------------------
    # 출력
    # -----------------------
    st.header("📋 대진표 결과")
    if not matches:
        st.warning("⚠️ 대진표를 만들 수 없습니다. 인원을 늘리거나 경기 수를 줄여보세요.")
    else:
        for i, (t1, t2) in enumerate(matches, 1):
            team1 = f"{t1[0]['name']}({t1[0]['grade']}) & {t1[1]['name']}({t1[1]['grade']})"
            team2 = f"{t2[0]['name']}({t2[0]['grade']}) & {t2[1]['name']}({t2[1]['grade']})"
            st.markdown(f"""**게임 {i}**  
{team1} 🆚 {team2}""")

        st.subheader("👤 개인별 경기 수")
        for p in players:
            st.markdown(f"- {p['name']} : {player_games[p['name']]}경기")
