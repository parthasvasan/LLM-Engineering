from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os

def load_env():
    load_dotenv(override=True)

    openai_key = os.getenv("OPENAI_API_KEY")
    claude_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key:
        print (f'OpenAI key exists : {openai_key[:8]}')
    if claude_key:
        print (f'Anthropic key exists : {claude_key[:12]}')

def get_system_prompt():
    return "You are an assistant that can tell jokes"

def get_user_prompt():
    return "Tell a light hearted joke to a software engineer"

def get_openai_response():
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt()

    prompts = [
        {'role': 'system', 'content':system_prompt},
        {'role': 'user', 'content':user_prompt}
    ]

    openai = OpenAI()
    response = openai.chat.completions.create (
        model='gpt-4o-mini',
        messages=prompts
    )
    return response.choices[0].message.content

def get_claude_response():
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt()

    prompts = [
        {'role': 'user', 'content':user_prompt}
    ]

    claude = Anthropic()
    response = claude.messages.create (
        model='claude-3-7-sonnet-latest',
        messages=prompts,
        max_tokens=200,
        system=system_prompt
    )
    return response.content[0].text

def get_response(model):
    if model == 'openai':
        return get_openai_response()
    elif model == 'claude':
        return get_claude_response()
    else:
        raise ValueError(f'Invalid model: {model}')

def main():
    load_env()
    model = 'openai'
    response = get_response(model)
    print(response)

if __name__ == "__main__":
    main()