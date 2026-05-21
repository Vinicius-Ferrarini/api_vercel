const express = require('express');
const { v4: uuidv4 } = require('uuid');
const cors = require('cors'); // Adicione esta linha junto com os outros requires

const app = express();

app.use(cors()); 
app.use(express.json()); // Permite que a API entenda JSON no body

// === ROTA DE LOGIN ===
app.post('/login', (req, res) => {
    const { email, password } = req.body || {};

    // Regra da atividade: verificar credenciais exatas
    if (email === "usuario@esoft.com" && password === "Abc123") {
        return res.status(200).json({ token: uuidv4() });
    }

    // Retorna erro 401 caso os dados estejam errados
    return res.status(401).json({ erro: "Credenciais inválidas" });
});

// --- NOSSA BASE DE DADOS EM MEMÓRIA ---
// Já iniciando com os dados que a atividade exige para facilitar
let jogos = [
    {
        "id": 1,
        "nome": "The Legend of Zelda",
        "tipo": "Aventura",
        "nota": 10,
        "review": "Um clássico absoluto."
    },
    {
        "id": 2,
        "nome": "FIFA 23",
        "tipo": "Esporte",
        "nota": 7,
        "review": "Bom para jogar com amigos."
    }
];

let proximoId = 3; // Controle para gerar o próximo ID no POST

// === ROTA: GET /jogos ===
// Retorna a lista completa de jogos
app.get('/jogos', (req, res) => {
    return res.status(200).json(jogos);
});

// === ROTA: POST /jogos ===
// Cadastra uma nova review
app.post('/jogos', (req, res) => {
    const { nome, tipo, nota, review } = req.body || {};

    // Validação para retornar 400 Bad Request se faltar algo
    if (!nome || !tipo || nota === undefined || !review) {
        return res.status(400).json({ erro: "Todos os campos são obrigatórios." });
    }

    const novoJogo = {
        id: proximoId++,
        nome,
        tipo,
        nota,
        review
    };

    jogos.push(novoJogo);

    // Retorna 201 Created com o objeto recém-criado
    return res.status(201).json(novoJogo);
});
// === ROTA: GET /jogos/{id} ===
// Busca detalhes de um jogo específico
app.get('/jogos/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const jogo = jogos.find(j => j.id === id);

    if (!jogo) {
        return res.status(404).json({ erro: "Jogo não encontrado." });
    }

    return res.status(200).json(jogo);
});

// === ROTA: PUT /jogos/{id} ===
// Atualiza todos os dados de um jogo
app.put('/jogos/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const { nome, tipo, nota, review } = req.body || {};

    // A regra exige que todos os campos sejam preenchidos
    if (!nome || !tipo || nota === undefined || !review) {
        return res.status(400).json({ erro: "Todos os campos são obrigatórios." });
    }

    const index = jogos.findIndex(j => j.id === id);

    if (index === -1) {
        return res.status(404).json({ erro: "Jogo não encontrado para atualização." });
    }

    // Atualiza o jogo na nossa lista
    jogos[index] = { id, nome, tipo, nota, review };

    return res.status(200).json(jogos[index]);
});

// === ROTA: DELETE /jogos/{id} ===
// Remove a review do sistema
app.delete('/jogos/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = jogos.findIndex(j => j.id === id);

    if (index === -1) {
        return res.status(404).json({ erro: "Jogo não encontrado para exclusão." });
    }

    // Remove 1 item a partir do index encontrado
    jogos.splice(index, 1);

    // Retorna 204 No Content (sem corpo de resposta, conforme a especificação)
    return res.status(204).send();
});

// === ROTA SECRETA PARA O TESTADOR AUTOMÁTICO ===
// Essa rota reseta a memória para o estado original
app.post('/reset', (req, res) => {
    jogos = [
        { "id": 1, "nome": "The Legend of Zelda", "tipo": "Aventura", "nota": 10, "review": "Um clássico absoluto." },
        { "id": 2, "nome": "FIFA 23", "tipo": "Esporte", "nota": 7, "review": "Bom para jogar com amigos." }
    ];
    proximoId = 3;
    return res.status(200).json({ mensagem: "API resetada para o estado inicial com sucesso!" });
});

// Inicialização do servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});