class Calculadora:
    def soma(self, a, b):
        return a + b
    
    def subtracao(self, a, b):
        return a - b


calc = Calculadora()

a = int(input("Digite o primeiro número: "))
b = int(input("Digite o segundo número: "))
operacao = input("Digite a operação (+ ou -): ")

if operacao == "+":
    resultado = calc.soma(a, b)
    print(f"Resultado da soma: {resultado}")
elif operacao == "-":
    resultado = calc.subtracao(a, b)
    print(f"Resultado da subtração: {resultado}")