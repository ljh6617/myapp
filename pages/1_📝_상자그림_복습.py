import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Python 3.12+ no longer includes distutils. koreanize-matplotlib still imports
# LooseVersion from it, so provide the compatible implementation bundled by setuptools.
import sys
import types
from setuptools._distutils.version import LooseVersion

distutils = types.ModuleType("distutils")
distutils_version = types.ModuleType("distutils.version")
distutils_version.LooseVersion = LooseVersion
distutils.version = distutils_version
sys.modules.setdefault("distutils", distutils)
sys.modules.setdefault("distutils.version", distutils_version)
import koreanize_matplotlib
plt.rcParams["font.family"] = ["NanumGothic", "AppleGothic", "Malgun Gothic"]


st.title("📝 상자그림 복습하기")
st.info("과자 14개의 열량 자료를 상자그림으로 나타낸 것입니다. ")
data = [290, 291, 291, 293, 294, 295, 299, 301, 303, 303, 303, 305, 305, 307]

st.write("**자료 (단위 : kcal) :**", ", ".join(map(str, data)))

# 상자그림 그리기
fig, ax = plt.subplots(figsize = (8, 1))

sns.boxplot(x = data, ax = ax)
ax.set_xlabel("과자의 열량(kcal)")
st.pyplot(fig)

# 복습 퀴즈
quiz = [
    {"문제": "1. 중앙값은?", "보기": [299, 300, 301, 303], 
    "정답": 300,
     "힌트": {299: "자료가 14개이므로 가운데 두 값 299와 301의 평균을 구하세요.",
             301: "자료가 14개이므로 가운데 두 값 299와 301의 평균을 구하세요.",
             303: "303은 가장 많이 나온 값입니다. 가운데 두 값을 찾아보세요."}},
    {"문제": "2. 제1사분위수는?", "보기": [291, 293, 294, 295], "정답": 293,
     "힌트": {291: "중앙값보다 왼쪽에 있는 자료 7개 전체의 중앙값을 구하세요.",
             294: "왼쪽 자료 290, 291, 291, 293, 294, 295, 299에서 가운데 값을 찾아보세요.",
             295: "왼쪽 자료 290, 291, 291, 293, 294, 295, 299에서 가운데 값을 찾아보세요."}},
    {"문제": "3. 제3사분위수는?", "보기": [303, 304, 305, 307], "정답": 303,
     "힌트": {304: "오른쪽 자료 7개 중 가운데 값은 자료에 있는 값입니다.",
             305: "오른쪽 자료 301, 303, 303, 303, 305, 305, 307에서 가운데 값을 찾아보세요.",
             307: "307은 최댓값입니다."}},
    {"문제": "4. 상자 안에 들어 있는 자료는 전체의 약 몇 %인가?", "보기": ["25 %", "50 %", "75 %"], "정답": "50 %",
     "힌트": {"25 %": "사분위수로 나뉜 구간 하나가 약 25 %입니다. 상자에는 구간이 몇 개인가요?",
             "75 %": "최솟값부터 제3사분위수까지가 약 75 %입니다."}},
]

# 모든 문제 셋을 한꺼번에 고른 뒤 한 번에 채점하기
with st.form("quiz"):
    answers = [st.radio(q["문제"], q["보기"], 
    index = None, key = n) for n, q in enumerate(quiz)]
    submitted = st.form_submit_button("채점하기")

# if submitted:
#     score = 0
#     for q, a in zip(quiz, answers):
#         if a ==q["정답"]:
#             score += 1
#             st.success(f"{q["문제"]}\n\n정답입니다. ")
#         elif a is None:
#             st.error(f"{q["문제"]}\n\n문항에 답을 고르지 않았습니다.")
#         else :
#             st.warning(f"{q["문제"]}\n\n{q["힌트"][a]}")

#     st.metric("점수", f"{score} / {len(quiz)}")
