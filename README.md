# 🎮 API Mobile - Biblioteca de Jogos

Esta API foi desenvolvida para a disciplina de Programação Mobile (2º Bimestre) e serve como backend (CRUD) para gerenciar uma biblioteca pessoal de jogos e suas respectivas avaliações.

A API possui um sistema de persistência em memória (RAM) e foi projetada para ser tolerante a falhas, bloqueando requisições com formatos incorretos (retornando os Status Codes exatos exigidos na especificação).

## 🛠️ Tecnologias Utilizadas
* **Node.js** com **Express** (Criação do Servidor)
* **UUID** (Geração de Tokens de Autenticação)
* **Hospedagem:** Render
* **Python 3** com `requests` (Script de Automação de Testes QA)

---

## 🚀 Como rodar a API localmente

1. Clone este repositório para a sua máquina.
2. Abra o terminal na pasta do projeto e instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor:
   ```bash
   npm start
   ```
A API estará rodando em `http://localhost:3000`.

---

## 📌 Endpoints da API

| Método | Rota | Descrição | Status Sucesso | Status Erro |
|---|---|---|---|---|
| **POST** | `/login` | Autenticação (Usuário/Senha) | `200 OK` | `401 Unauthorized` |
| **GET** | `/jogos` | Retorna a lista completa de jogos | `200 OK` | - |
| **POST** | `/jogos` | Cadastra uma nova review | `201 Created` | `400 Bad Request` |
| **GET** | `/jogos/{id}` | Busca os detalhes de um jogo | `200 OK` | `404 Not Found` |
| **PUT** | `/jogos/{id}` | Atualiza todos os dados do jogo | `200 OK` | `400` ou `404` |
| **DELETE**| `/jogos/{id}` | Remove o jogo do sistema | `204 No Content`| `404 Not Found` |
| **POST** | `/reset` | *Rota Secreta:* Reseta a API para testes | `200 OK` | - |

---

## 🤖 Utilitário de Testes Automáticos (`testador.py`)

O projeto inclui um utilitário de Linha de Comando (CLI) feito em Python para auditar a API. Ele roda uma bateria de 14 testes cobrindo o **Caminho Feliz** (dados corretos) e o **Caminho Triste** (tentativas de quebrar o servidor com chaves erradas, ausentes ou credenciais inválidas).

### Pré-requisitos para os testes
Certifique-se de ter o Python 3 e a biblioteca `requests` instalados.
* No Windows: `pip install requests`
* No Linux (WSL/Ubuntu): `sudo apt install python3-requests`

### Como usar o Testador
O script exige que você informe a URL da API que deseja testar diretamente no comando do terminal.

**Para testar a API local:**
```bash
python3 testador.py http://localhost:3000
```

**Para testar uma API hospedada (Sua ou de um colega):**
```bash
python3 testador.py https://api-vercel-qc4y.onrender.com
```

### O que o script valida?
1. **Segurança:** Tenta logar sem senha, com senha errada e corpo vazio.
2. **Robustez (Erros 400):** Tenta criar jogos faltando o campo `review` ou enviando a chave com erro de digitação (`nom` em vez de `nome`).
3. **Persistência Real:** Após executar um `PUT` alterando o nome de um jogo, o script dispara um `GET` logo em seguida para comprovar se a alteração realmente ocorreu no banco de dados.
4. **Idempotência:** Tenta deletar um jogo duas vezes seguidas para garantir que a API devolva `404` na segunda tentativa.
