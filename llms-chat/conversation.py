import os
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
from IPython.display import display, Markdown

def load_env():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY"), os.getenv("ANTHROPIC_API_KEY")


def call_gpt(openai_llm, gpt_model, gpt_messages, claude_messages):
    gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

    messages = [{"role": "system", "content": gpt_system}]

    for gpt, claude in zip(gpt_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": claude})
    completion = openai_llm.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

def call_claude(anthropic_llm, claude_model, claude_messages, gpt_messages):
    claude_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

    messages = []
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = anthropic_llm.messages.create(
        model=claude_model,
        system=claude_system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text

def main():
    api_key, anthropic_api_key = load_env()
    
    gpt_model = "gpt-4o-mini"
    claude_model = "claude-3-haiku-20240307"

    openai_llm = OpenAI()
    anthropic_llm = Anthropic()

    gpt_messages = ["Hi there"]
    claude_messages = ["Hi"]

    for i in range(5):
        gpt_next = call_gpt(openai_llm, gpt_model, gpt_messages, claude_messages)
        print(f"GPT:\n{gpt_next}\n")
        gpt_messages.append(gpt_next)
    
        claude_next = call_claude(anthropic_llm, claude_model, claude_messages, gpt_messages)
        print(f"Claude:\n{claude_next}\n")
        claude_messages.append(claude_next)

    

if __name__ == "__main__":
    main()