from src.agent.agent import FinAssistAgent


def main() -> None:
    print("=" * 60)
    print("              FINASSIST AI")
    print("     Assistente Financeiro Inteligente")
    print("=" * 60)

    print("\nDigite 'sair' para encerrar.\n")

    agent = FinAssistAgent()

    while True:

        user_message = input("Você: ").strip()

        if user_message.lower() == "sair":
            print("\nFinAssist AI encerrado.")
            break

        if not user_message:
            continue

        try:
            response = agent.answer(
                user_message
            )

            print(f"\nFinAssist AI: {response}\n")

        except Exception as error:
            print(
                f"\nErro ao processar solicitação: {error}\n"
            )


if __name__ == "__main__":
    main()