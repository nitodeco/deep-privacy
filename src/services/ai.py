import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import json

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_completion(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    model: str = "gpt-4o",
    temperature: float = 0.5,
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


def generate_structured_completion(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    model: str = "gpt-4o",
    temperature: float = 0.5,
    response_format: BaseModel | None = None,
):
    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        response_format=response_format,
    )
    parsed_response = json.loads(response.choices[0].message.content)
    if response_format:
        return response_format(**parsed_response)
