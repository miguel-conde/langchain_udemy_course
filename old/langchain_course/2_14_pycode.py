import argparse

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--language", type=str, default="Python")
parser.add_argument("--task", type=str, default="print 'Hello, World!'")
args = parser.parse_args()

llm = OpenAI()

prompt = PromptTemplate.from_template(
    template = "Write a very short {language} function that will {task}"
    )

code_chain = prompt | llm

result = code_chain.invoke({
    "language": args.language, 
    "task": args.task
    })

print(result)