txt=str(input("Yazı yaz"))
a=str(input("Harf"))
con=0
for i in txt:
  if i==a:
    con+=1
print(con)