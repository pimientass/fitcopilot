from ollama import Client

from fitcopilot.config.settings import get_settings


def ollama_chat(*, model: str, prompt: str, schema: dict) -> str:
    settings = get_settings()

    client = Client(
        host=settings.ollama_base_url,
        timeout=settings.ollama_timeout_seconds,
    )

    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format=schema,
        options={
            "temperature": 0,
        },
        keep_alive=settings.ollama_keep_alive,
    )

    content = response.message.content
    if content is None:
        raise ValueError("ollama returned empty content")

    return content
