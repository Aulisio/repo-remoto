from search import search_prompt


def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Chat iniciado. Digite 'sair' para encerrar.\n")
    while True:
        try:
            question = input("PERGUNTA: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

        if not question:
            continue
        if question.lower() == "sair":
            print("Encerrando...")
            break

        answer = chain(question)
        print(f"RESPOSTA: {answer}\n")


if __name__ == "__main__":
    main()