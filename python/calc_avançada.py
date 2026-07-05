class Calculadora:
    def soma(self, a, b):
        return a + b
    
    def subtracao(self, a, b):
        return a - b
    
    def multiplicacao(self, a, b):
        return a * b
    
    def divisao(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Erro: Divisão por zero não é permitida."


calc = Calculadora()

a = int(input("Digite o primeiro número: "))
b = int(input("Digite o segundo número: "))
operacao = input("Digite a operação (+, -, * ou /): ")

if operacao == "+":
    resultado = calc.soma(a, b)
    print(f"Resultado da soma: {resultado}")
if operacao == "-":
    resultado = calc.subtracao(a, b)
    print(f"Resultado da subtração: {resultado}")
if operacao == "*":
    resultado = calc.multiplicacao(a, b)
    print(f"Resultado da multiplicação: {resultado}")
if operacao == "/":
    resultado = calc.divisao(a, b)
    print(f"Resultado da divisão: {resultado}")