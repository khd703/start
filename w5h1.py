import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# 페이지 설정
st.set_page_config(page_title="6하원칙 작문 도우미", layout="wide")

# API 키 입력
api_key = st.sidebar.text_input("Google API Key를 입력하세요", type="password")

# 6하원칙 입력 필드
st.title("6하원칙 작문 도우미")

col1, col2 = st.columns(2)

with col1:
    who = st.text_input("누가")
    when = st.text_input("언제")
    where = st.text_input("어디서")
    
with col2:
    what = st.text_input("무엇을")
    how = st.text_input("어떻게")
    why = st.text_input("왜")

# 프롬프트 템플릿 설정
prompt_template = """
다음 6하원칙을 바탕으로 자연스러운 글을 작성해주세요:

- 누가: {who}
- 언제: {when}
- 어디서: {where}
- 무엇을: {what}
- 어떻게: {how}
- 왜: {why}

위 정보를 바탕으로 자연스럽게 연결된 하나의 글을 작성해주세요.
"""

# 생성 버튼
if st.button("작문 생성"):
    if not api_key:
        st.error("API키가 없습니다.")
    elif not all([who, when, where, what, how, why]):
        st.error("모든 항목을 입력해주세요!")
    else:
        try:
            # Gemini 모델 설정
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.0-pro",
                google_api_key=api_key,
                temperature=0.7
            )
            
            # 프롬프트 생성
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["who", "when", "where", "what", "how", "why"]
            )
            
            # 결과 생성
            response = llm.invoke(
                prompt.format(
                    who=who, when=when, where=where,
                    what=what, how=how, why=why
                )
            )
            
            # 결과 출력
            st.subheader("생성된 작문")
            st.write(response.content)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
