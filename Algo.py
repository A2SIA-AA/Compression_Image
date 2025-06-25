import numpy as np

#################################################
#Algo puissance itérée :
#determine la plus grande valeur propre ainsi que son vecteur propre associé
def puissancei(A,tol):

	n = A.shape[0]
	x0 = np.arange(n)#initialise x0 en tant que vecteur aléatoire de taille n
	
	x0 = x0/np.sqrt(np.dot(x0,x0)) #normalisation du vecteur initial
	
	y = np.dot(A,x0)
	x1 = y/np.sqrt(np.dot(y,y))
	
	while (abs(abs(np.dot(x0,x1))-1) > tol):
		x0 = x1
		y = np.dot(A,x0)
		x1 = y/np.sqrt(np.dot(y,y))
		
		
	Lam = np.sqrt(np.dot(y,y))
	return Lam,x1
#################################################

#################################################
#Algorithme de déflation :
def deflation(A,p,tol) :
	#extrait le nombre de lignes de la matrice A :
	n = A.shape[0]
	
	#vecteur des valeurs propres :
	lam = np.zeros(p)
	
	#matrice des vecteurs propres :
	vect = np.zeros((n,p))
	
	#Calcul de la 1ère valeur propre en appelant la fonction puissance :
	lam[0], vect[:,0] = puissancei(A,tol)
	for k in range(1,p) :
		print("Ite : ",k)
		#calcul de la matrice déflattée A :
		A = A - (lam[k-1]) * np.outer(vect[:,k-1],vect[:,k-1])
		
		#calcul valeur et vecteur propre associé à la matrice déflatté A :
		lam[k], vect[:,k] = puissancei(A,tol)
		
	#retourne les valeurs et vecteurs propres calculées :
	return lam, vect
#################################################

#################################################
#Algo de SVD :
def svd(A,tol):

	n,m,p,t = para(A)#extrait de A les paramètres nécessaire
	
	S = np.zeros((n,m))#initialise une matrice de 0 de taille (n,m)
	S_inv = np.zeros((m,m))
	
	#construction de la matrice V :
	s, V = deflation(A.T @ A,m, tol)
	
	#construction de la matrice S et S_inv:
	for i in range(p):
		S[i,i] = np.sqrt(s[i])
		S_inv[i,i] = 1/np.sqrt(s[i])

	#construction de la matrice U :
	U = (A @ V @ S_inv)[:,:n]
	

	if t==True:
		e = calcul_error(A.T,V,S.T,U.T)
		
		return V, S.T, U.T, e
	
	e = calcul_error(A,U,S,V)
		
	return U, S, V.T, e

#################################################

#################################################
#Extrait de A les paramètre nécessaire :
def para(A):
	t = False
	n = A.shape[0] #nombre de lignes de A
	m = A.shape[1] #nombre de colonnes de A
	if n > m:
		t = True
		A = A.T
		n = A.shape[0]
		m = A.shape[1]	
	
	p = min(n,m) #nombre max de valeur propre pour une matrice n*m
	
	return n,m,p,t
#################################################


#################################################
#Calcule l'erreur pour les matrices de l'exemple :
def calcul_error(A, U, S, V):
	# Reconstruction de USV
	A1 = np.dot(U,np.dot(S,V))
	# Calcul de la norme
	error = np.linalg.norm(A1 - A,ord='fro')
	return error
#################################################

#################################################
#Caclule l'erreur de compression pour les matrices image
def calcul_error_compress(A, A_k):
	# Calcul de la norme
	no = np.linalg.norm(A - A_k,ord='fro')
	noA = np.linalg.norm(A,ord='fro')
	error = no/noA
	return error
#################################################

#################################################
#Reduit la taille des matrices U,S,V (k étant le nombre de valeur singulière à garder):
def compress(U, S, V, k):
    U_R = U[:,:k]
    S_R = S[:k,:k]
    V_R = V[:k,:]
    return U_R, S_R, V_R
#################################################
