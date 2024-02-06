from langchain import HuggingFacePipeline, PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import chainlit as cl 
from huggingface_hub import login
import torch

import config

login(token=config.hugging_face_token)

model_id = "TheBloke/Llama-2-13B-chat-GGML"

llm = CTransformers(
  model=model_id,
  model_type='llama',
  max_new_tokens=512,
  temperature=0.5,
  repitition_penalty=1.1,
  config={'context_length':700}
  )

with open('context_shortest.txt') as f:
    text = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)
texts = text_splitter.create_documents([text])

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                   model_kwargs={'device':'cpu'})

vectorstore = FAISS.from_documents(texts, embeddings)


custom_prompt_template='''Use the following pieces of information to answer the users question.
If you don't know the answer, please just say you don't know. Don't make up an answer.
You are a helpful assistant, you always only answer for the assistant, then you stop.

Context:{context}
History: {history}
question:{question}

Only returns the helpful answer below and nothing else.
Helpful answer
'''

retriever = vectorstore.as_retriever()

@cl.on_chat_start
async def main():
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['history', 'context', 'question'])
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever = retriever,
        chain_type_kwargs={'prompt':prompt,
                       "memory": ConversationBufferMemory(
                                memory_key="history",
                                input_key="question")}
        )
 
    msg=cl.Message(content="Firing up the QA bot...")
    await msg.send()
    msg.content="Hello, welcome to the DataSpeak Chatbot. What is your query?"
    await msg.update()
    cl.user_session.set("qa_chain", qa_chain)
    
 
@cl.on_message 
async def main(message: str):
    qa_chain = cl.user_session.get("qa_chain")
   
    res = await qa_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])
  
    await cl.Message(
        content=res["result"]
    ).send()

