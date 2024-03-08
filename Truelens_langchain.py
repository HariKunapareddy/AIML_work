
from trulens_eval import TruChain
from trulens_eval.feedback.provider.langchain import Langchain

from langchain.chains import LLMChain
from trulens_eval.feedback import Feedback, Huggingface, OpenAI

from langchain_community.llms import Ollama
import os

from trulens_eval import Tru
tru=Tru()

os.environ["OPENAI_API_KEY"] = "sk-*"

llm = Ollama(model="llama2")






 # Code snippet taken from langchain 0.0.281 (API subject to change with new versions)
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate

full_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        template=
        "Provide a helpful response with relevant background information for the following: {prompt}",
        input_variables=["prompt"],
    )
)

chat_prompt_template = ChatPromptTemplate.from_messages([full_prompt])

llm = OpenAI(temperature=0.9, max_tokens=128)

chain = LLMChain(llm=llm, prompt=chat_prompt_template, verbose=True)





from trulens_eval.feedback import Feedback, Huggingface, OpenAI
# Initialize HuggingFace-based feedback function collection class:
hugs = Huggingface()
openai = OpenAI()

# Define a language match feedback function using HuggingFace.
lang_match = Feedback(hugs.language_match).on_input_output()
# By default this will check language match on the main app input and main app
# output.

# Question/answer relevance between overall question and answer.
qa_relevance = Feedback(openai.relevance).on_input_output()
# By default this will evaluate feedback on main app input and main app output.



# wrap your chain with TruChain
truchain = TruChain(
    chain,
    app_id='Chain1_ChatApplication',
    feedbacks=[ qa_relevance]
)
# Note: any `feedbacks` specified here will be evaluated and logged whenever the chain is used.
#truchain("What is my total order count?")

prompts = [
    "What company acquired MosaicML?",
    "What's the best way to travel from NYC to LA?",
    "How did the change in the exchange rate during 2021 affect the stock price of US based companies?",
    "Compare the stock performance of Google and Microsoft",
    "What is the highest market cap airline that flies from Los Angeles to New York City?",
    "I'm interested in buying a new smartphone from the producer with the highest stock price. Which company produces the smartphone I should by and what is their current stock price?"
]

with truchain as recording:
    chain("What is my bill amount?")

rec = recording.get()

print(rec)

tru_record = recording.records[0]
#print(tru_record.feedback_results)

for feedback, feedback_result in rec.wait_for_feedback_results().items():
    print(feedback.name, feedback_result.result)

tru.run_dashboard()