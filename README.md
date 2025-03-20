# 🚀 FastAPI Project

Este repositório contém um projeto utilizando FastAPI para autenticação via JWT.

## 📌 Requisitos

- 🐍 Python 3.8+
- 📦 `pip` instalado

## ⚙️ Configuração do Ambiente Virtual

1. 🏗️ Crie um ambiente virtual:
   ```sh
   python -m venv fastapi_env
   ```
2. 🔌 Ative o ambiente virtual:
   - No Windows:
     ```sh
     fastapi_env\Scripts\activate
     ```
   - No macOS/Linux:
     ```sh
     source fastapi_env/bin/activate
     ```

## 📥 Instalação das Dependências

1. 📜 Instale as dependências do projeto:
   ```sh
   pip install -r requirements.txt
   ```
2. Caso o arquivo `requirements.txt` não exista, instale manualmente os pacotes necessários:
   ```sh
   pip install fastapi uvicorn
   ```
   Depois, gere o arquivo de dependências:
   ```sh
   pip freeze > requirements.txt
   ```

## ▶️ Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```sh
fastapi dev main.py
```

O servidor rodará por padrão em `http://127.0.0.1:8000/`.

## 🔗 Endpoints Principais

- 🔑 `POST /login` - Autentica o usuário e retorna um token JWT.
- 🔒 `GET /protected` - Rota protegida que exige autenticação via token.

## 👤 Autores

Gabriel Meira
Gabriela Fiori
Gabriel Barbosa
Heitor Morais
Henrique César

## 📜 Licença

Este projeto está sob a licença [MIT](LICENSE).
