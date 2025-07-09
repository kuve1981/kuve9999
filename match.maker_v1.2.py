import streamlit as st
from itertools import combinations
from collections import defaultdict

st.title("🏸 배드민턴 대진표 생성기 (급수 + 성별 기반)")

# 사용자 입력
st.sidebar.header("🛠️ 설정")
num_players = st.sidebar.number_input("총 참가 인원 수", min_value=4, max_value=40, value=12, step=1)
games_per_player = st.sidebar.slider("1인당 경기 수", min_value=1, max_value=10, value=2)

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
    used_combinations = set()
    matches = []

    grade_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    def grade_diff(p1, p2):
        return abs(grade_order[p1['grade']] - grade_order[p2['grade']])

    def is_valid_match(t1, t2, strict=True):
        names = {p['name'] for p in t1 + t2}
        if len(names) < 4:
            return False
        if any(player_games[name] >= games_per_player for name in names):
            return False
        if strict and tuple(sorted(names)) in used_combinations:
            return False
        return True

    def add_match(t1, t2, match_type):
        names = [p['name'] for p in t1 + t2]
        for name in names:
            player_games[name] += 1
        used_combinations.add(tuple(sorted(names)))
        matches.append((t1, t2, match_type))

    def create_matches_by_gender(gender, allow_reuse=False):
        group = [p for p in players if player_games[p['name']] < games_per_player or allow_reuse]
        group = [p for p in group if p['gender'] == gender]
        team_pairs = list(combinations(group, 2))
        team_pairs.sort(key=lambda t: grade_diff(t[0], t[1]))
        for t1 in team_pairs:
            for t2 in team_pairs:
                if len({t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}) < 4:
                    continue
                if is_valid_match(t1, t2, strict=not allow_reuse):
                    add_match(t1, t2, f"{gender}복식")
                    return True
        return False

    def create_mixed_matches(allow_reuse=False):
        males = [p for p in players if player_games[p['name']] < games_per_player or allow_reuse]
        males = [p for p in males if p['gender'] == '남']
        females = [p for p in players if player_games[p['name']] < games_per_player or allow_reuse]
        females = [p for p in females if p['gender'] == '여']
        pairs = [(m, f) for m in males for f in females if m['name'] != f['name']]
        pairs.sort(key=lambda t: grade_diff(t[0], t[1]))
        for t1 in pairs:
            for t2 in pairs:
                names = {t1[0]['name'], t1[1]['name'], t2[0]['name'], t2[1]['name']}
                if len(names) < 4:
                    continue
                if is_valid_match(t1, t2, strict=not allow_reuse):
                    add_match(t1, t2, "혼합복식")
                    return True
        return False

    # 경기 생성 루프
    def fill_matches(allow_reuse=False):
        made_match = create_matches_by_gender("남", allow_reuse)
        if not made_match:
            made_match = create_matches_by_gender("여", allow_reuse)
        if not made_match:
            made_match = create_mixed_matches(allow_reuse)
        return made_match

    # 모든 인원이 목표 경기 수를 채울 때까지
    while any(player_games[p['name']] < games_per_player for p in players):
        filled = fill_matches(allow_reuse=False)
        if not filled:
            # 기존 사용된 조합까지 허용하여 채우기 시도
            filled = fill_matches(allow_reuse=True)
            if not filled:
                st.warning("⚠️ 모든 조합을 시도했지만 더 이상 경기 구성이 어렵습니다.")
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
