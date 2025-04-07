import geo
miktar=int(input("kaç tane minare?"))
r1=int(input("koni yaricapi?"))
h1=int(input("koni yükseklik?"))

r2=int(input("silindir yaricapi?"))
h2=int(input("silindir yükseklik?"))
result= miktar*geo.toplamHacim(r1,h1,r2,h2)
print(result)