import streamlit as st
from itertools import combinations, product
from collections import defaultdict
import math

st.title("🏸 배드민턴 대진표 생성기 (급수 밸런스 + 중복 방지)")

# 사용자 입력
st.sidebar.header("🛠️ 설정")
num_players = st.sidebar.number_input("총 참가 인원 수", min_value=4, max_value=40, value=12, step=1)
games_per_player = st.sidebar.slider("1인당 경기 수", min_value=1, max_value=10, value=2)

# 급수 매핑
grade_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

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
    players = [p for p in players if p['name']]
    if len(players) < 4:
        st.error("⚠️ 최소 4명 이상의 유효한 선수가 필요합니다.")
        st.stop()

    st.success(f"✅ 유효 선수 수: {len(players)}명")

    player_games = defaultdict(int)
    matches = []
    used_teams = set()
    used_game_combos = set()

    # 점수 변환
    def grade_score(p):
        return grade_map[p['grade']]

    # 평균 급수 점수
    def team_score(team):
        return sum(grade_score(p) for p in team) / len(team)

    # 팀 밸런스 차이 계산
    def match_score(t1, t2):
        return abs(team_score(t1) - team_score(t2))

    # 팀 중복 여부 확인
    def team_key(team):
        return tuple(sorted(p['name'] for p in team))

    def match_key(t1, t2):
        names = sorted([p['name'] for p in t1 + t2])
        return tuple(names)

    # 사용 가능한 팀 구성만 필터링
    def filter_valid_teams(teams):
        return [t for t in teams if team_key(t) not in used_teams]

    def try_match(gender=None, allow_mixed=False):
        if gender:
            group = [p for p in players if p['gender'] == gender and player_games[p['name']] < games_per_player]
        elif allow_mixed:
            group = [p for p in players if player_games[p['name']] < games_per_player]
        else:
            return False

        if len(group) < 4:
            return False

        teams = list(combinations(group, 2))
        teams = filter_valid_teams(teams)

        match_candidates = []
        for t1, t2 in combinations(teams, 2):
            names = {p['name'] for p in t1 + t2}
            if len(names) < 4:
                continue
            if any(player_games[n] >= games_per_player for n in names):
                continue
            if match_key(t1, t2) in used_game_combos:
                continue
            score = match_score(t1, t2)
            match_candidates.append((score, t1, t2))

        match_candidates.sort(key=lambda x: x[0])  # 급수 평균 차이 적은 조합부터

        for score, t1, t2 in match_candidates:
            names = {p['name'] for p in t1 + t2}
            for n in names:
                player_games[n] += 1
            used_teams.add(team_key(t1))
            used_teams.add(team_key(t2))
            used_game_combos.add(match_key(t1, t2))
            match_type = f"{gender}복식" if gender else "혼합복식"
            matches.append((t1, t2, match_type))
            return True
        return False

    # 반복: 모든 사람이 games_per_player 도달할 때까지
    while any(player_games[p['name']] < games_per_player for p in players):
        if not try_match(gender="남"):
            if not try_match(gender="여"):
                if not try_match(allow_mixed=True):
                    st.warning("⚠️ 더 이상 구성할 수 있는 팀이 없습니다. 일부 선수는 경기 수를 채우지 못했을 수 있습니다.")
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
