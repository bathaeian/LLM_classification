import os
import argparse
import requests
from dotenv import load_dotenv


def main():

    load_dotenv()

    api_key = os.getenv("API_key")

    if not api_key:
        raise ValueError("API_key not found in .env")

    parser = argparse.ArgumentParser(description="Send a prompt to OpenRouter LLM")

    parser.add_argument("--prompt", required=True, help="Path to prompt file")

    parser.add_argument("--output", required=True, help="Path to save LLM response")

    parser.add_argument(
        "--model", default="openai/gpt-oss-20b:free", help="OpenRouter model name"
    )

    args = parser.parse_args()

    with open(args.prompt, "r") as f:
        prompt = f.read()

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        json={"model": args.model, "messages": [{"role": "user", "content": prompt}]},
    )

    response_json = response.json()

    if "error" in response_json:
        raise RuntimeError(response_json["error"])

    result = response_json["choices"][0]["message"]["content"]

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, "w") as f:
        f.write(result)

    print("Prompt:")
    print(args.prompt)

    print("Model:")
    print(args.model)

    print("Response saved:")
    print(args.output)


if __name__ == "__main__":
    main()
