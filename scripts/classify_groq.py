from openai import OpenAI
from dotenv import load_dotenv

import argparse
import os


load_dotenv()
# print(os.getenv("GROQ_API_KEY"))
# exit()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)

    parser.add_argument(
        "--model",
        default="llama-3.3-70b-versatile"
    )

    args = parser.parse_args()

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    with open(args.prompt, "r") as f:
        prompt = f.read()
    # prompt = "Say hello in one sentence."

    response = client.chat.completions.create(
        model=args.model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, "w") as f:
        f.write(result)

    print("Done!")
    print(f"Model: {args.model}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()