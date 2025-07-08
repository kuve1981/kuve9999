import streamlit as st
import random
from itertools import combinations
from collections import defaultdict, Counter

st.title("🏸 배드민턴 대진표 자동 생성기")

# -----------------------
# 1. 입력: 인원 및 1인당 경기 수
# -----------------------
st.sidebar.header("🎯 설정")

num_players = st.sidebar.number_input("전체 선수 수", min_value=4, max_value=40, value=12, step=2)
games_per_person = st.sidebar.slider("1인당 경기 수", min_value=1, max_value=4, value=2)

total_games = (num_players * games_per_person) // 4

st.sidebar.markdown(f"📌 총 경기 수 예상: **{total_games}게임**")

# -----------------------
# 2. 선수 자동 생성
# -----------------------

grades = ['a', 'b', 'c', 'd']
sexes = ['남', '여']

def generate_players(n):
    players = []
    for i in range(n):
        name = f"{sexes[i % 2]}{i+1}"
        gender = sexes[i % 2]
        grade = grades[i % len(grades)]
        players.append({'name': name, 'gender': gender, 'grade': grade})
    return players

players = generate_players(num_players)

st.subheader("👤 자동 생성된 선수 목록")
st.dataframe(players)

# -----------------------
# 3. 대진표 생성
# -----------------------

player_games = defaultdict(int)
used_combos = set()
matches = []

def team_score(team):
    grade_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    return abs(grade_map[team[0]['grade']] - grade_map[team[1]['grade']])

def match_score(t1, t2):
    return abs(team_score(t1) - team_score(t2))

def is_valid(team1, team2):
    names = {team1[0]['name'], team1[1]['name'], team2[0]['name'], team2[1]['name']}
    if len(names) < 4:
        return False
    if any(player_games[name] >= games_per_person for name in names):
        return False
    key = tuple(sorted(names))
    if key in used_combos:
        return False
    return True

def generate_matches(players, total_games):
    teams = list(combinations(players, 2))
    teams.sort(key=lambda x: team_score(x))
    while len(matches) < total_games:
        found = False
        for t1 in teams:
            for t2 in teams:
                if is_valid(t1, t2):
                    match = (t1, t2)
                    matches.append(match)
                    names = [p['name'] for p in t1 + t2]
                    for name in names:
                        player_games[name] += 1
                    used_combos.add(tuple(sorted(names)))
                    found = True
                    break
            if found:
                break
        if not found:
            break

generate_matches(players, total_games)

# -----------------------
# 4. 대진표 출력
# -----------------------
st.header("📋 생성된 대진표")

if not matches:
    st.warning("⚠️ 대진표를 생성할 수 없습니다. 인원 수를 늘리거나 경기 수를 줄여보세요.")
else:
    for i, (t1, t2) in enumerate(matches, 1):
        team1 = f"{t1[0]['name']}({t1[0]['grade']}) & {t1[1]['name']}({t1[1]['grade']})"
        team2 = f"{t2[0]['name']}({t2[0]['grade']}) & {t2[1]['name']}({t2[1]['grade']})"
        st.markdown(f"""**게임 {i}**  
{team1} 🆚 {team2}""")

# -----------------------
# 5. 개인별 경기 수 출력
# -----------------------
st.subheader("📊 개인별 경기 수")

for p in players:
    st.markdown(f"- {p['name']} : {player_games[p['name']]}경기")

