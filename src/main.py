from src.bootstrap.factory import build_application
from src.persistence.session import get_session_factory


def main() -> None:
    print("=" * 60)
    print("              FINASSIST AI")
    print("     Assistente Financeiro Inteligente")
    print("=" * 60)

    print("\nDigite 'sair' para encerrar.\n")

    session_factory = get_session_factory()
    db = session_factory()

    try:
        container = build_application(db)

        while True:
            user_message = input("Você: ").strip()

            if user_message.lower() == "sair":
                print("\nFinAssist AI encerrado.")
                break

            if not user_message:
                continue

            try:
                response = container.financial_flow.process_message(
                    external_user_id="cli-user",
                    message=user_message,
                )

                print(f"\nFinAssist AI: {response}\n")

            except Exception as error:
                print(
                    f"\nErro ao processar solicitação: {error}\n"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()