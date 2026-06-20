-- Criar banco de dados
CREATE DATABASE loja;
USE loja;

-- Criar tabela
CREATE TABLE produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    categoria VARCHAR(50),
    preco DECIMAL(10,2),
    estoque INT,
    fornecedor VARCHAR(100)
);

-- Inserir dados
INSERT INTO produtos (nome, categoria, preco, estoque, fornecedor) VALUES
('Arroz 5kg', 'Alimentos', 24.90, 50, 'Alimentos Brasil'),
('Feijao 1kg', 'Alimentos', 8.50, 80, 'Alimentos Brasil'),
('Macarrao', 'Alimentos', 4.20, 120, 'Massas Sul'),
('Detergente', 'Limpeza', 2.99, 60, 'Limpeza Total'),
('Sabao em Po', 'Limpeza', 15.50, 40, 'Limpeza Total'),
('Amaciante', 'Limpeza', 12.90, 35, 'Casa Limpa'),
('Shampoo', 'Higiene', 18.75, 25, 'Beleza Max'),
('Condicionador', 'Higiene', 19.90, 20, 'Beleza Max'),
('Pasta de Dente', 'Higiene', 6.50, 90, 'Sorriso Feliz'),
('Racao para Cachorro', 'Pet', 89.90, 15, 'Pet House');