from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

def 
prompt = ChatPromptTemplate.from_template("You are an expert in astronomy. Answer the question. <Question>: {input}")

# chain 연결 (LCEL)
chain = prompt | llm

# chain 호출
chain.invoke({"input": "지구의 자전 주기는?"})

llm.invoke("지구의 자전 주기는?")