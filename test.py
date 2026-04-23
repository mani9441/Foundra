# test_remote_ollama.py

from backend.agentic_engine.LLMs.RemoteOllamaLLM  import RemoteOllama


def main():

    llm = RemoteOllama(
        model="phi3",
        base_url="http://172.23.105.40:8000",   # change to your server IP
        temperature=0.3,
        verbose_stream=True
    )

    print("\nSending request...\n")

    response = llm.invoke(
        "You are a startup CEO. Give one short decision on launching an AI SaaS product."
    )

    print("\n\n==========================")
    print("FINAL RESPONSE:")
    print("==========================\n")
    print(response.content)


if __name__ == "__main__":
    main()