import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from zoneinfo import ZoneInfo # 한국시간 기록

st.title("상자그림 형성평가")
st.info("모든 문제를 푼 뒤 맨 아래 채점하기를 눌러주세요.")

student_id = st.session_state.get("학번")
# st.write(student_id)

if not student_id:
    st.warning("메인 화면에서 학번을 먼저 입력하세요.")
    st.stop()

conn = st.connection("gsheets", type = GSheetsConnection)
quiz = conn.read(worksheet = "문항", ttl = 60)

# 학생이 푼 답이 저장될 곳
answers = {}
choices = {}

with st.form("quiz"):
    for n, (i, row) in enumerate(quiz.iterrows(), start = 1):
        st.markdown(f"문제 {n}. {row['문제']}")
        choices[i] = {row[f"보기{k}"]: k for k in range(1, 5) if pd.notna(row[f"보기{k}"])}
        answers[i] = st.radio("답을 고르세요.", list(choices[i]), index=None, key=f"q_{i}")
    submitted = st.form_submit_button("채점하기")

if submitted:
    score = 0
    for n, (i, row) in enumerate(quiz.iterrows(), start = 1):
        selected = answers[i]
        if selected is None:
            st.warning(f"문제 {n}: 답을 고르지 않았어요!")
            continue
        k = choices[i][selected]  # 고른 보기의 번호
        hint = row[f"힌트{k}"] if pd.notna(row[f"힌트{k}"]) else ""  # 그 보기에 맞춘 힌트

        if str(selected) == str(row["정답"]):  # 숫자와 글자를 모두 글자로 바꿔 비교
            score += 1
            st.success(f"문제 {n}: 정답입니다. {hint}")
        else:
            st.warning(f"문제 {n}: {hint}")

    total = len(quiz)
    point = round(score / total * 100)
    st.metric("내 점수", f"{point}점", f"{total}문항 중 {score}문항 정답")
    if score == total:
        st.balloons()  # 만점이면 풍선 효과

    # 응답을 형성평가응답 탭에 한 줄 추가하기
    now = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")
    response_columns = [f"문제{n} 응답" for n in range(1, len(quiz) + 1)]
    columns = ["제출 시각", "학번", "점수", *response_columns]

    log = conn.read(worksheet="형성평가응답", ttl=0).dropna(how="all")
    # 기존 시트의 열 이름을 현재 형식에 맞추고, 문항 수만큼 응답 열을 확보합니다.
    log = log.iloc[:, :len(columns)].copy()
    for _ in range(len(columns) - len(log.columns)):
        log[f"_응답열{len(log.columns)}"] = ""
    log.columns = columns

    picked = [answers[i] if answers[i] is not None else "" for i in quiz.index]
    new_row = pd.DataFrame([[now, student_id, point, *picked]], columns=columns)
    conn.update(worksheet="형성평가응답", data=pd.concat([log, new_row], ignore_index=True))
    st.caption("응답이 저장되었습니다.")
