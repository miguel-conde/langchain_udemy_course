# from langchain.llms import OpenAI
from langchain_openai import OpenAI

llm = OpenAI()

# result = llm("Write a very very short poem")
result = llm.invoke("Write a very very short poem")
print(result)

  