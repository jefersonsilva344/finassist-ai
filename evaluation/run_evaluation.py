# ============================================================
# FINASSIST AI
# Sistema de Avaliação do Agente
# ============================================================

# Importa o módulo json para ler o dataset de avaliação.
import json

# Importa Path para trabalhar com caminhos de arquivos
# de forma compatível com diferentes sistemas operacionais.
from pathlib import Path


# Importa o classificador de intenção do agente.
from src.agent.intent import classify_intent

# Importa o mecanismo de recuperação da base de conhecimento.
from src.knowledge.retriever import retrieve_knowledge

# Importa a função responsável pelo cálculo da acurácia.
from evaluation.metrics import calculate_accuracy


# ============================================================
# CONFIGURAÇÃO DOS CAMINHOS
# ============================================================

# Obtém o diretório onde este arquivo está localizado.
#
# Exemplo:
#
# F:\finassist-ai\evaluation\run_evaluation.py
#
# BASE_DIR será:
#
# F:\finassist-ai\evaluation
BASE_DIR = Path(__file__).resolve().parent


# Define o caminho do dataset utilizado na avaliação.
#
# Resultado:
#
# F:\finassist-ai\evaluation\dataset.json
DATASET_PATH = BASE_DIR / "dataset.json"


# ============================================================
# CARREGAMENTO DO DATASET
# ============================================================

def load_dataset():
    """
    Carrega o dataset de avaliação em formato JSON.

    O dataset contém perguntas, intenções esperadas
    e documentos esperados da base de conhecimento.
    """

    # Abre o arquivo usando UTF-8 para preservar
    # caracteres como ç, ã, é etc.
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        # Converte o conteúdo JSON para estruturas Python.
        return json.load(file)


# ============================================================
# AVALIAÇÃO DE INTENÇÃO
# ============================================================

def evaluate_intent(dataset):
    """
    Avalia a capacidade do agente de identificar
    corretamente a intenção principal de cada pergunta.
    """

    # Contador de classificações corretas.
    correct = 0

    # Lista que armazenará os resultados individuais.
    results = []

    # Percorre todas as perguntas do dataset.
    for item in dataset:

        # Executa o classificador de intenção.
        predicted = classify_intent(
            item["question"]
        )

        # Compara a intenção prevista com a intenção esperada.
        is_correct = (
            predicted
            == item["expected_intent"]
        )

        # Se estiver correta, incrementa o contador.
        if is_correct:
            correct += 1

        # Armazena os detalhes da avaliação.
        results.append(
            {
                "id": item["id"],
                "question": item["question"],
                "expected": item["expected_intent"],
                "predicted": predicted,
                "correct": is_correct,
            }
        )

    # Calcula a acurácia da classificação.
    accuracy = calculate_accuracy(
        correct,
        len(dataset),
    )

    # Retorna a métrica e os resultados individuais.
    return accuracy, results


# ============================================================
# AVALIAÇÃO DA BASE DE CONHECIMENTO
# ============================================================

def evaluate_knowledge(dataset):
    """
    Avalia se o mecanismo de recuperação consegue
    encontrar o documento esperado para cada pergunta.
    """

    # Contador de recuperações corretas.
    correct = 0

    # Lista com os resultados individuais.
    results = []

    # Percorre todas as entradas do dataset.
    for item in dataset:

        # Obtém o documento esperado.
        #
        # O método .get() evita erro caso o campo
        # não exista no JSON.
        expected_document = item.get(
            "expected_document"
        )

        # Algumas perguntas não precisam consultar
        # a base de conhecimento.
        #
        # Exemplo:
        #
        # "Quanto é 20% de 5000?"
        #
        # Nesse caso expected_document pode estar vazio.
        if not expected_document:
            continue

        # Recupera o conhecimento relacionado à pergunta.
        context = retrieve_knowledge(
            item["question"]
        )

        # Verifica se o documento esperado aparece
        # no contexto recuperado.
        found = (
            expected_document
            in context
        )

        # Se encontrou o documento correto,
        # incrementa o contador.
        if found:
            correct += 1

        # Armazena os detalhes do resultado.
        results.append(
            {
                "id": item["id"],
                "question": item["question"],
                "expected_document": expected_document,
                "found": found,
                "context": context,
            }
        )

    # Quantidade de casos que realmente exigiram
    # recuperação de conhecimento.
    total = len(results)

    # Calcula a acurácia da recuperação.
    accuracy = calculate_accuracy(
        correct,
        total,
    )

    # Retorna a métrica e os resultados.
    return accuracy, results


# ============================================================
# CÁLCULO DA TAXA DE ERRO
# ============================================================

def calculate_error_rate(
    accuracy: float,
) -> float:
    """
    Calcula a taxa de erro a partir da acurácia.

    Exemplo:

    Accuracy = 0.90

    Error Rate = 1 - 0.90
               = 0.10

    Resultado:
    10% de erro.
    """

    return 1 - accuracy


# ============================================================
# EXIBIÇÃO DOS RESULTADOS DE INTENÇÃO
# ============================================================

def print_intent_results(results):
    """
    Exibe no terminal os resultados individuais
    da classificação de intenção.
    """

    print(
        "\n--- INTENT RESULTS ---"
    )

    # Percorre cada resultado.
    for result in results:

        # Define o status visual.
        status = (
            "OK"
            if result["correct"]
            else "FAIL"
        )

        # Mostra pergunta e intenção identificada.
        print(
            f"[{status}] "
            f"{result['question']} → "
            f"{result['predicted']}"
        )


# ============================================================
# EXIBIÇÃO DOS RESULTADOS DA BASE DE CONHECIMENTO
# ============================================================

def print_knowledge_results(results):
    """
    Exibe no terminal os resultados individuais
    da recuperação da base de conhecimento.
    """

    print(
        "\n--- KNOWLEDGE RESULTS ---"
    )

    # Percorre todos os resultados.
    for result in results:

        # Define o status visual.
        status = (
            "OK"
            if result["found"]
            else "FAIL"
        )

        print(
            f"\n[{status}]"
        )

        # Exibe o ID do caso.
        print(
            f"ID: {result['id']}"
        )

        # Exibe a pergunta.
        print(
            f"Pergunta: "
            f"{result['question']}"
        )

        # Exibe o documento que deveria
        # ter sido recuperado.
        print(
            f"Documento esperado: "
            f"{result['expected_document']}"
        )

        # Mostra se o documento foi encontrado.
        print(
            f"Encontrado: "
            f"{result['found']}"
        )

        # Se houve falha, mostra o contexto
        # que foi efetivamente recuperado.
        if not result["found"]:

            print(
                "Contexto recuperado:"
            )

            print(
                result["context"]
            )


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():
    """
    Executa todo o processo de avaliação do FinAssist AI.
    """

    # --------------------------------------------------------
    # 1. Carregar dataset
    # --------------------------------------------------------

    dataset = load_dataset()

    # --------------------------------------------------------
    # 2. Avaliar classificação de intenção
    # --------------------------------------------------------

    intent_accuracy, intent_results = (
        evaluate_intent(dataset)
    )

    # --------------------------------------------------------
    # 3. Avaliar recuperação de conhecimento
    # --------------------------------------------------------

    knowledge_accuracy, knowledge_results = (
        evaluate_knowledge(dataset)
    )

    # --------------------------------------------------------
    # 4. Calcular taxa de erro
    # --------------------------------------------------------

    intent_error = calculate_error_rate(
        intent_accuracy
    )

    knowledge_error = calculate_error_rate(
        knowledge_accuracy
    )

    # --------------------------------------------------------
    # 5. Exibir cabeçalho
    # --------------------------------------------------------

    print("=" * 60)

    print(
        "FINASSIST AI — AVALIAÇÃO"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # 6. Exibir métricas de intenção
    # --------------------------------------------------------

    print(
        f"\nIntent Accuracy: "
        f"{intent_accuracy:.2%}"
    )

    print(
        f"Intent Error Rate: "
        f"{intent_error:.2%}"
    )

    # --------------------------------------------------------
    # 7. Exibir métricas de recuperação
    # --------------------------------------------------------

    print(
        f"\nKnowledge Retrieval Accuracy: "
        f"{knowledge_accuracy:.2%}"
    )

    print(
        f"Knowledge Retrieval Error Rate: "
        f"{knowledge_error:.2%}"
    )

    # --------------------------------------------------------
    # 8. Exibir resultados individuais
    # --------------------------------------------------------

    print_intent_results(
        intent_results
    )

    print_knowledge_results(
        knowledge_results
    )


# ============================================================
# PONTO DE ENTRADA
# ============================================================

# Este bloco garante que main() seja executada somente
# quando o arquivo for executado diretamente como módulo.
if __name__ == "__main__":
    main()