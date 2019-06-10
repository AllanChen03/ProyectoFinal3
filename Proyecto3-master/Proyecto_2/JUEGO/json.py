import pickle

lista_usuarios = ["Allan","Mauricio"]

fichero_binario = open("lista_usuario","wb")

pickle.dump(lista_usuarios, fichero_binario)

fichero_binario.close()

del (fichero_binario)

ficheroApertura = open("lista_usuario", "rb")

usuarios = pickle.load(ficheroApertura)

ficheroApertura.close()

for c in usuarios:
    print(c)
