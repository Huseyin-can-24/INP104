while True:
  eier=int(input("Wieviele Eier"))
  if eier<6:
    print("ungültiger Wert")
    continue
  else:
    break
oniki=eier//12
print("Onikili kutu= "+ str(oniki))
kalan=eier%12
altili=kalan//6
kalan=altili%6
print("Altılı kutu= " + str(altili))
print("yemek için= " + str(kalan))