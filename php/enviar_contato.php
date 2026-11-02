<?php
header('Content-Type: application/json; charset=utf-8');

$host = 'localhost';
$user = 'root';
$pass = '';
$db   = 'curriculo';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Método inválido.']);
    exit;
}

$nome = trim($_POST['nome'] ?? '');
$email = trim($_POST['email'] ?? '');
$mensagem = trim($_POST['mensagem'] ?? '');

if ($nome === '' || $email === '' || $mensagem === '') {
    echo json_encode(['success' => false, 'message' => 'Preencha todos os campos.']);
    exit;
}

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    echo json_encode(['success' => false, 'message' => 'Erro de conexão com o banco de dados.']);
    exit;
}

$conn->set_charset('utf8mb4');

$stmt = $conn->prepare('INSERT INTO contatos (nome, email, mensagem, criado_em) VALUES (?, ?, ?, NOW())');
$stmt->bind_param('sss', $nome, $email, $mensagem);

if ($stmt->execute()) {
    echo json_encode(['success' => true, 'message' => 'Mensagem enviada com sucesso.']);
} else {
    echo json_encode(['success' => false, 'message' => 'Erro ao salvar no banco.']);
}

$stmt->close();
$conn->close();
?>
