# 새로운 자료 추가하기
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import koreanize_matplotlib
plt.rcParams["font.family"] = ["NanumGothic", "AppleGothic", "Malgun Gothic"]

st.title("✍️ 내 통학시간 입력하기")
st.info("입력한 값은 구글 시트 측정자료 탭에 학번과 함께 저장됩니다. ")

student_id = st.session_state.get("학번")
# st.write(student_id)

if not student_id:
    st.warning("메인화면에서 먼저 학번을 입력해주세요.")
    st.stop()

# '측정자료' 탭과 연결하기
gsheets_secrets = st.secrets.get("connections", {}).get("gsheets", {})
spreadsheet = gsheets_secrets.get("spreadsheet")
if not spreadsheet:
    st.error("Google Sheets 주소가 설정되지 않았습니다. .streamlit/secrets.toml의 [connections.gsheets]에 spreadsheet를 설정해주세요.")
    st.stop()

conn = st.connection("gsheets", type = GSheetsConnection)
df = conn.read(spreadsheet = spreadsheet, worksheet = "data", usecols = [0,1,2], ttl = 0)
# st.write(df)

# 통학시간 제출하기
with st.form("measure", clear_on_submit = True):
    group = st.selectbox("반", ["1반", "2반", "3반"])
    minutes = st.number_input("통학 시간(분)", 
    min_value = 0, max_value = 180,
    value = None, step = 1)
    submitted = st.form_submit_button("제출")

if submitted:
    if minutes is None:
        st.warning("통학 시간을 입력해주세요. ")
    else:
        new_row = pd.DataFrame([[student_id, group, minutes]],
        columns = df.columns) #새로운 한 줄을 만들기
        st.write(new_row)
        # df 업데이트
        df = pd.concat([df, new_row], ignore_index = True)
        conn.update(worksheet = "data", data = df)
        st.success(f"{student_id}학생의 통학시간이 저장되었습니다. ")

st.subheader(f"지금까지 입력한 학생 수 : {len(df)}명")
fig, ax = plt.subplots(figsize =(8,3))
sns.boxplot(data = df, x = "통학 시간(분)", y = "반", 
whis=(0, 100), ax = ax)
st.pyplot(fig)
