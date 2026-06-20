

while True:
   print("opcao 1")
   print("opcao 2")
   print("opcao 3")

   cadastro=(int(input("digite seu numero: ")))

   if cadastro==1:
      print("ola mundo")
      for i in range(20,50, 2):
         print(i)
   elif cadastro==2:
      print("boa noite")
   elif cadastro==3:
      print("boa baixo")
   elif cadastro==4:
      break
