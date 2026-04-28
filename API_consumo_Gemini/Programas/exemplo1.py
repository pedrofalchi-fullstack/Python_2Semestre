import os  # Biblioteca para manipular variáveis de sistema
from dotenv import load_dotenv  # Carrega configurações do arquivo .env
from google import genai  # Importa o novo SDK do Gemini

# 1. Configuração inicial
load_dotenv()  # Carrega o arquivo .env
api_key = os.getenv("GEMINI_API_KEY")  # Obtém a chave de API

# 2. Inicialização do cliente e sessão
client = genai.Client(api_key=api_key)  # Cria o cliente da API
modelo_alvo = "gemini-2.5-flash-lite"  # Define o modelo estável e gratuito
chat = client.chats.create(model=modelo_alvo)  # Cria a sessão que manterá o histórico

print(f"--- Chat Iniciado com {modelo_alvo} ---")
print("Digite 'sair' para encerrar a conversa.\n")

# 3. Loop de conversa contínua
while True:
    # Captura a entrada do usuário
    pergunta = input("Você: ")

    # Condição de parada: se o usuário digitar 'sair', o loop quebra
    if pergunta.lower() in ["sair", "exit", "quit", "parar"]:
        print("Encerrando chat... Até logo!")
        break

    try:
        # Envia a mensagem para o modelo dentro do contexto do chat atual
        resposta = chat.send_message_stream(pergunta)

        print("Gemini:", end=" ", flush=True)

        # Itera sobre os pedaços da resposta (streaming)
        for chunk in resposta:
            if chunk.text:
                print(chunk.text, end='', flush=True)

        print("\n" + "-" * 30)  # Linha separadora para organizar o terminal

    except Exception as e:
        # Trata erros de conexão ou cota sem fechar o programa
        print(f"\n[ERRO]: {e}")
        print("Tente novamente em instantes ou verifique sua conexão.")