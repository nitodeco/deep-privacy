import openai
from pydantic import BaseModel


def init_client(key: str):
    global client
    client = openai.OpenAI(api_key=key)


def generate_completion(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    model: str = "gpt-4o",
    temperature: float = 0.5,
    response_format: BaseModel | None = None,
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        response_format=response_format,
    )
    return response.choices[0].message.content
