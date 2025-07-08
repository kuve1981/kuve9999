import streamlit as st
import random
from collections import defaultdict
from itertools import combinations

st.title("🏸 급수 기반 배드민턴 대진표 생성기")

# -----------------------------
# 🔧 사용자 입력: 인원 설정
# -----------------------------
st.sidebar.header("선수 입력 설정")

grades = ['a', 'b', 'c', 'd']
sexes = ['남', '여']
players = []

# 사용자 입력으로 성별+급수별 인원 수 설정
for grade in grades:
    for sex in sexes:
        key = f"{grade}_{sex}"
        count = st.sidebar.number_input(f"{grade.upper()}급 {sex}자", min_value=0, max_value=10, value=0, step=1)
        for i in range(count):
            players.append({
                'name': f"{grade.upper()}{sex}{i+1}",
                'grade': grade,
                'sex': sex
            })

# -----------------------------
# 🎮 게임 수 설정
# -----------------------------
game_count = st.sidebar.slider("게임 수 선택", min_value=1, max_value=8, value=4)

# -----------------------------
# 📋 대진표 생성 로직
# -----------------------------

# 플레이어 shuffle & 정렬 by grade
random.shuffle(players)

# 등급별로 플레이어 분류
grade_buckets = defaultdict(list)
for p in players:
    grade_buckets[p['grade']].append(p)

# 결과 저장
matches = []

# 1게임당 4명 필요 → 전체 필요한 인원
total_players_needed = game_count * 4
selected_players = players[:total_players_needed]

def make_team_balance_score(p1, p2):
    grade_score = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    return abs(grade_score[p1['grade']] - grade_score[p2['grade']])

# 팀 생성 함수
def generate_matches(players, game_count):
    used = set()
    games = []

    def is_available(p): return p['name'] not in used

    # 모든 가능한 팀 조합
    all_pairs = [(p1, p2) for p1, p2 in combinations(players, 2) if is_available(p1) and is_available(p2)]

    # 급수 차이가 적은 조합부터 정렬
    all_pairs.sort(key=lambda pair: make_team_balance_score(pair[0], pair[1]))

    while len(games) < game_count and len(used) <= len(players) - 4:
        for (p1, p2) in all_pairs:
            if not is_available(p1) or not is_available(p2):
                continue
            for (p3, p4) in all_pairs:
                if len(set([p1['name'], p2['name'], p3['name'], p4['name']])) < 4:
                    continue
                if not (is_available(p3) and is_available(p4)):
                    continue
                # 모두 다른 사람이면 경기 성립
                team1 = (p1, p2)
                team2 = (p3, p4)
                games.append((team1, team2))
                for p in [p1, p2, p3, p4]:
                    used.add(p['name'])
                break
            if len(games) >= game_count:
                break
    return games

matches = generate_matches(selected_players, game_count)

# -----------------------------
# 🖥️ 결과 출력
# -----------------------------

st.header("📋 자동 생성된 대진표")

if not matches:
    st.warning("⚠️ 생성된 대진표가 없습니다. 총 인원을 늘려보세요.")
else:
    for i, (team1, team2) in enumerate(matches, 1):
        t1 = f"{team1[0]['name']} & {team1[1]['name']}"
        t2 = f"{team2[0]['name']} & {team2[1]['name']}"
        st.markdown(f"""**게임 {i}**
    {t1} 🆚 {t2}""")

# -----------------------------
# 🔢 참가 인원 수 확인
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(f"**총 등록 인원:** {len(players)}명")
st.sidebar.markdown(f"**필요 인원:** {total_players_needed}명")
