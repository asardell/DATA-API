# Chapitre 1 – Prise en main de Python

## Objectifs

Voici les objectifs de ce chapitre :
- [ ] comprendre ce qui distingue Python de C++, C# et Java
- [ ] installer Python 3.12 et créer un environnement virtuel
- [ ] installer un package avec `pip` et lister les packages installés
- [ ] configurer Visual Studio Code pour Python
- [ ] créer et exécuter un notebook Jupyter
- [ ] manipuler les variables et les principaux types de données
- [ ] utiliser les listes et les dictionnaires
- [ ] écrire une condition, une boucle et une fonction simple

## Sommaire

- [Chapitre 1 – Prise en main de Python](#chapitre-1--prise-en-main-de-python)
  - [Objectifs](#objectifs)
  - [Sommaire](#sommaire)
  - [Introduction : Python pour un développeur C++, C# ou Java](#introduction--python-pour-un-développeur-c-c-ou-java)
  - [Préparation : installer Python, Visual Studio Code et l'environnement virtuel](#préparation--installer-python-visual-studio-code-et-lenvironnement-virtuel)
    - [Installer Python 3.12](#installer-python-312)
    - [Vérifier Python et pip](#vérifier-python-et-pip)
    - [Installer `virtualenv` (optionnel)](#installer-virtualenv-optionnel)
    - [Créer un environnement virtuel](#créer-un-environnement-virtuel)
    - [Activer et désactiver l’environnement](#activer-et-désactiver-lenvironnement)
    - [Installer des librairies dans l’environnement](#installer-des-librairies-dans-lenvironnement)
    - [Exporter les dépendances](#exporter-les-dépendances)
    - [Créer un second environnement pour test](#créer-un-second-environnement-pour-test)
    - [Utiliser Jupyer notebook en localhost](#utiliser-jupyer-notebook-en-localhost)
    - [Notebooks interactifs dans VS Code](#notebooks-interactifs-dans-vs-code)
    - [Créer un notebook interactif](#créer-un-notebook-interactif)
  - [Exercice 1 – Premier script et syntaxe](#exercice-1--premier-script-et-syntaxe)
    - [Mémo](#mémo)
    - [Exemple](#exemple)
    - [Exercices](#exercices)
  - [Exercice 2 – Variables et types de données](#exercice-2--variables-et-types-de-données)
    - [Mémo](#mémo-1)
    - [Exemple](#exemple-1)
    - [Exercices](#exercices-1)
  - [Exercice 3 – Listes](#exercice-3--listes)
    - [Mémo](#mémo-2)
    - [Exemple](#exemple-2)
    - [Exercices](#exercices-2)
  - [Exercice 4 – Dictionnaires](#exercice-4--dictionnaires)
    - [Mémo](#mémo-3)
    - [Exemple](#exemple-3)
    - [Exercices](#exercices-3)
  - [Exercice 5 – Conditions et boucles](#exercice-5--conditions-et-boucles)
    - [Mémo](#mémo-4)
    - [Exemple](#exemple-4)
    - [Exercices](#exercices-4)
  - [Exercice 6 – Fonctions](#exercice-6--fonctions)
    - [Mémo](#mémo-5)
    - [Exemple](#exemple-5)
    - [Exercices](#exercices-5)
  - [Exercice 7 – Premier notebook Jupyter](#exercice-7--premier-notebook-jupyter)
    - [Créer le notebook dans VS Code](#créer-le-notebook-dans-vs-code)
    - [Exercices](#exercices-6)
  - [Liens utiles](#liens-utiles)

## Introduction : Python pour un développeur C++, C# ou Java

**Python** est un langage de haut niveau, interprété, dont la syntaxe est volontairement lisible. Il est utilisé pour les scripts d'automatisation, les applications web, les API et, surtout, l'analyse de données. Son écosystème compte des bibliothèques de référence comme `pandas` (tableaux de données), `requests` (appels HTTP) ou `FastAPI` (création d'API).

Pour un développeur qui vient de C++, C# ou Java, les concepts sont les mêmes : variables, fonctions, boucles, structures de données. Ce qui change, ce sont surtout les habitudes d'écriture :

| Sujet | C++ / C# / Java | Python |
|-------|-----------------|--------|
| Blocs de code | accolades `{ }` | indentation (4 espaces) |
| Fin d'instruction | `;` | fin de ligne |
| Déclaration de type | obligatoire (`int x = 5;`) | non : `x = 5` suffit |
| Commentaire | `//` ou `/* */` | `#` |
| Valeur absente | `null` | `None` |
| Affichage | `Console.WriteLine`, `System.out.println`, `cout` | `print()` |
| Opérateurs logiques | `&&`, `\|\|`, `!` | `and`, `or`, `not` |

Deux points à retenir dès le début :
- **L'indentation fait partie de la syntaxe** : un bloc de code est défini par son décalage, pas par des accolades. Une mauvaise indentation provoque une erreur.
- **Le typage est dynamique** : une variable n'a pas de type fixé à sa déclaration. C'est la valeur affectée qui porte le type.

Les exemples de ce chapitre utilisent des **DPE (diagnostics de performance énergétique) fictifs**, dans le même format que les données de l'API ADEME. Les chapitres suivants interrogent les vraies données.

## Préparation : installer Python, Visual Studio Code et l'environnement virtuel

### Installer Python 3.12

Sous Windows, le lanceur `py` permet de choisir la version de Python à utiliser. Pour afficher les versions installées :

```powershell
py -0p
```

Si la version 3.12 n'est pas présente, l'installer depuis [python.org](https://www.python.org/downloads/). Vérifier ensuite :

```powershell
py -3.12 --version
# Python 3.12.x
```

Les environnements virtuels permettent d'isoler les dépendances Python pour chaque projet.  
Cela évite les conflits de version et garantit que le projet fonctionne toujours avec les bonnes librairies.


<p align="center">
  <img src="https://www.dataquest.io/wp-content/uploads/2022/01/python-virtual-envs1.webp" alt="Source de l'image" width="600"/>
</p>

### Vérifier Python et pip

Avant de créer un environnement virtuel, vérifiez que Python 3 est installé :

```bash
python --version
# ou
python -V
```

Vérifiez le chemin d'installation de Python :

```bash
where python   # Windows
which python   # Linux / MacOS
```

Listez les librairies Python déjà installées :

```bash
pip list
```


### Installer `virtualenv` (optionnel)

:warning: Si vous avez plusieurs versions de python installé. Vous pouvez choisir avec quelle version vous souhaitez lancer les commandes : 

```bash
py -0p # vous indique les versions disponible
py -3.10 --version # selon votre version qui s'affiche
```

sert à afficher toutes les installations Python détectées par le lanceur `Windows py`, ainsi que leur chemin.

Python 3 inclut `venv`, mais `virtualenv` peut être utilisé pour plus de flexibilité :

```bash
pip install virtualenv
pip list  # vérifier que virtualenv est bien installé
```


### Créer un environnement virtuel

Positionnez-vous dans le dossier où vous souhaitez créer votre environnement :

```bash
cd C:/Users/Anthony/Documents/my_virtual_envs
```

Créez l'environnement appelé `env-ademe` :

```bash
py -m venv env-ademe
#ou
py -3.10 -m venv env-ademe # pour choisir la bonne version python a utiliser
```

- `-m venv` indique à Python d’exécuter le module `venv` comme script.
- ⚠️ **Ne pas créer l’environnement dans le dossier du projet** pour éviter d’inclure des fichiers temporaires. Sauf si on veut utiliser Jupyter en localhost ou intéractif ([voir plus bas](#utiliser-jupyer-notebook-en-localhost))


### Activer et désactiver l’environnement

Windows (cmd) :

```bash
cd ./env-ademe/Scripts
activate.bat
```

Linux / MacOS (bash) :

```bash
source env-ademe/bin/activate
```

Pour désactiver l’environnement :

```bash
deactivate
```

Vérifiez que l’environnement est activé et les packages installés :

```bash
pip list
```


### Installer des librairies dans l’environnement

Exemple pour Pandas et NumPy :

```bash
pip install numpy pandas matplotlib
pip list  # vérifier l'installation
```


### Exporter les dépendances

Pour partager ou recréer un environnement, exportez les dépendances dans un fichier `requirements.txt` :

```bash
cd C:/Users/Anthony/Documents/my_virtual_envs
pip freeze > requirements.txt
```

- ⚠️ **Ne pas créer `requirements.txt` dans le dossier de l’environnement**, mais dans le dossier de votre projet.

Pour installer les dépendances sur un autre environnement :

```bash
pip install -r C:/Users/Anthony/Documents/my_virtual_envs/requirements.txt
```


### Créer un second environnement pour test

:warning: Pour que VS Code détecte automatiquement vos environnements virtuels, il est conseillé de créer votre environnement virtuel dans votre dossier projet.


```bash
cd C:/Users/Anthony/Documents/Formation
py -3.10 -m venv test-env
cd ./test-env/Scripts/activate  # ou activate.bat sous Windows
cd C:/Users/Anthony/Documents/my_virtual_envs
pip install -r requirements.txt
pip list  # vérifier que toutes les librairies sont bien installées
```


### Utiliser Jupyer notebook en localhost

1. Ouvrez VS Code dans votre projet.
2. Ouvrez le terminal intégré (cmd ou PowerShell).
3. Activez votre environnement virtuel comme montré précédemment.
4. Vérifiez que VS Code utilise l’interpréteur Python de l’environnement activé.

:bulb:  Pour une utilisation de Jupyter dans VS Code, installer également `ipykernel` après avoir activité l'environnement `env-ademe` :

```cmd
pip install notebook
pip install ipykernel
jupyter notebook
```

### Notebooks interactifs dans VS Code

Installer les extensions nécessaires

1. Ouvre VS Code et va dans **Extensions** (Ctrl+Shift+X).  
2. Installe **Python** (par Microsoft).  
3. Installe **Jupyter** (par Microsoft).  

Ces deux extensions sont indispensables pour travailler avec des notebooks interactifs.

### Créer un notebook interactif

1. Appuie sur **Ctrl+Shift+P** → tape `Jupyter: Create New Blank Notebook`.  
2. Choisis le **kernel** correspondant à ton environnement Python (ex. `env-ademe`).  
3. Si ton environnement n'apparaît pas dans la liste (ex. un venv situé en dehors du dossier ouvert), appuie sur **Ctrl+Shift+P** → tape `Python: Select Interpreter` → **Enter interpreter path...** → indique le chemin vers `python.exe` de ton venv, par exemple `C:\Users\Anthony\Documents\Formation\test-env\Scripts\python.exe`.  

## Exercice 1 – Premier script et syntaxe

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `print()` | Affiche une ou plusieurs valeurs dans la console. | `print("Bonjour")` |
| `#` | Commentaire : tout ce qui suit sur la ligne est ignoré. | `# surface en m²` |
| f-string `f"..."` | Insère une variable dans une chaîne avec `{ }`. | `f"Surface : {surface} m²"` |
| `type()` | Retourne le type d'une valeur. | `type(62.7)` |

### Exemple

Créer un fichier `premier_script.py` dans le dossier du projet, puis l'exécuter avec `python premier_script.py` :

```python
# Un commentaire commence par #
prenom = "Anthony"
print("Bonjour", prenom)

# Une f-string insère la valeur d'une variable entre accolades
surface = 62.7
print(f"Surface du logement : {surface} m²")
```

Résultat :

```text
Bonjour Anthony
Surface du logement : 62.7 m²
```

### Exercices

1. Afficher la phrase `Formation DATA-API` avec `print()`.
<details>
<summary>Correction</summary>

```python
print("Formation DATA-API")
```
</details>

2. Calculer la surface d'un logement rectangulaire de 7,5 m de large et 8,4 m de long, puis afficher le résultat avec une f-string sous la forme `Surface : 63.0 m²`. Arrondir à deux décimales avec `round(valeur, 2)`.
<details>
<summary>Correction</summary>

```python
largeur = 7.5
longueur = 8.4
surface = round(largeur * longueur, 2)
print(f"Surface : {surface} m²")
# Surface : 63.0 m²
```
</details>

3. Que produit le code suivant ? Corriger l'erreur.
```python
if True:
print("Le bloc est exécuté")
```
<details>
<summary>Correction</summary>

Le code provoque une erreur : `IndentationError: expected an indented block`. La ligne `print` doit être décalée sous le `if` :

```python
if True:
    print("Le bloc est exécuté")
```
</details>

> **Note : les commentaires**
> En Java ou en C#, un commentaire utilise `//`. En Python, c'est `#`. Les docstrings (chaînes entre `"""`) servent à documenter une fonction, voir l'exercice 6.

## Exercice 2 – Variables et types de données

Une **variable** est un nom qui référence une valeur. Le type n'est pas déclaré : Python le déduit de la valeur. Les types de base sont `int` (entier), `float` (nombre à virgule), `str` (texte), `bool` (`True` ou `False`) et `NoneType` (`None`, absence de valeur).

### Mémo

| Nom de la commande | Description | Exemple | Résultat |
|--------------------|-------------|---------|----------|
| `type()` | Retourne le type d'une valeur. | `type(3)` | `<class 'int'>` |
| `int()` | Convertit en entier. | `int("3")` | `3` |
| `float()` | Convertit en nombre à virgule. | `float("62.7")` | `62.7` |
| `str()` | Convertit en texte. | `str(3)` | `"3"` |
| `/` | Division, renvoie toujours un `float`. | `7 / 2` | `3.5` |
| `//` | Division entière. | `7 // 2` | `3` |
| `%` | Reste de la division. | `7 % 2` | `1` |

### Exemple

```python
surface = 62.7          # float
nb_pieces = 3           # int
etiquette = "D"         # str
est_collectif = False   # bool
commentaire = None      # NoneType

print(type(surface))        # <class 'float'>
print(type(nb_pieces))      # <class 'int'>
print(type(commentaire))    # <class 'NoneType'>

# Conversion : une valeur lue dans un fichier est souvent du texte
texte = "62.7"
print(float(texte) * 2)     # 125.4
print(texte * 2)            # 62.762.7 : la multiplication répète le texte
```

### Exercices

1. Afficher le type des variables `nb_pieces` et `est_collectif` avec `type()`.
<details>
<summary>Correction</summary>

```python
print(type(nb_pieces))       # <class 'int'>
print(type(est_collectif))   # <class 'bool'>
```
</details>

2. La valeur `"62.7"` est lue sous forme de texte. Calculer le double de sa valeur numérique.
<details>
<summary>Correction</summary>

```python
texte = "62.7"
double = float(texte) * 2
print(double)   # 125.4
```
</details>

3. Calculer `7 / 2`, `7 // 2` et `7 % 2`. Donner le type du résultat de `7 / 2`.
<details>
<summary>Correction</summary>

```python
print(7 / 2)    # 3.5
print(7 // 2)   # 3
print(7 % 2)    # 1
print(type(7 / 2))  # <class 'float'>
```
</details>

> **Note : `/` et `//`**
> En C++, C# ou Java, la division de deux entiers donne un entier. En Python 3, `/` donne toujours un `float`. Pour une division entière, utiliser `//`.

## Exercice 3 – Listes

Une **liste** est une suite ordonnée d'éléments, modifiable. Elle se crée avec `[ ]`. Comme en C#, les positions commencent à **0**. Une position négative compte depuis la fin : `-1` désigne le dernier élément.

### Mémo

| Nom de la commande | Description | Exemple | Résultat |
|--------------------|-------------|---------|----------|
| `[ ]` | Crée une liste. | `[21.3, 62.7]` | |
| `len()` | Retourne le nombre d'éléments. | `len(surfaces)` | `5` |
| `liste[i]` | Accède à l'élément de position `i`. | `surfaces[0]` | `21.3` |
| `liste[a:b]` | Extrait les éléments de `a` (inclus) à `b` (exclu). | `surfaces[1:3]` | `[62.7, 56.8]` |
| `append()` | Ajoute un élément à la fin. | `surfaces.append(90.1)` | |
| `extend()` | Ajoute tous les éléments d'une autre liste à la fin. | `surfaces.extend([88.0, 30.5])` | |
| `remove()` | Supprime la première occurrence d'une valeur. | `surfaces.remove(21.3)` | |
| `in` | Teste la présence d'une valeur. | `"D" in etiquettes` | `True` |
| `sum()`, `min()`, `max()` | Somme, minimum et maximum. | `sum(surfaces)` | |

### Exemple

```python
surfaces = [21.3, 62.7, 56.8, 76.6, 45.0]

print(len(surfaces))      # 5
print(surfaces[0])        # 21.3 : premier élément
print(surfaces[-1])       # 45.0 : dernier élément
print(surfaces[1:3])      # [62.7, 56.8]

surfaces.append(90.1)     # ajout en fin de liste
print(surfaces)           # [21.3, 62.7, 56.8, 76.6, 45.0, 90.1]

# extend() ajoute chaque élément d'une autre liste
lots = [1, 2]
lots.extend([3, 4])
print(lots)               # [1, 2, 3, 4]
```

### Exercices

1. Dans la liste `surfaces` de l'exemple, afficher le troisième élément, puis tous les éléments sauf le premier.
<details>
<summary>Correction</summary>

```python
print(surfaces[2])    # 56.8
print(surfaces[1:])   # [62.7, 56.8, 76.6, 45.0, 90.1]
```
</details>

2. Calculer la surface moyenne des logements de la liste `[21.3, 62.7, 56.8, 76.6, 45.0]`, sans utiliser `append()`.
<details>
<summary>Correction</summary>

```python
surfaces = [21.3, 62.7, 56.8, 76.6, 45.0]
moyenne = sum(surfaces) / len(surfaces)
print(moyenne)   # 52.48
```
La somme vaut 262.4 et il y a 5 éléments : 262.4 / 5 = 52.48.
</details>

3. Ajouter `90.1` à la liste, puis supprimer la valeur `21.3`. Afficher la liste et sa longueur.
<details>
<summary>Correction</summary>

```python
surfaces = [21.3, 62.7, 56.8, 76.6, 45.0]
surfaces.append(90.1)
surfaces.remove(21.3)
print(surfaces)        # [62.7, 56.8, 76.6, 45.0, 90.1]
print(len(surfaces))   # 5
```
</details>

4. Vérifier avec `in` que la valeur `62.7` appartient à la liste, puis que `100.0` n'y appartient pas.
<details>
<summary>Correction</summary>

```python
print(62.7 in surfaces)     # True
print(100.0 in surfaces)    # False
```
</details>

> **Note : les listes sont modifiables**
> `append()`, `extend()` et `remove()` modifient la liste elle-même, elles ne renvoient rien. Écrire `surfaces = surfaces.append(90.1)` met `None` dans la variable : c'est une erreur fréquente quand on vient d'un autre langage.
>
> `append()` ajoute la liste entière comme **un seul** élément, `extend()` ajoute **chaque** élément : `[1, 2].append([3, 4])` donne `[1, 2, [3, 4]]`, alors que `[1, 2].extend([3, 4])` donne `[1, 2, 3, 4]`.

### Ensembles : `set`

Un **ensemble** (`set`) est une collection **sans doublon** et **sans ordre**. On ne peut pas accéder à un élément par sa position (`ensemble[0]` provoque une erreur). Il sert surtout à comparer deux collections : union, intersection, différence. Une liste se convertit en ensemble avec `set()`.

> **Attention :** `{ }` crée un **dictionnaire** vide, pas un ensemble. Pour un ensemble vide, écrire `set()`.

| Opération | Syntaxe | Équivalent méthode | Résultat : éléments dans... |
|-----------|---------|--------------------|-----------------------------|
| Union | `a \| b` | `a.union(b)` | a **ou** b |
| Intersection | `a & b` | `a.intersection(b)` | a **et** b |
| Différence | `a - b` | `a.difference(b)` | a **mais pas** b |
| Nombre d'éléments distincts | `len(a)` | | |

### Exemple

```python
a = [21.3, 62.7, 56.8, 62.7]   # 62.7 apparaît deux fois
b = [62.7, 76.6, 45.0]

sa = set(a)                     # doublon supprimé
sb = set(b)

print(len(sa))                  # 3
print(sorted(sa | sb))          # union : [21.3, 45.0, 56.8, 62.7, 76.6]
print(sorted(sa & sb))          # intersection : [62.7]
print(sorted(sa - sb))          # différence : [21.3, 56.8]
```

`sorted()` sert ici à afficher les éléments dans un ordre stable, car un `set` n'a pas d'ordre garanti.

### Exercices (suite)

5. Avec `a` et `b` de l'exemple, calculer les éléments qui sont dans `b` mais pas dans `a` (différence `b - a`), en affichant le résultat trié.
<details>
<summary>Correction</summary>

```python
a = [21.3, 62.7, 56.8, 62.7]
b = [62.7, 76.6, 45.0]

print(sorted(set(b) - set(a)))   # [45.0, 76.6]
```
</details>

6. Combien de logements distincts y a-t-il dans la liste `[21.3, 62.7, 56.8, 62.7, 21.3]` ? Répondre avec un `set`, puis vérifier avec `len()` sur la liste d'origine.
<details>
<summary>Correction</summary>

```python
valeurs = [21.3, 62.7, 56.8, 62.7, 21.3]

print(len(set(valeurs)))   # 3 valeurs distinctes
print(len(valeurs))        # 5 éléments au total
```
</details>

## Exercice 4 – Dictionnaires

Un **dictionnaire** associe des **clés** à des **valeurs**, comme une `Dictionary<string, object>` en C# ou une `Map` en Java. Il se crée avec `{ }`. Il représente bien un enregistrement : un DPE, une ligne d'une réponse d'API.

### Mémo

| Nom de la commande | Description | Exemple | Résultat |
|--------------------|-------------|---------|----------|
| `{ }` | Crée un dictionnaire. | `{"etiquette_dpe": "D"}` | |
| `d[cle]` | Lit la valeur associée à une clé. Erreur `KeyError` si la clé est absente. | `logement["etiquette_dpe"]` | `"D"` |
| `d.get(cle, defaut)` | Lit la valeur, ou renvoie `defaut` si la clé est absente. | `logement.get("annee", "inconnue")` | `"inconnue"` |
| `d[cle] = valeur` | Ajoute une clé ou modifie sa valeur. | `logement["annee"] = 1948` | |
| `keys()`, `values()`, `items()` | Parcourt les clés, les valeurs ou les couples. | `logement.items()` | |
| `in` | Teste la présence d'une clé. | `"annee" in logement` | `False` |

### Exemple

```python
logement = {
    "numero_dpe": "EXEMPLE-0001",
    "code_postal_ban": "69100",
    "surface_habitable_logement": 62.7,
    "etiquette_dpe": "D",
}

print(logement["etiquette_dpe"])                 # D
print(logement.get("annee", "non renseignée"))   # non renseignée

logement["etiquette_ges"] = "C"                  # ajout d'une clé
for cle, valeur in logement.items():
    print(f"{cle} : {valeur}")
```

### Exercices

1. Afficher la surface habitable du logement de l'exemple.
<details>
<summary>Correction</summary>

```python
print(logement["surface_habitable_logement"])   # 62.7
```
</details>

2. Essayer `logement["annee"]`, puis récupérer la même information avec `get()` et la valeur par défaut `"non renseignée"`. Quelle est la différence ?
<details>
<summary>Correction</summary>

```python
logement["annee"]                           # KeyError: 'annee'
print(logement.get("annee", "non renseignée"))   # non renseignée
```
`logement["annee"]` lève une exception si la clé n'existe pas. `get()` ne lève rien et renvoie la valeur par défaut. Cette différence servira au chapitre 2 pour lire des réponses d'API qui ne contiennent pas toujours tous les champs.
</details>

3. Ajouter la clé `"annee_construction"` avec la valeur `1948`, puis afficher le dictionnaire.
<details>
<summary>Correction</summary>

```python
logement["annee_construction"] = 1948
print(logement)
```
</details>

4. Créer une liste de deux dictionnaires de DPE fictifs, avec les clés `numero_dpe` et `etiquette_dpe`. Afficher le numéro de chaque DPE avec une boucle `for`.
<details>
<summary>Correction</summary>

```python
dpe_fictifs = [
    {"numero_dpe": "EXEMPLE-0002", "etiquette_dpe": "B"},
    {"numero_dpe": "EXEMPLE-0003", "etiquette_dpe": "F"},
]

for dpe in dpe_fictifs:
    print(dpe["numero_dpe"])
```
</details>

> **Note : une réponse d'API est souvent une liste de dictionnaires**
> La liste `dpe_fictifs` a la même forme qu'une réponse JSON contenant plusieurs enregistrements. Les chapitres 2 et 3 reprennent cette structure.

## Exercice 5 – Conditions et boucles

Les conditions et les boucles fonctionnent comme dans les autres langages, à deux différences près : pas de parenthèses obligatoires autour de la condition, et un bloc défini par son indentation. `range(n)` génère les entiers de 0 à `n - 1`.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `if` / `elif` / `else` | Exécute un bloc selon une condition. | `if surface > 50:` |
| `for ... in` | Parcourt les éléments d'une séquence. | `for etiquette in etiquettes:` |
| `range()` | Génère une suite d'entiers. | `range(1, 4)` donne 1, 2, 3 |
| `enumerate()` | Parcourt une liste en donnant aussi la position. | `for i, x in enumerate(liste):` |
| `while` | Répète un bloc tant qu'une condition est vraie. | `while page <= 3:` |
| `break` | Sort de la boucle en cours. | |

### Exemple

```python
etiquette = "D"

if etiquette in ["A", "B", "C"]:
    print("Logement économe")
elif etiquette == "D":
    print("Logement moyen")
else:
    print("Logement énergivore")

for etiquette in ["A", "E", "G"]:
    print(etiquette)

page = 1
while page <= 3:
    print(f"Lecture de la page {page}")
    page += 1

# enumerate() donne la position et la valeur à chaque tour
etiquettes = ["A", "E", "D"]
for i, etiquette in enumerate(etiquettes):
    print(i, etiquette)
```

Résultat de la dernière boucle :

```text
0 A
1 E
2 D
```

`enumerate()` commence à compter à **0**, comme les positions d'une liste. Pour commencer à 1, écrire `enumerate(etiquettes, start=1)`.

### Exercices

1. Écrire une condition qui affiche `Passoire énergétique` si l'étiquette est `E`, `F` ou `G`, et `Pas une passoire` sinon. Tester avec les étiquettes `"B"` et `"F"`.
<details>
<summary>Correction</summary>

```python
for etiquette in ["B", "F"]:
    if etiquette in ["E", "F", "G"]:
        print("Passoire énergétique")
    else:
        print("Pas une passoire")
# Pas une passoire
# Passoire énergétique
```
</details>

2. Pour la liste `etiquettes = ["A", "E", "D", "G", "C"]`, compter le nombre de passoires énergétiques avec une boucle `for` et une variable `compteur`.
<details>
<summary>Correction</summary>

```python
etiquettes = ["A", "E", "D", "G", "C"]
compteur = 0
for etiquette in etiquettes:
    if etiquette in ["E", "F", "G"]:
        compteur += 1
print(compteur)   # 2
```
</details>

3. Simuler la lecture de 5 pages avec une boucle `for` et `range()`, en affichant `Page 1` à `Page 5`.
<details>
<summary>Correction</summary>

```python
for page in range(1, 6):
    print(f"Page {page}")
```
`range(1, 6)` donne 1, 2, 3, 4, 5 : la borne haute est exclue.
</details>

4. Pour la liste `etiquettes = ["A", "E", "D", "G", "C"]`, afficher chaque étiquette avec sa position en commençant à 1, sous la forme `1 - A`, avec `enumerate()`.
<details>
<summary>Correction</summary>

```python
etiquettes = ["A", "E", "D", "G", "C"]
for position, etiquette in enumerate(etiquettes, start=1):
    print(f"{position} - {etiquette}")
# 1 - A
# 2 - E
# 3 - D
# 4 - G
# 5 - C
```
</details>

> **Note : `range()` exclut sa borne haute**
> `range(1, 6)` ne contient pas 6. Cette règle sert pour les boucles sur les pages d'une API : pour les pages 1 à 5, il faut écrire `range(1, 6)`.

## Exercice 6 – Fonctions

Une fonction se définit avec `def`. Son corps est indenté. Elle peut recevoir des paramètres, avec ou sans valeur par défaut, et renvoie un résultat avec `return`. La première ligne de la fonction peut être une **docstring**, une chaîne entre `"""` qui documente son rôle.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `def` | Définit une fonction. | `def somme(a, b):` |
| `return` | Renvoie une valeur et termine la fonction. | `return a + b` |
| Paramètre par défaut | Valeur utilisée si l'argument n'est pas fourni. | `def arrondir(x, n=2):` |
| `round()` | Arrondit un nombre à `n` décimales. | `round(62.756, 1)` donne `62.8` |

### Exemple

```python
def surface_moyenne(surfaces, decimales=2):
    """Renvoie la surface moyenne d'une liste de surfaces, arrondie."""
    return round(sum(surfaces) / len(surfaces), decimales)

surfaces = [21.3, 62.7, 56.8]
print(surface_moyenne(surfaces))       # 46.93
print(surface_moyenne(surfaces, 0))    # 47.0
```

### Exercices

1. Écrire une fonction `est_passoire(etiquette)` qui renvoie `True` si l'étiquette est `E`, `F` ou `G`, et `False` sinon. Tester avec `"B"` et `"G"`.
<details>
<summary>Correction</summary>

```python
def est_passoire(etiquette):
    """Renvoie True si l'étiquette DPE est E, F ou G."""
    return etiquette in ["E", "F", "G"]

print(est_passoire("B"))   # False
print(est_passoire("G"))   # True
```
</details>

2. Écrire une fonction `compter_passoires(etiquettes)` qui renvoie le nombre de passoires dans une liste, en réutilisant `est_passoire()`. Tester avec `["A", "E", "D", "G", "C"]`.
<details>
<summary>Correction</summary>

```python
def compter_passoires(etiquettes):
    """Renvoie le nombre d'étiquettes E, F ou G dans la liste."""
    compteur = 0
    for etiquette in etiquettes:
        if est_passoire(etiquette):
            compteur += 1
    return compteur

print(compter_passoires(["A", "E", "D", "G", "C"]))   # 2
```
</details>

3. Appeler `surface_moyenne()` avec la liste `[21.3, 62.7, 56.8]` avec la valeur par défaut, puis avec `decimales=1`.
<details>
<summary>Correction</summary>

```python
surfaces = [21.3, 62.7, 56.8]
print(surface_moyenne(surfaces))      # 46.93
print(surface_moyenne(surfaces, 1))   # 46.9
```
</details>

> **Note : paramètres par défaut**
> Un paramètre avec une valeur par défaut doit être placé après les paramètres obligatoires : `def f(a, b=2)` est valide, `def f(a=2, b)` provoque une erreur. Les paramètres nommés (`decimales=1`) rendent l'appel plus lisible.

## Exercice 7 – Premier notebook Jupyter

Un **notebook Jupyter** découpe le code en cellules. Chaque cellule s'exécute séparément, et les variables restent en mémoire d'une cellule à l'autre. Il est utile pour explorer des données, alors qu'un script `.py` est exécuté d'un seul bloc.

### Créer le notebook dans VS Code

1. Dans le dossier du projet, créer un fichier `exercices_chapitre_1.ipynb`, ou utiliser `Ctrl + Maj + P`, puis `Jupyter: Create New Blank Notebook`.
2. Choisir le **kernel** `env-ademe` (l'environnement créé dans la préparation) quand VS Code le demande. Le kernel est l'interpréteur Python qui exécute les cellules.
3. Ajouter une cellule de code avec le bouton **+ Code**, écrire le code, puis l'exécuter avec `Maj + Entrée`.

### Exercices

1. Dans une première cellule, créer la variable `surface = 62.7`. Dans une deuxième cellule, afficher `surface * 2`. Exécuter les deux cellules dans l'ordre.
<details>
<summary>Correction</summary>

Cellule 1 :
```python
surface = 62.7
```

Cellule 2 :
```python
print(surface * 2)   # 125.4
```
</details>

2. Exécuter la deuxième cellule avant la première, dans une session fraîche (menu du notebook : redémarrer le kernel). Que se passe-t-il ?
<details>
<summary>Correction</summary>

Python signale `NameError: name 'surface' is not defined`. La variable n'existe pas encore : elle n'est créée que lorsque la première cellule est exécutée.
</details>

3. Importer les fonctions `est_passoire()` et `compter_passoires()` de l'exercice 6 dans des cellules du notebook, puis tester `compter_passoires(["E", "F", "A"])`.
<details>
<summary>Correction</summary>

Recopier les deux fonctions dans une cellule, puis ajouter une cellule :

```python
print(compter_passoires(["E", "F", "A"]))   # 2
```
</details>

> **Note : l'ordre d'exécution**
> Dans un notebook, l'ordre d'exécution des cellules peut différer de l'ordre d'affichage. Une cellule qui fonctionne seulement parce qu'une autre a été lancée avant peut donner un résultat faux une fois le notebook relancé du début. Pour vérifier un notebook, utiliser `Redémarrer` puis `Tout exécuter`.

## Liens utiles

- [Tutoriel officiel Python](https://docs.python.org/fr/3/tutorial/)
- [Documentation Python : types natifs (listes, dictionnaires)](https://docs.python.org/fr/3/library/stdtypes.html)
- [Visual Studio Code : utiliser Python](https://code.visualstudio.com/docs/python/python-tutorial)
- [Visual Studio Code : notebooks Jupyter](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- [Documentation de venv](https://docs.python.org/fr/3/library/venv.html)
