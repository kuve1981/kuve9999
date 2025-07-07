import streamlit as st
import random
from itertools import combinations

# 전체 선수 목록
male_players = ['a남', 'b남', 'c남', 'd남', 'e남', 'f남']
female_players = ['a여', 'b여', 'c여', 'd여', 'e여', 'f여']

st.title("🏸 배드민턴 대진표 생성기")
st.markdown("한 사람당 4게임, 지각자 고려 대진표 자동 생성")

# 지각자 선택
late_males = st.multiselect("지각 남자 선수 (게임 3부터 참여)", male_players)
late_females = st.multiselect("지각 여자 선수 (게임 3부터 참여)", female_players)

# 참여 가능한 시점 선택
start_game = 3

# 각 사람의 게임 기록용
player_games = {p: [] for p in male_players + female_players}

# 대진표 저장
matches = []

# 최대 게임 수
total_matches = 12

# 가능한 모든 팀 조합
def make_teams(males, females):
    teams = []

    # 남자 복식
    for team1, team2 in combinations(combinations(males, 2), 2):
        if len(set(team1 + team2)) == 4:
            teams.append((team1, team2, "MD"))

    # 여자 복식
    for team1, team2 in combinations(combinations(females, 2), 2):
        if len(set(team1 + team2)) == 4:
            teams.append((team1, team2, "WD"))

    # 혼합 복식
    xd_pairs = list(combinations(males, 1))
    for m1 in xd_pairs:
        for f1 in females:
            for m2 in xd_pairs:
                for f2 in females:
                    if m1 != m2 and f1 != f2 and len({m1[0], f1, m2[0], f2}) == 4:
                        team1 = (m1[0], f1)
                        team2 = (m2[0], f2)
                        teams.append((team1, team2, "XD"))
    return teams

# 팀 필터: 지각자 고려 + 4게임 초과 안 됨
def is_valid_team(team1, team2, game_idx):
    all_players = list(team1 + team2)
    for p in all_players:
        if len(player_games[p]) >= 4:
            return False
        if game_idx < start_game:
            if p in late_males or p in late_females:
                return False
    return True

# 대진 생성
def create_schedule():
    game_idx = 1
    teams = make_teams(male_players, female_players)
    random.shuffle(teams)

    while game_idx <= total_matches:
        for t1, t2, match_type in teams:
            if is_valid_team(t1, t2, game_idx):
                matches.append({
                    '게임': game_idx,
                    '팀1': t1,
                    '팀2': t2,
                    '유형': match_type
                })
                for p in t1 + t2:
                    player_games[p].append(game_idx)
                game_idx += 1
                break
        else:
            st.warning("⚠️ 대진표를 완전히 만들 수 없습니다. 지각자가 너무 많거나 제한이 많을 수 있어요.")
            break

create_schedule()

# 출력
st.subheader("📋 자동 생성된 대진표")
for m in matches:
    t1 = ' & '.join(m['팀1'])
    t2 = ' & '.join(m['팀2'])
    st.markdown(f"**게임 {m['게임']}** ({m['유형']})  
    → {t1} vs {t2}")

# 개인별 게임 수 출력
st.subheader("👤 개인별 게임 수")
for p, games in player_games.items():
    st.markdown(f"- {p} : {len(games)}게임")

