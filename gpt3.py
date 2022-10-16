from jmespath import search
import openai


def gpt3complete(speech):
    return openai.Completion.create(model="text-davinci-002", prompt="Decide whether a Text's sentiment is positive, neutral, or negative.\n\nText: \"I loved the new Batman movie!\"\nSentiment:", temperature=0, max_tokens=60, top_p=1.0, frequency_penalty=0.5, presence_penalty=0.0)