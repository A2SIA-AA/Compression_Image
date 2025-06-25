# SVD-Image-Compression  
Application de la **décomposition en valeurs singulières (SVD)** pour la réduction de taille d’images.

> *Projet d’Analyse Numérique – GM3*  
> Doubli Hoda & Ait Taleb Assia – Février 2024

---

## 1. Contenu du dépôt

| Fichier / dossier                | Description                                                     |
|---------------------------------|-----------------------------------------------------------------|
| `algo.py`                       | Fonctions **puissance itérée**, **déflation** & **SVD maison**  |
| `main.py`                       | Script CLI : charge une image, choisit *k*, enregistre la sortie |
| `images`                       | Jeux d’essai : `lena512.bmp`, `mandrill.bmp`, `tigre.bmp`        |
| `report_SVD_Compression.pdf`    | Mémoire complet (21 pages)                                      |
| `README.md`                     | *vous y êtes*                                                   |

---

## 2. Rappels théoriques

| Section | Résumé |
|---------|--------|
| **2.1** | Valeurs propres/singulières ; matrices orthogonales, norme de Frobenius. |
| **2.3** | Théorème : `A = U Σ Vᵀ`.  U, V unitaires, Σ diag. |
| **2.4** | **Eckart-Young** : meilleure approx. de rang *k* ⇒ SVD tronquée. |
| **3**   | Implémentation Python : puissance itérée → déflation → SVD. |

---

## 3. Installation

```bash
python main.py
````

---

## 4. Résultats (extraits)

| Image                | k   | Facteur F | Erreur ‖·‖<sub>F</sub> | Aperçu                       |
| -------------------- | --- | --------- | ---------------------- | ---------------------------- |
| Lena (512×512)       | 100 | 2.54✕     | 4.7 e-2                | ![lena](lena512.bmp)    |
| Mandrill (512², RGB) | 120 | 4.3✕      | 5.3 e-2                | ![mandrill](mandrill.bmp) |
| Tigre (441×660, RGB) | 150 | 6.1✕      | 6.8 e-2                | ![tigre](tigre.bmp)  |

> On retrouve la chute rapide de l’erreur jusqu’à \~ k = 20 % du rang, puis un palier.
> Au-delà de la borne théorique k\* ≈ mn / (m+n+1), les arrondis flottants dégradent parfois l’image (pics d’erreur).

---

## 5. Limites connues

* **Mat. identité** ou rang plein → valeurs σ toutes égales : peu compressible.
* Erreurs d’arrondi pour k très proche du rang (voir rapport §3.5).

---

## 6. Références

* Golub & Kahan (1965) – algorithmique SVD
* Eckart & Young (1936) – approximation minimale de rang *k*
* Cours GM3 INSA Rouen – Algèbre linéaire & Analyse numérique
* Notes historiques : “On the early history of the SVD”

---

> *« Réduire les octets, garder l’essentiel » – la magie de la SVD.*

