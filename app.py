import streamlit as st
import pandas as pd
import random
import os
from PIL import Image

# -----------------------------
# CSV 불러오기
# -----------------------------
df = pd.read_csv("spanish - 시트1.csv", encoding="utf-8")

# -----------------------------
# 제목
# -----------------------------
st.title("🎮 스페인어 퀴즈 게임")
st.write("10문제를 풀고 띠부씰을 모아보세요!")

# -----------------------------
# session_state 초기화
# -----------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "questions" not in st.session_state:
    st.session_state.questions = None

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "reward_given" not in st.session_state:
    st.session_state.reward_given = False

# -----------------------------
# 카테고리 선택
# -----------------------------
category = st.selectbox(
    "카테고리를 선택하세요",
    df["category"].unique()
)

selected_df = df[df["category"] == category]

# -----------------------------
# 게임 시작 버튼
# -----------------------------
if st.button("🎮 게임 시작"):

    st.session_state.questions = selected_df.sample(
        n=min(10, len(selected_df))
    ).reset_index(drop=True)

    st.session_state.started = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.show_result = False
    st.session_state.reward_given = False

# -----------------------------
# 게임 진행
# -----------------------------
if st.session_state.started:

    questions = st.session_state.questions
    idx = st.session_state.question_index

    # 문제 남아있을 때
    if idx < len(questions):

        q = questions.iloc[idx]

        st.write(f"# 문제 {idx + 1}")
        st.write(q["quiz"])
        st.write("뜻 :", q["korean"])

        answer = st.text_input(
            "정답 입력",
            key=f"answer_{idx}"
        )

        # 제출 버튼
        if st.button("제출", key=f"submit_{idx}"):

            st.session_state.show_result = True

            if answer == q["answer"]:

                st.success("정답입니다! 🎉")
                st.session_state.score += 1

            else:

                st.error("틀렸습니다!")

            st.write(f"정답 : {q['answer']}")

        # 다음 문제 버튼
        if st.session_state.show_result:

            if st.button("다음 문제"):

                st.session_state.question_index += 1
                st.session_state.show_result = False

                st.rerun()

    # -----------------------------
    # 게임 종료
    # -----------------------------
    else:

        score = st.session_state.score
        total = len(questions)

        percent = (score / total) * 100

        st.write("# 🎉 게임 종료")
        st.write(f"점수 : {score} / {total}")
        st.write(f"정답률 : {percent:.0f}%")

        # -----------------------------
        # 띠부씰 지급
        # -----------------------------
        if percent >= 80 and not st.session_state.reward_given:

            st.success("🎁 띠부씰 획득!")

            images = []

            for file in os.listdir():
                if file.endswith(".png"):
                    images.append(file)

            if len(images) > 0:

                selected = random.choice(images)

                # collection 저장
                with open("collection.txt", "a") as f:
                    f.write(selected + "\n")

                img = Image.open(selected)

                st.image(img, width=300)

                st.write("획득한 띠부씰 :", selected)

                # 중복 지급 방지
                st.session_state.reward_given = True

        elif percent < 80:

            st.error("아쉽습니다! 다음에 다시 도전하세요!")

# -----------------------------
# 컬렉션 보기
# -----------------------------
st.divider()

if st.button("📖 컬렉션 보기"):

    collection = []

    # collection 파일 없으면 생성
    if not os.path.exists("collection.txt"):
        open("collection.txt", "w").close()

    # collection 불러오기
    with open("collection.txt", "r") as f:
        for line in f:
            collection.append(line.strip())

    # 중복 제거
    collection = list(set(collection))

    st.write("# 📚 내 컬렉션")

    if len(collection) == 0:

        st.write("아직 획득한 띠부씰이 없습니다.")

    else:

        for item in collection:

            if os.path.exists(item):

                img = Image.open(item)

                st.image(img, width=200)

                st.write(item)