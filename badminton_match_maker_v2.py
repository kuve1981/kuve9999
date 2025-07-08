import streamlit as st
import random
from itertools import combinations
from collections import defaultdict, Counter

st.title("🏸 배드민턴 대진표 생성기 (급수+성별 기반)")

# ---------------------------------------
# 1. 사용자 입력
# ---------------------------------------
with st.form("player_form"):
    st.subheader("👤 선수 정보 입력")

    num_players = st.number_input("총 참가 인원 수", min_value=4, max_value=40, value=12, step=1)
    player_list = []

    for i in range(num_players):
        cols = st.columns([4, 2, 2])
        name = cols[0].text_input(f"이름 {i+1}", key=f"name_{i}")
        gender = cols[1].selectbox("성별", ["남", "여"], key=f"gender_{i}")
        grade = cols[2].selectbox("급수", ["A", "B", "C", "D"], key=f"grade_{i}")
        if name.strip():
            player_list.append({'name': name.strip(), 'gender': gender, 'grade': grade})

    games_per_person = st.slider("1인당 경기 수", min_value=1, max_value=4, value=2)
    submitted = st.form_submit_button("📋 대진표 생성")

# ---------------------------------------
# 2. 대진표 생성
# ---------------------------------------
if submitted:
    if len(player_list) < 4:
        st.error("⚠️ 최소 4명 이상의 선수가 필요합니다.")
        st.stop()

    total_games = (len(player_list) * games_per_person) // 4
    st.success(f"🎯 총 경기 수: {total_games} (1인당 {games_per_person}게임 기준)")

    player_games = defaultdict(int)
    used_pairs = set()
    matches = []

    # 급수 순서
    grade_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    # 성별별 급수 정렬
    def get_grouped_players(players):
        grouped = defaultdict(list)
        for p in players:
            key = (p['gender'], p['grade'])
            grouped[key].append(p)
        return grouped

    def make_team_combinations(group):
        return list(combinations(group, 2))

    def grade_diff(p1, p2):
        return abs(grade_order[p1['grade']] - grade_order[p2['grade']])

    def team_balance_score(t1, t2):
        return abs(grade_diff(*t1) - grade_diff(*t2))

    def is_usable(names):
        return all(player_games[n] < games_per_person for n in names) and tuple(sorted(names)) not in used_pairs

    # 게임 구성 함수
    def generate_matches(players, total_games):
        grouped = get_grouped_players(players)
        male_players = [p for p in players if p['gender'] == '남']
        female_players = [p for p in players if p['gender'] == '여']
        mixed_pairs = list(combinations(male_players, 1)) + list(combinations(female_players, 1))

        games_created = 0

        def try_match(gender):
            nonlocal games_created
            grades = ['A', 'B', 'C', 'D']
            for g in grades:
                group = grouped.get((gender, g), [])
                teams = make_team_combinations(group)
                teams.sort(key=lambda t: grade_diff(*t))
                for t1 in teams:
                    for t2 in teams:
                        names = {t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}
                        if len(names) < 4:
                            continue
                        if is_usable(names):
                            matches.append((t1, t2, f"{gender}복식"))
                            for n in names:
                                player_games[n] += 1
                            used_pairs.add(tuple(sorted(names)))
                            games_created += 1
                            if games_created >= total_games:
                                return

        def try_mix():
            nonlocal games_created
            all_males = [p for p in players if p['gender'] == '남']
            all_females = [p for p in players if p['gender'] == '여']
            male_pairs = [(m1, f1) for m1 in all_males for f1 in all_females if m1['name'] != f1['name']]
            for t1 in male_pairs:
                for t2 in male_pairs:
                    names = {t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}
                    if len(names) < 4:
                        continue
                    if is_usable(names):
                        matches.append((t1, t2, "혼합복식"))
                        for n in names:
                            player_games[n] += 1
                        used_pairs.add(tuple(sorted(names)))
                        games_created += 1
                        if games_created >= total_games:
                            return

        # 남자복식 → 여자복식 → 혼합복식 순서로 매칭
        while games_created < total_games:
            try_match("남")
            if games_created < total_games:
                try_match("여")
            if games_created < total_games:
                try_mix()
            else:
                break

    generate_matches(player_list, total_games)

    # ---------------------------------------
    # 3. 출력
    # ---------------------------------------
    st.subheader("📋 생성된 대진표")

    if not matches:
        st.warning("❗ 충분한 팀 구성이 불가능합니다. 인원 수를 늘리거나 1인당 경기 수를 줄여보세요.")
    else:
        for i, (t1, t2, kind) in enumerate(matches, 1):
            team1 = f"{t1[0]['name']}({t1[0]['grade']}) & {t1[1]['name']}({t1[1]['grade']})"
            team2 = f"{t2[0]['name']}({t2[0]['grade']}) & {t2[1]['name']}({t2[1]['grade']})"
            st.markdown(f"**게임 {i} - {kind}**  
{team1} 🆚 {team2}")

        st.subheader("👤 개인별 경기 수")
        for p in player_list:
            st.markdown(f"- {p['name']}: {player_games[p['name']]}게임")

