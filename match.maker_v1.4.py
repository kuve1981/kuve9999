import streamlit as st
from itertools import combinations
from collections import defaultdict

st.title("🏸 배드민턴 대진표 생성기 (밸런스 + 최소 경기 수 보장)")

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
    used_match_combos = set()

    def grade_score(p):
        return grade_map[p['grade']]

    def team_score(team):
        return sum(grade_score(p) for p in team) / 2

    def match_score(t1, t2):
        return abs(team_score(t1) - team_score(t2))

    def team_key(team):
        return tuple(sorted(p['name'] for p in team))

    def match_key(t1, t2):
        return tuple(sorted(p['name'] for p in t1 + t2))

    def find_match(allow_overflow=False, allow_mixed=False):
        if allow_mixed:
            group = players
        else:
            group = [p for p in players if player_games[p['name']] < games_per_player or allow_overflow]

        male = [p for p in group if p['gender'] == '남']
        female = [p for p in group if p['gender'] == '여']

        for label, group_players in [('남복식', male), ('여복식', female)]:
            if len(group_players) < 4:
                continue
            teams = list(combinations(group_players, 2))
            for t1 in teams:
                for t2 in teams:
                    names = set(p['name'] for p in t1 + t2)
                    if len(names) < 4:
                        continue
                    if match_key(t1, t2) in used_match_combos:
                        continue
                    matches.append((t1, t2, label))
                    used_teams.add(team_key(t1))
                    used_teams.add(team_key(t2))
                    used_match_combos.add(match_key(t1, t2))
                    for p in t1 + t2:
                        player_games[p['name']] += 1
                    return True

        # 혼합 복식
        if allow_mixed:
            pairs = [(m, f) for m in male for f in female if m['name'] != f['name']]
            for t1 in pairs:
                for t2 in pairs:
                    names = set(p['name'] for p in t1 + t2)
                    if len(names) < 4:
                        continue
                    if match_key(t1, t2) in used_match_combos:
                        continue
                    matches.append((t1, t2, '혼합복식'))
                    used_teams.add(team_key(t1))
                    used_teams.add(team_key(t2))
                    used_match_combos.add(match_key(t1, t2))
                    for p in t1 + t2:
                        player_games[p['name']] += 1
                    return True
        return False

    # 단계 1: 기본 조건으로 매칭 시도 (모든 사람 최소 경기 수까지)
    while any(player_games[p['name']] < games_per_player for p in players):
        matched = find_match(allow_overflow=False, allow_mixed=False)
        if not matched:
            matched = find_match(allow_overflow=False, allow_mixed=True)
            if not matched:
                break  # 기본 조합으로는 더 이상 불가능

    # 단계 2: 목표 도달 못한 사람 위해 오버플로우 허용
    if any(player_games[p['name']] < games_per_player for p in players):
        while any(player_games[p['name']] < games_per_player for p in players):
            matched = find_match(allow_overflow=True, allow_mixed=True)
            if not matched:
                break

    # 출력
    st.header("📋 생성된 대진표")
    if not matches:
        st.warning("❗ 대진표를 생성할 수 없습니다.")
    else:
        for i, (t1, t2, mtype) in enumerate(matches, 1):
            team1 = f"{t1[0]['name']}({t1[0]['grade']}) & {t1[1]['name']}({t1[1]['grade']})"
            team2 = f"{t2[0]['name']}({t2[0]['grade']}) & {t2[1]['name']}({t2[1]['grade']})"
            st.markdown(f"""**게임 {i} - {mtype}**
{team1} 🆚 {team2}""")

    # 개인별 경기 수
    st.subheader("👤 개인별 경기 수")
    for p in players:
        st.markdown(f"- {p['name']} : {player_games[p['name']]}경기")
