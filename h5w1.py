import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os

st.title("6하원칙 기반 작문 도우미")

# Gemini API 키 설정
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

# Gemini 모델 초기화
if api_key is not None:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-002", temperature=0.7, api_key=api_key)
    # 6하원칙 입력 필드
    with st.container(border=True):
        who = st.text_input("누가:")
        why = st.text_input("왜:")
        when = st.text_input("언제:")
        where = st.text_input("어디서:")
        what = st.text_input("무엇을:")
        how = st.text_input("어떻게:")

    # 생성 버튼
    request = st.text_input("요청 내용을 입력하세요:")
    _, col, _ =st.columns(3)
    if col.button("작문 생성하기", use_container_width=True):
        if request and who and what and when and where and why and how:
            # 프롬프트 템플릿 생성
            template = """
            다음 6하원칙을 바탕으로 {request}(을/를) 작성해주세요:
            
            누가: {who}
            무엇을: {what}
            언제: {when}
            어디서: {where}
            왜: {why}
            어떻게: {how}
            
            다음 조건을 반드시 지켜주세요:
            1. 모든 6하원칙 요소를 자연스럽게 포함할 것
            2. 문장을 자연스럽게 연결할 것
            3. 한국어로 작성할 것
            4. 3문단 이하로 구성할 것
            """
            
            prompt = PromptTemplate(
                input_variables=["request", "who", "what", "when", "where", "why", "how"],
                template=template
            )
            
            # 작문 생성
            final_prompt = prompt.format(
                request=request,
                who=who,
                what=what,
                when=when,
                where=where,
                why=why,
                how=how
            )
            
            # 결과 출력
            st.markdown("### 생성된 작문:")
            st.write_stream(llm.stream(final_prompt))
        else:
            st.error("모든 항목을 입력해주세요!")
else:
    st.error("Gemini API 키를 먼저 입력해주세요!")




