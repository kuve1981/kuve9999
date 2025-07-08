import streamlit as st
import random
from itertools import combinations
from collections import defaultdict, Counter

st.title("🏸 급수 기반 배드민턴 대진표 생성기")

# -----------------------
# 1. 사용자 입력
# -----------------------

st.header("👥 선수 등록")

player_list = []

with st.form("player_form"):
    num_players = st.number_input("선수 인원 수", min_value=4, max_value=40, step=1)
    player_data = []
    
    st.markdown("**이름 / 성별 / 급수(a~d)**를 입력하세요")

    for i in range(int(num_players)):
        cols = st.columns([4, 2, 2])
        with cols[0]:
            name = st.text_input(f"이름 {i+1}", key=f"name_{i}")
        with cols[1]:
            gender = st.selectbox("성별", options=["남", "여"], key=f"gender_{i}")
        with cols[2]:
            grade = st.selectbox("급수", options=["a", "b", "c", "d"], key=f"grade_{i}")
        
        player_data.append({'name': name.strip(), 'gender': gender, 'grade': grade})

    per_person_game = st.slider("1인당 경기 수", min_value=1, max_value=4, value=2)
    submitted = st.form_submit_button("대진표 생성")

if submitted:
    # -----------------------
    # 2. 입력 유효성 검사
    # -----------------------
    valid_players = [p for p in player_data if p['name']]
    if len(valid_players) < 4:
        st.error("선수는 최소 4명 이상 입력해야 합니다.")
        st.stop()

    total_games_needed = (len(valid_players) * per_person_game) // 4
    st.markdown(f"✅ 총 {len(valid_players)}명 × {per_person_game}게임 = 총 {total_games_needed}게임 필요")

    # -----------------------
    # 3. 대진표 생성
    # -----------------------
    player_games = defaultdict(int)
    used_combinations = set()
    matches = []

    def team_balance_score(team):
        grade_weight = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        return abs(grade_weight[team[0]['grade']] - grade_weight[team[1]['grade']])

    def match_balance_score(t1, t2):
        return abs(team_balance_score(t1) - team_balance_score(t2))

    def get_team_combinations(players):
        return list(combinations(players, 2))

    # 전체 가능한 조합
    player_pool = valid_players.copy()
    random.shuffle(player_pool)

    all_teams = list(combinations(player_pool, 2))
    all_teams = [t for t in all_teams if t[0] != t[1]]
    all_teams.sort(key=lambda x: team_balance_score(x))  # 급수 가까운 팀 우선

    # 경기 생성
    for _ in range(total_games_needed):
        found = False
        for t1 in all_teams:
            if player_games[t1[0]['name']] >= per_person_game or player_games[t1[1]['name']] >= per_person_game:
                continue
            for t2 in all_teams:
                all_names = {t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}
                if len(all_names) < 4:
                    continue
                if any(player_games[name] >= per_person_game for name in all_names):
                    continue
                team_key = tuple(sorted(all_names))
                if team_key in used_combinations:
                    continue
                # 등록
                matches.append((t1, t2))
                for name in all_names:
                    player_games[name] += 1
                used_combinations.add(team_key)
                found = True
                break
            if found:
                break

    # -----------------------
    # 4. 결과 출력
    # -----------------------
    st.header("📋 생성된 대진표")
    if not matches:
        st.warning("⚠️ 충분한 조합을 만들 수 없습니다. 인원을 늘리거나 경기 수를 줄여주세요.")
    else:
        for i, (team1, team2) in enumerate(matches, 1):
            t1 = f"{team1[0]['name']} & {team1[1]['name']}"
            t2 = f"{team2[0]['name']} & {team2[1]['name']}"
            st.markdown(f"**게임 {i}**  
            {t1} 🆚 {t2}")

    # -----------------------
    # 5. 개인별 경기 수
    # -----------------------
    st.subheader("👤 개인별 경기 수")
    game_counter = Counter(player_games)
    for name, count in game_counter.items():
        st.markdown(f"- {name}: {count}경기")
