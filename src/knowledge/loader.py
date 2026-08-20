from pathlib import Path


KNOWLEDGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "knowledge"
)


def load_knowledge() -> dict[str, str]:
    """
    Carrega todos os documentos Markdown da base de conhecimento.
    """

    documents: dict[str, str] = {}

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        documents[file_path.name] = file_path.read_text(
            encoding="utf-8"
        )

    return documents