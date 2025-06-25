import numpy as np
from random import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


import Algo as algo

####################################################
# Choix de la partie
print('Que souhaitez-vous faire ?')
print('1. Tester la décomposition SVD via un exemple')
print('2. Utiliser SVD pour la compression d’image sur une image de gris')
print('3. Utiliser SVD pour la compression d’image sur une image coloré carré')
print('4. Utiliser SVD pour la compression d’image sur une image coloré rectangle')
choixPartie = input('Choix : ')
###################################################

###################################################
if(choixPartie == '1'):
    print('Voulez-vous afficher à l’écran les matrices ?')
    print('1. Oui')
    print('2. Non')
    choixAffiche= input('Choix : ')
###################################################

###################################################
if(choixPartie == '1'):
    print('Quel type de matrice ?')
    print('1. Carré')
    print('2. Rectangulaire')
    choixExemple= input('Choix : ')
###################################################

####################################################
if(choixPartie == '1'):

	###############################################	
	if(choixExemple == '1'):
	
		#Initialisation :
		x = input("Entrez la taille de la matrice : ")
		n = int(x)
		p = min(n,n)
	
		#Construction de la matrice carrée A de l'exemple :
		diagonal = 2*np.ones(n)
		diagonal_sup_inf = -np.ones(n-1)
		A = np.diag(diagonal_sup_inf,-1) + np.diag(diagonal) + np.diag(diagonal_sup_inf,1)
	###############################################	
	
	###############################################		
	if(choixExemple == '2') :
		
		#Initialisation :
		x = input("Entrez le nombre de lignes de la matrice : ")
		n = int(x)
		y = input("Entrez le nombre de colonnes de la matrice :")
		m = int(y)
		
		#construction de la matrice rectangulaire A de l'exemple :
		sequence = np.arange(1, n * m + 1)
		A = sequence.reshape(n, m)
		A = np.array(A, dtype=float)
		#A = np.random.rand(n,m)
	###############################################
	
	###############################################
	#Affichage des matrices :
	
	#Fonction svd de python
	U1,s,V1 = np.linalg.svd(A)
	
	#Fonction svd 
	U,S,V,e = algo.svd(A,tol = 1e-15)
	###############################################
	
	###############################################
	if(choixAffiche == '1'):
	
		print("Matrice U:\n",U)
		print("Matrice U_python:\n",U1)
	
		print("\nMatrice V:\n",V)
		print("Matrice V_python:\n",U)
	
		print("\nMatrice S:\n",S)
		print("Vecteur S_python:\n",s)
		
		print("\nReconstitution USV^T:\n",U @ S @ V)
		print("Matrice A de départ:\n",A)
	###############################################
	
	###############################################
	#Calcul de l'erreur
	print("erreur:",e)
	###############################################
	
####################################################

####################################################
if(choixPartie == '2' or choixPartie == '3' or choixPartie == '4'):
    print('1. Compresser l’image')
    print('2. Afficher le graphe d’erreur')
    choixMéthode= input('Choix : ')
####################################################

####################################################
if(choixPartie == '2'):
	
	####################################################
	# Charger l'image en matrice
	img_gray = mpimg.imread("lena512.bmp")
	
	# Convertir l'image en flottants
	img_gray = img_gray.astype(float)
	
	#Extraire les paramètre lié à la matrice image
	n,m,p,t = algo.para(img_gray)	
	
	#Appliquer SVD
	U,S,V,e = algo.svd(img_gray,tol = 1e-8)
	####################################################
	
	####################################################
	if(choixMéthode == '1'):
		
		#Matrices compressé
		k = 100 #nombre de valeur singulière à garder
		U, S, V = algo.compress(U, S, V, k) #Reduit la taille des matrices U, S et V
	
		reconstructed_image = U @ S @ V 
		
		#met à jour la matrice avec des valeurs entre 0 et 255
		reconstructed_image = np.clip(reconstructed_image, 0, 255)
		
		#enregistre dans le dossier l'image
		mpimg.imsave("reconstructed_lena_gray.png", reconstructed_image.astype(np.uint8),cmap='gray')
	
		# Afficher l'image reconstruite
		plt.imshow(reconstructed_image.astype(np.uint8),cmap='gray')
		plt.axis('off')
		plt.show()
	####################################################
	
	####################################################
	if(choixMéthode == '2'):
		#Calcul l'erreur pour k allant de 0 à N_iter
		N_iter = 511
		er = np.zeros(N_iter)
		y = np.zeros(N_iter)
		for k in range(N_iter):
			U_k, S_k, V_k = algo.compress(U, S, V, k)
			reconstructed_image = U_k @ S_k @ V_k
			
			reconstructed_image = np.clip(reconstructed_image, 0, 255)
			y[k] = k
			er[k] = algo.calcul_error_compress(img_gray, reconstructed_image)	
		
		#Affiche le graphe d'erreur
		plt.plot(y,er)
		plt.ylabel("erreur")
		plt.xlabel("k")
		plt.yscale('log') #Echelle logarithme pour l'axe des ordonnées
		plt.show()
	####################################################
	
####################################################
	
####################################################
if(choixPartie == '3'):
	
	####################################################
	# Charger l'image couleur
	img_color = mpimg.imread("mandrill.bmp")

	# Convertir l'image en flottants
	img_color = img_color.astype(float)
	
	# Appliquer la SVD à chaque canal de couleur
	U_red, S_red, V_red, e_red = algo.svd(img_color[:,:,0], tol=1e-8)
	U_green, S_green, V_green, e_green = algo.svd(img_color[:,:,1], tol=1e-8)
	U_blue, S_blue, V_blue, e_blue = algo.svd(img_color[:,:,2], tol=1e-8)
	####################################################
	
	####################################################
	if(choixMéthode == '1'):

		# Nombre de valeurs singulières à conserver
		k = 100
		U_red, S_red, V_red = algo.compress(U_red, S_red, V_red, k)
		U_green, S_green, V_green = algo.compress(U_green, S_green, V_green, k)
		U_blue, S_blue, V_blue = algo.compress(U_blue, S_blue, V_blue, k)
		
		# Reconstruire chaque canal de couleur à partir de U, S et V
		reconstructed_red = U_red @ (S_red) @ V_red
		reconstructed_green = U_green @ (S_green) @ V_green
		reconstructed_blue = U_blue @ (S_blue) @ V_blue

		# Empiler les canaux de couleur pour obtenir l'image reconstruite
		reconstructed_image = np.stack((reconstructed_red, reconstructed_green, reconstructed_blue), axis=-1)

		# On s'assure que les valeurs de l'image reconstruite sont entre 0 et 255
		reconstructed_image = np.clip(reconstructed_image, 0, 255)

		# Enregistrer l'image reconstruite
		mpimg.imsave("reconstructed_mandrill_color.png", reconstructed_image.astype(np.uint8))

		# Afficher l'image reconstruite
		plt.imshow(reconstructed_image.astype(np.uint8))
		plt.axis('off')#Axe non nécessaire puisque ce n'est pas un graphe mais une image
		plt.show()
	####################################################
	
	####################################################
	if(choixMéthode == '2'):
	
		#Calcule l'erreur pour chaque canal
		N_iter = 510
		er_red = np.zeros(N_iter)
		er_blue = np.zeros(N_iter)
		er_green = np.zeros(N_iter)
		y = np.zeros(N_iter)
		for k in range(N_iter):
			U_redk, S_redk, V_redk = algo.compress(U_red, S_red, V_red, k)
			U_greenk, S_greenk, V_greenk = algo.compress(U_green, S_green, V_green, k)
			U_bluek, S_bluek, V_bluek = algo.compress(U_blue, S_blue, V_blue, k)
			
			# Reconstruire chaque canal de couleur à partir de U, S et V
			reconstructed_red = U_redk @ (S_redk) @ V_redk
			reconstructed_green = U_greenk @ (S_greenk) @ V_greenk
			reconstructed_blue = U_bluek @ (S_bluek) @ V_bluek
			
			y[k] = k
			er_red[k] = algo.calcul_error_compress(img_color[:,:,0], reconstructed_red)
			er_green[k] = algo.calcul_error_compress(img_color[:,:,1], reconstructed_green)
			er_blue[k] = algo.calcul_error_compress(img_color[:,:,2], reconstructed_blue)	
		
		plt.plot(y,er_red,color='red')#Affiche le graphe du canal rouge en rouge
		plt.plot(y,er_green,color='green')
		plt.plot(y,er_blue,color='blue')
		
		plt.ylabel("erreur")
		plt.xlabel("k")
		plt.yscale('log')#echelle log pour l'axe des ordonnées
		plt.show()
	####################################################
	
####################################################

####################################################
if(choixPartie == '4'):
	
	####################################################
	# Charger l'image couleur
	img_color = mpimg.imread("tigre.bmp")

	# Convertir l'image en flottants
	img_color = img_color.astype(float)
	
	# Appliquer la SVD à chaque canal de couleur
	U_red, S_red, V_red, e_red = algo.svd(img_color[:,:,0], tol=1e-8)
	U_green, S_green, V_green, e_green = algo.svd(img_color[:,:,1], tol=1e-8)
	U_blue, S_blue, V_blue, e_blue = algo.svd(img_color[:,:,2], tol=1e-8)
	####################################################
	
	####################################################
	if(choixMéthode == '1'):

		# Nombre de valeurs singulières à conserver
		k = 100
		U_red, S_red, V_red = algo.compress(U_red, S_red, V_red, k)
		U_green, S_green, V_green = algo.compress(U_green, S_green, V_green, k)
		U_blue, S_blue, V_blue = algo.compress(U_blue, S_blue, V_blue, k)
		
		# Reconstruire chaque canal de couleur à partir de U, S et V
		reconstructed_red = U_red @ (S_red) @ V_red
		reconstructed_green = U_green @ (S_green) @ V_green
		reconstructed_blue = U_blue @ (S_blue) @ V_blue

		# Empiler les canaux de couleur pour obtenir l'image reconstruite
		reconstructed_image = np.stack((reconstructed_red, reconstructed_green, reconstructed_blue), axis=-1)

		# On s'assure que les valeurs de l'image reconstruite sont entre 0 et 255
		reconstructed_image = np.clip(reconstructed_image, 0, 255)

		# Enregistrer l'image reconstruite
		mpimg.imsave("reconstructed_tigre_color.png", reconstructed_image.astype(np.uint8))

		# Afficher l'image reconstruite
		plt.imshow(reconstructed_image.astype(np.uint8))
		plt.axis('off')
		plt.show()
	####################################################
	
	####################################################
	if(choixMéthode == '2'):
	
		N_iter = 600
		er_red = np.zeros(N_iter)
		er_blue = np.zeros(N_iter)
		er_green = np.zeros(N_iter)
		y = np.zeros(N_iter)
		for k in range(N_iter):
			U_redk, S_redk, V_redk = algo.compress(U_red, S_red, V_red, k)
			U_greenk, S_greenk, V_greenk = algo.compress(U_green, S_green, V_green, k)
			U_bluek, S_bluek, V_bluek = algo.compress(U_blue, S_blue, V_blue, k)
			
			# Reconstruire chaque canal de couleur à partir de U, S et V
			reconstructed_red = U_redk @ (S_redk) @ V_redk
			reconstructed_green = U_greenk @ (S_greenk) @ V_greenk
			reconstructed_blue = U_bluek @ (S_bluek) @ V_bluek
			
			y[k] = k
			er_red[k] = algo.calcul_error_compress(img_color[:,:,0], reconstructed_red)
			er_green[k] = algo.calcul_error_compress(img_color[:,:,1], reconstructed_green)
			er_blue[k] = algo.calcul_error_compress(img_color[:,:,2], reconstructed_blue)	
		
		#Affiche les courbes correspondant aux 3 différents canaux
		plt.plot(y,er_red,color='red')
		plt.plot(y,er_green,color='green')
		plt.plot(y,er_blue,color='blue')
		
		plt.ylabel("erreur")
		plt.xlabel("k")
		plt.yscale('log')
		plt.show()
	####################################################
	
####################################################
