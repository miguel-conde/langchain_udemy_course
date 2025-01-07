import argparse

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import sequential

from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--language", type=str, default="Python")
parser.add_argument("--task", type=str, default="print 'Hello, World!'")
args = parser.parse_args()

llm = OpenAI()

prompt_code = PromptTemplate.from_template(
    template = "Write a very short {language} function that will {task}"
    )

prompt_test = PromptTemplate.from_template(
    template = "Write a test for the following {language} code: \n{text}"
    )

code_chain = LLMChain(
    prompt = prompt_code,
    llm = llm,
)

test_chain = LLMChain(
    prompt = prompt_test,
    llm = llm,
)

chain = code_chain | test_chain

result = chain.invoke({
    "language": args.language, 
    "task": args.task
    })

print(result)