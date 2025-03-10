def toplama(a,b):
  toplama=a+b
  print(toplama)
def cikarma(a,b):
  cikarma=a-b
  print(cikarma)
def carpma(a,b):
  carpma=a*b
  print(carpma)
def bolme(a,b):
  bolme=a/b
  print(bolme)
while True: 
  a=int(input("Sayı1"))
  b=int(input("Sayı2"))
  operasyon=input("operasyon")
  if operasyon=="+":
    toplama(a,b)
  elif  operasyon=="-":
   cikarma(a,b)
  elif  operasyon=="*":
   carpma(a,b)
  elif  operasyon=="/":
   bolme(a,b)
  else:
   print("Hatalı İşlem")
  f=input("Devam mı?")
  if f=="Y" or f=="y":
   continue
  elif f=="N" or f=="n":
    break
  else:
    break
print("Ende")