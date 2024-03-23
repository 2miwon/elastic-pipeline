from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from config import *

sum_llm = ChatOpenAI(model=os.getenv("SUMMARY_MODEL"), temperature=0)
chat_llm = ChatOpenAI(model=os.getenv("CHAT_MODEL"), temperature=0)
# card_img_gen = ChatOpenAI(model=os.getenv("CARD_IMG_GEN_MODEL"))

sum_prompt = ChatPromptTemplate.from_template("You are an expert in astronomy. Answer the question. <Question>: {input}")
chat_prompt = ChatPromptTemplate.from_template("You are an expert in astronomy. Answer the question. <Question>: {input}")

def chat(prompt, system_prompt=os.getenv("CHAT_PROMPT")):
    response = chat_llm(f"{system_prompt}\n\nHuman: {prompt}\nAssistant:")
    return response.strip("Assistant:")

def summary(bill_id):
    link = "/file/{bill_id}"

    try:
        loader = PyPDFLoader(link)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        summary_chain = load_summarize_chain(sum_llm, chain_type="map_reduce", map_prompt=PromptTemplate(
            template="Summarize this text in 3 bullet points:\n\n{text}",
            input_variables=["text"]
        ))
        summary = summary_chain.run(texts)
        return summary

    except Exception:
        return "No response"

def check_chat(prompt, bill_id, system_prompt=os.getenv("SUM_PROMPT")):
    link = "/file/{bill_id}"

    try:
        loader = PyPDFLoader(link)
        documents = loader.load()
        extracted_text = "".join([doc.page_content for doc in documents])

        txt = f"{prompt} External references include a '(Source: {extracted_text})' citation."
        response = sum_llm(f"{system_prompt}\n\nHuman: {txt}\nAssistant:")
        return response.strip("Assistant:")

    except Exception:
        return "No response"
    
if __name__ == "__main__":
    print(chat_llm.invoke("지구의 자전 주기는?"))
    # print(chat("hi"))