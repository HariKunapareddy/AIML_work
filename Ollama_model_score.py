from langchain_community.llms import Ollama


llm = Ollama(model="mistral")

prompt='''For the given user question please validate whether the answer on below points and return only score with out explanation
1. The answer is what user exactly looking for and give the score on the scale of 1 to 10. Give score 1 if answer is not user is looking for the question, give score 10 if answer is exactly what user is looking for 

question: {question}
answer: {answer}'''

question='what is my bill amount?'
answer="You can look at the century link portal for billing infomration"


print(llm.invoke(prompt.format(question=question,answer=answer)))
