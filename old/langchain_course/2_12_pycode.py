from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

llm = OpenAI()
# prompt = PromptTemplate(
#     template = "Write a very short {language} function that will {task}",
#     input_variables = ["language", "task"]
#     )
prompt = PromptTemplate.from_template(
    template = "Write a very short {language} function that will {task}"
    )

# code_chain = LLMChain(
#     llm = llm, 
#     prompt = prompt
#     )

code_chain = prompt | llm

# result = code_chain.invoke({"language": "Python", "task": "print 'Hello, World!'"})
result = code_chain.invoke({
    "language": "Python", 
    "task": "print 'Hello, World!'"
    })
# print(result['text'])
print(result)
