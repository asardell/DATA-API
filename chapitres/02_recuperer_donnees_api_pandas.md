# Chapitre 2 – Récupérer et exploiter des données d'une API avec Python et Pandas

## Objectifs

Voici les objectifs de ce chapitre :
- [ ] comprendre le fonctionnement d'une API REST : requête, paramètres, réponse, code de réponse
- [ ] lire la documentation d'une API pour identifier les endpoints et les paramètres
- [ ] interroger l'API ADEME avec `requests.get()` et des paramètres
- [ ] parcourir plusieurs pages de résultats dans une boucle
- [ ] lire une réponse JSON et la transformer en DataFrame Pandas
- [ ] sélectionner, filtrer, trier et agréger les données avec Pandas
- [ ] exploiter les codes de réponse HTTP et gérer les erreurs et les timeouts
- [ ] exporter les données en CSV et les relire
- [ ] exploiter les résultats dans un notebook Jupyter

## Sommaire

- [Chapitre 2 – Récupérer et exploiter des données d'une API avec Python et Pandas](#chapitre-2--récupérer-et-exploiter-des-données-dune-api-avec-python-et-pandas)
  - [Objectifs](#objectifs)
  - [Sommaire](#sommaire)
  - [Introduction : une API REST et les données DPE de l'ADEME](#introduction--une-api-rest-et-les-données-dpe-de-lademe)
  - [Préparation : installer requests et pandas](#préparation--installer-requests-et-pandas)
  - [Exercice 1 – Première requête GET](#exercice-1--première-requête-get)
    - [Mémo](#mémo)
    - [Exemple](#exemple)
    - [Exercices](#exercices)
  - [Exercice 2 – Lire la documentation et construire une requête](#exercice-2--lire-la-documentation-et-construire-une-requête)
    - [Mémo](#mémo-1)
    - [Exemple](#exemple-1)
    - [Exercices](#exercices-1)
  - [Exercice 3 – Parcourir plusieurs pages](#exercice-3--parcourir-plusieurs-pages)
    - [Mémo](#mémo-2)
    - [Exemple](#exemple-2)
    - [Exercices](#exercices-2)
  - [Exercice 4 – Transformer la réponse en DataFrame](#exercice-4--transformer-la-réponse-en-dataframe)
    - [Mémo](#mémo-3)
    - [Exemple](#exemple-3)
    - [Exercices](#exercices-3)
  - [Exercice 5 – Gérer les codes de réponse et les erreurs](#exercice-5--gérer-les-codes-de-réponse-et-les-erreurs)
    - [Mémo](#mémo-4)
    - [Exemple](#exemple-4)
    - [Exercices](#exercices-4)
  - [Exercice 6 – Sélectionner et filtrer](#exercice-6--sélectionner-et-filtrer)
    - [Mémo](#mémo-5)
    - [Exemple](#exemple-5)
    - [Exercices](#exercices-5)
  - [Exercice 7 – Trier et agréger](#exercice-7--trier-et-agréger)
    - [Mémo](#mémo-6)
    - [Exemple](#exemple-6)
    - [Exercices](#exercices-6)
  - [Exercice 8 – Exporter et relire un fichier CSV](#exercice-8--exporter-et-relire-un-fichier-csv)
    - [Mémo](#mémo-7)
    - [Exemple](#exemple-7)
    - [Exercices](#exercices-7)
  - [Exercice 9 – Mini-projet dans un notebook : passoires par année](#exercice-9--mini-projet-dans-un-notebook--passoires-par-année)
    - [Contexte](#contexte)
    - [Consignes](#consignes)
    - [Correction](#correction)
    - [Questions d'interprétation](#questions-dinterprétation)
  - [Exercice 10 (facultatif) – Parcourir toutes les pages avec le curseur `after`](#exercice-10-facultatif--parcourir-toutes-les-pages-avec-le-curseur-after)
    - [Mémo](#mémo-8)
    - [Exemple](#exemple-8)
    - [Exercice](#exercice)
  - [Liens utiles](#liens-utiles)

## Introduction : une API REST et les données DPE de l'ADEME

Une **API REST** est un service accessible par HTTP. Le client envoie une **requête** à une **URL** (la route), avec des **paramètres** ajoutés après le `?`. Le serveur renvoie une **réponse** : un **code de réponse** (`200` si tout va bien) et, le plus souvent, un corps au format **JSON**. Le JSON se lit en Python comme des listes et des dictionnaires, vus au chapitre 1.


![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTE_8o3DcCDUUWu2DnfjzBsT4lAvp3RCnvu7OmA0EsbOXRn6axpdPmSpBBR&s=10)

Dans ce chapitre, on n'utilise que la méthode **`GET`**, qui sert à lire des données. Les méthodes `POST`, `PUT` et `DELETE` sont abordées au chapitre 3.

Les données viennent de l'API ADEME, jeu **`dpe03existant`** : les diagnostics de performance énergétique (DPE) de logements existants. La documentation de l'API est disponible sur [data.ademe.fr](https://data.ademe.fr/datasets/dpe03existant/api-doc?operation=readLines). Cette API est publique : aucune clé n'est nécessaire pour les appels de ce chapitre.

Les paramètres utilisés dans ce chapitre :

| Paramètre | Rôle | Exemple |
|-----------|------|---------|
| `size` | nombre de lignes renvoyées par page | `size=100` |
| `page` | numéro de la page (à partir de 1) | `page=3` |
| `select` | liste des colonnes à renvoyer, séparées par des virgules | `select=numero_dpe,etiquette_dpe` |
| `qs` | filtre sur les valeurs d'une colonne | `qs=code_departement_ban:69` |
| `date_reception_dpe_gte` / `_lte` | bornes de date (supérieure ou égale, inférieure ou égale) | `date_reception_dpe_gte=2026-01-01` |

Les réponses contiennent trois champs : `total` (nombre de lignes correspondant au filtre), `results` (la liste des lignes de la page) et `next` (adresse de la page suivante, utilisée à l'exercice 10).

> **Note : des données qui évoluent**
> Les valeurs indiquées dans ce chapitre ont été constatées le 7 novembre 2026. Le nombre total de DPE augmente à mesure que l'ADEME publie de nouveaux diagnostics : vos résultats peuvent donc différer légèrement. Les étapes, elles, ne changent pas.

## Préparation : installer requests et pandas

Activer l'environnement créé au chapitre 1, puis installer les deux bibliothèques :

```powershell
# Activer l'environnement créé au chapitre 1 (chemin complet vers son dossier)
<chemin-vers-env-ademe>\Scripts\activate.bat
pip install requests pandas
pip list
```

`requests` envoie les requêtes HTTP. `pandas` organise les données dans un **DataFrame**, un tableau à lignes et colonnes.

Vérifier que les deux bibliothèques s'importent :

```python
import requests
import pandas as pd

print(requests.__version__)
print(pd.__version__)
```

> **Note : `requests` et `pd`**
> La convention `import pandas as pd` est universelle : on la retrouve dans toute la documentation Pandas. Les deux lignes d'import se mettent en début de script ou de notebook.

## Exercice 1 – Première requête GET

### Mémo

| Nom de la commande | Description | Argument pertinent | Exemple |
|--------------------|-------------|--------------------|---------|
| `requests.get()` | Envoie une requête `GET` et renvoie la réponse. | `params`, `timeout` | `requests.get(URL, params=params)` |
| `params=` | Ajoute un dictionnaire de paramètres à l'URL. | | `params={"size": 3}` |
| `timeout=` | Arrête l'appel si la réponse n'arrive pas dans le délai (en secondes). | | `timeout=10` |
| `response.status_code` | Code de réponse HTTP. | | `200` |
| `response.url` | URL complète envoyée, paramètres encodés. | | |
| `response.json()` | Convertit le corps JSON en dictionnaire ou liste Python. | | `data["total"]` |

### Exemple

```python
import requests

URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"

params = {
    "size": 3,
    "select": "numero_dpe,date_reception_dpe,code_postal_ban,etiquette_dpe,surface_habitable_logement",
    "qs": "code_departement_ban:69",
}

response = requests.get(URL, params=params, timeout=10)
print(response.status_code)   # 200
print(response.url)           # l'URL complète, avec les paramètres encodés

data = response.json()
print(data["total"])          # 517849
print(data["results"][0])
```

Le premier élément de `results` est un dictionnaire :

```text
{'numero_dpe': '2269E1179443X', 'date_reception_dpe': '2022-05-30', 'code_postal_ban': '69400', 'surface_habitable_logement': 75.8, 'etiquette_dpe': 'E', '_score': None}
```

### Exercices

1. Interroger l'API avec `size` égal à `3` et afficher le code de réponse.
<details>
<summary>Correction</summary>

```python
response = requests.get(URL, params={"size": 3}, timeout=10)
print(response.status_code)   # 200
```
</details>

2. Afficher les clés de la réponse JSON, puis le nombre total de DPE du département 69 (filtre `qs=code_departement_ban:69`).
<details>
<summary>Correction</summary>

```python
params = {"size": 3, "qs": "code_departement_ban:69"}
data = requests.get(URL, params=params, timeout=10).json()
print(list(data.keys()))   # ['total', 'next', 'results']
print(data["total"])       # 517849
```
Le champ `total` compte toutes les lignes qui correspondent au filtre, même si `size` n'en renvoie que 3.
</details>

3. Comparer la taille de l'objet renvoyé avec et sans `select`. Quelles colonnes contient un enregistrement sans `select` ?
<details>
<summary>Correction</summary>

```python
sans_select = requests.get(URL, params={"size": 1}, timeout=10).json()
print(len(sans_select["results"][0]))   # nombre de colonnes sans select
```
Sans `select`, l'API renvoie toutes les colonnes du jeu de données, ce qui alourdit la réponse. Le paramètre `select` permet de ne demander que les colonnes utiles. Le nombre de colonnes sans `select` dépend du jeu de données : le compter dans votre résultat plutôt que de le recopier.
</details>

> **Note : `timeout` dès la première requête**
> Sans `timeout`, `requests` peut attendre très longtemps une réponse. Prendre l'habitude de le préciser dès le début : le chapitre 3 explique comment gérer ce cas.

> **Note : la colonne `_score`**
> L'API ajoute une colonne `_score` à chaque ligne. Elle sert au classement d'une recherche textuelle et reste vide ici (`None`). Elle sera retirée à l'exercice 4.

## Exercice 2 – Lire la documentation et construire une requête

La documentation d'une API répond à trois questions : quel **endpoint** interroger, quels **paramètres** sont acceptés, quelle forme a la **réponse**. Pour `dpe03existant`, l'endpoint qui renvoie les lignes du jeu est `lines`, et la page de documentation liste les paramètres de filtre.

Le paramètre `qs` accepte la syntaxe `colonne:valeur`. Les bornes de date se passent avec `date_reception_dpe_gte` et `date_reception_dpe_lte`.

### Mémo

| Nom | Description | Exemple |
|-----|-------------|---------|
| `qs` | Filtre sur une colonne. | `qs=code_departement_ban:75` |
| `date_reception_dpe_gte` | Date minimale de réception, incluse. | `2026-01-01` |
| `date_reception_dpe_lte` | Date maximale de réception, incluse. | `2026-01-07` |
| Dictionnaire `params` | Permet de construire la requête par étapes. | `params["size"] = 10` |

### Exemple

```python
params = {
    "size": 1,
    "qs": "code_departement_ban:69",
    "date_reception_dpe_gte": "2026-01-01",
    "date_reception_dpe_lte": "2026-01-07",
}
data = requests.get(URL, params=params, timeout=10).json()
print(data["total"])   # 983
```

### Exercices

1. Afficher le nombre de DPE du département 75 (Paris).
<details>
<summary>Correction</summary>

```python
params = {"size": 1, "qs": "code_departement_ban:75"}
data = requests.get(URL, params=params, timeout=10).json()
print(data["total"])   # 862377
```
</details>

2. Afficher le nombre de DPE du département 69 reçus entre le 1er et le 7 janvier 2026.
<details>
<summary>Correction</summary>

```python
params = {
    "size": 1,
    "qs": "code_departement_ban:69",
    "date_reception_dpe_gte": "2026-01-01",
    "date_reception_dpe_lte": "2026-01-07",
}
data = requests.get(URL, params=params, timeout=10).json()
print(data["total"])   # 983
```
</details>

3. Construire un dictionnaire `params` pour le département 69, avec `size` à `5` et `select` contenant `numero_dpe` et `etiquette_dpe`. Vérifier avec `response.url` que les paramètres sont bien dans l'URL.
<details>
<summary>Correction</summary>

```python
params = {
    "size": 5,
    "select": "numero_dpe,etiquette_dpe",
    "qs": "code_departement_ban:69",
}
response = requests.get(URL, params=params, timeout=10)
print(response.url)
# ...?size=5&select=numero_dpe%2Cetiquette_dpe&qs=code_departement_ban%3A69
```
`requests` encode les caractères spéciaux (`,` devient `%2C`, `:` devient `%3A`). On n'écrit donc pas l'URL à la main : on passe un dictionnaire à `params`.
</details>

> **Note : filtrer par code postal**
> La documentation permet aussi de filtrer sur `code_postal_ban`. Dans l'environnement où ce chapitre a été vérifié, ce filtre renvoie une erreur `403 Forbidden`, alors que le filtre par département fonctionne. Le chapitre utilise donc le département. Si le filtre par code postal fonctionne sur votre poste, vous pouvez le remplacer : `qs=code_postal_ban:69100`.

## Exercice 3 – Parcourir plusieurs pages

Une seule requête renvoie au plus `size` lignes. Pour récupérer davantage de données, on demande les pages les unes après les autres avec `page`, dans une boucle.

Une limite à connaître : pour une requête paginée, `size` multiplié par le numéro de page ne peut pas dépasser 10 000. Une demande de `size=100` à la `page=101` renvoie l'erreur `400` : `"size + skip" cannot be more than 10000`. Le numéro de page reste donc limité à 100 pages de 100 lignes. Pour aller plus loin, il faut le curseur `after` (exercice 10).

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `range(a, b)` | Entiers de `a` à `b - 1`. Pour les pages 1 à 20 : `range(1, 21)`. | `for page in range(1, 21):` |
| `list.extend()` | Ajoute tous les éléments d'une liste à la fin d'une autre. | `lignes.extend(results)` |
| `break` | Arrête la boucle quand la page est vide. | |
| `data.get("results", [])` | Lit `results`, ou une liste vide si la clé manque. | |

### Exemple

```python
def extraire_pages(departement, nb_pages, taille_page):
    """Renvoie les lignes de plusieurs pages de DPE pour un département."""
    lignes = []
    for page in range(1, nb_pages + 1):
        params = {
            "page": page,
            "size": taille_page,
            "select": "numero_dpe,date_reception_dpe,code_postal_ban,etiquette_dpe,surface_habitable_logement",
            "qs": f"code_departement_ban:{departement}",
        }
        response = requests.get(URL, params=params, timeout=10)
        results = response.json().get("results", [])
        if not results:
            break   # plus de données : on sort de la boucle
        lignes.extend(results)
    return lignes

lignes = extraire_pages("69", nb_pages=2, taille_page=100)
print(len(lignes))   # 200
```

### Exercices

1. Récupérer 5 pages de 10 lignes pour le département 69 et afficher le nombre de lignes obtenues.
<details>
<summary>Correction</summary>

```python
lignes = extraire_pages("69", nb_pages=5, taille_page=10)
print(len(lignes))   # 50
```
</details>

2. Récupérer 20 pages de 100 lignes pour le département 69, puis afficher le nombre de lignes et le nombre de `numero_dpe` distincts. Que remarque-t-on ?
<details>
<summary>Correction</summary>

```python
lignes = extraire_pages("69", nb_pages=20, taille_page=100)
print(len(lignes))                                  # 2000
print(len({ligne["numero_dpe"] for ligne in lignes}))   # 2000
```
Chaque DPE n'apparaît qu'une fois : les pages ne se chevauchent pas. Il y a 2 000 lignes parce que la boucle s'arrête à 20 pages de 100 : le département en compte plus de 500 000, on n'a donc récupéré qu'un extrait. Ces 2 000 premières lignes ne forment pas un échantillon représentatif, car 1 738 d'entre elles ont été reçues en 2026. Garder cette limite en tête pour les analyses de l'exercice 9.
</details>

3. Vérifier que `size=100` avec `page=101` renvoie une erreur `400`, puis expliquer le message.
<details>
<summary>Correction</summary>

```python
response = requests.get(URL, params={"page": 101, "size": 100}, timeout=10)
print(response.status_code)   # 400
print(response.text)          # "size + skip" cannot be more than 10000
```
L'API limite le nombre de lignes atteignables avec `page` et `size` à 10 000 : `100 × 101 = 10 100`, au-dessus de la limite.
</details>

> **Note : pourquoi `range(1, nb_pages + 1)`**
> Les pages commencent à 1, alors que les positions dans une liste commencent à 0. Avec `range(1, nb_pages + 1)`, la boucle donne bien les pages de 1 à `nb_pages`.

## Exercice 4 – Transformer la réponse en DataFrame

Un **DataFrame** est un tableau à lignes et colonnes, qui se crée à partir d'une liste de dictionnaires. Chaque dictionnaire devient une ligne, chaque clé une colonne. Pandas gère les types de chaque colonne (texte, nombre, date) et les valeurs manquantes.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `pd.DataFrame()` | Crée un DataFrame à partir d'une liste de dictionnaires. | `pd.DataFrame(lignes)` |
| `df.shape` | Nombre de lignes et de colonnes. | `(2000, 6)` |
| `df.head(n)` | Affiche les `n` premières lignes (5 par défaut). | `df.head(3)` |
| `df.info()` | Résumé : colonnes, types et valeurs non nulles. | |
| `df.dtypes` | Type de chaque colonne. | |
| `df.isna().sum()` | Nombre de valeurs manquantes par colonne. | |
| `df.drop(columns=...)` | Supprime des colonnes. | `df.drop(columns=["_score"])` |
| `pd.json_normalize()` | Aplatit une réponse JSON contenant des objets imbriqués. Inutile ici, les données sont à plat. | |

### Exemple

```python
import pandas as pd

df = pd.DataFrame(lignes)
print(df.shape)               # (2000, 6)
df = df.drop(columns=["_score"])
print(df.shape)               # (2000, 5)
print(df.dtypes)
print(df.isna().sum())
print(df.head(3))
```

### Exercices

1. Créer le DataFrame `df` à partir de `lignes`, puis afficher ses dimensions.
<details>
<summary>Correction</summary>

```python
df = pd.DataFrame(lignes)
print(df.shape)   # (2000, 6)
```
La colonne `_score` compte parmi les six colonnes.
</details>

2. Supprimer la colonne `_score`, puis afficher le type de chaque colonne. Quel type a `surface_habitable_logement` ? Et `date_reception_dpe` ?
<details>
<summary>Correction</summary>

```python
df = df.drop(columns=["_score"])
print(df.dtypes)
```
- `surface_habitable_logement` est un `float64` : les nombres avec décimales sont lus comme des nombres.
- `date_reception_dpe` est un `object` : Pandas la lit comme du texte. Elle sera convertie en date à l'exercice 9.
</details>

3. Compter les valeurs manquantes par colonne. Combien de surfaces sont absentes ?
<details>
<summary>Correction</summary>

```python
print(df.isna().sum())
# surface_habitable_logement    54
```
Les 54 valeurs manquantes sont exclues par défaut des calculs de moyenne et de comptage.
</details>

4. Afficher les trois premières lignes avec `head(3)`, puis le résumé avec `info()`.
<details>
<summary>Correction</summary>

```python
print(df.head(3))
df.info()
```
`info()` indique le nombre de valeurs non nulles par colonne (2 000 sauf pour la surface, 1 946) et le type de chaque colonne.
</details>

> **Note : `object` ne veut pas dire « objet »**
> Dans Pandas, le type `object` désigne en général du texte (`str`). Une colonne de dates lue depuis un CSV apparaît en `object` tant qu'on ne la convertit pas.

## Exercice 5 – Gérer les codes de réponse et les erreurs

Une requête peut se passer de quatre façons : réussir (`200`), échouer côté client (`4xx` : requête mal formée, ressource absente, accès refusé), échouer côté serveur (`5xx`), ou ne donner aucune réponse dans le délai (timeout, ou serveur injoignable). Un code `200` ne garantit pas la présence de données : une recherche sans résultat renvoie aussi `200`, avec `total` à 0.

Le paramètre `timeout` indique à `requests` combien de secondes attendre la réponse. Sans lui, un appel peut bloquer le programme indéfiniment.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `response.status_code` | Code de réponse HTTP. | `404` |
| `response.ok` | `True` si le code est inférieur à 400. | `False` pour un `404` |
| `response.raise_for_status()` | Lève `HTTPError` si le code est `4xx` ou `5xx`. | |
| `timeout=2` | Abandonne si la réponse n'arrive pas dans le délai, en secondes. | `requests.get(URL, timeout=2)` |
| `requests.exceptions.HTTPError` | Erreur de code HTTP `4xx` ou `5xx`. | |
| `requests.exceptions.Timeout` | Délai dépassé (`ConnectTimeout` ou `ReadTimeout`). | |
| `requests.exceptions.ConnectionError` | Connexion impossible : serveur injoignable, nom de domaine inconnu. | |
| `requests.exceptions.RequestException` | Classe parente de toutes les erreurs de `requests`. | |

### Exemple

```python
import requests

URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"

def appeler_api(params):
    """Renvoie le JSON de l'API, ou None si la requête échoue."""
    try:
        response = requests.get(URL, params=params, timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Délai dépassé : pas de réponse en 2 secondes.")
    except requests.exceptions.HTTPError:
        print(f"Erreur HTTP {response.status_code} : {response.text[:80]}")
    except requests.exceptions.ConnectionError:
        print("Connexion impossible.")
    return None

appeler_api({"page": 101, "size": 100})
# Erreur HTTP 400 : "size + skip" cannot be more than 10000
```

Ordre des blocs `except` : `ConnectTimeout` hérite à la fois de `Timeout` et de `ConnectionError`. Le bloc `Timeout` doit donc venir **avant** le bloc `ConnectionError`, sinon un délai dépassé serait signalé comme une connexion impossible.

### Exercices

1. Interroger un dataset qui n'existe pas (`dpe_inexistant` à la place de `dpe03existant` dans l'URL). Afficher le code de réponse et le corps de la réponse.
<details>
<summary>Correction</summary>

```python
response = requests.get(
    "https://data.ademe.fr/data-fair/api/v1/datasets/dpe_inexistant/lines",
    timeout=2,
)
print(response.status_code)   # 404
print(response.text)          # Dataset not found
```
Le code `404` signifie que la ressource demandée n'existe pas. Ici, c'est l'URL qui est fausse : il faut la vérifier avant d'accuser le serveur.
</details>

2. Demander la `page` 101 avec `size` égal à 100. Utiliser `raise_for_status()` pour lever l'exception, puis afficher le message de l'exception.
<details>
<summary>Correction</summary>

```python
from requests.exceptions import HTTPError

response = requests.get(URL, params={"page": 101, "size": 100}, timeout=2)
try:
    response.raise_for_status()
except HTTPError as e:
    print(e)
```

Résultat :

```text
400 Client Error: Bad Request for url: https://data.ademe.fr/.../lines?page=101&size=100
```

Le serveur refuse une requête qu'il juge mal formée : `size` multiplié par `page` dépasse 10 000 (exercice 3).
</details>

3. Demander les DPE du code postal `69100` avec `qs=code_postal_ban:69100`. Quel code obtient-on dans l'environnement où ce chapitre a été vérifié ? Quelle exception `requests` lève-t-elle ?
<details>
<summary>Correction</summary>

```python
params = {"size": 1, "qs": "code_postal_ban:69100"}
print(appeler_api(params))
```

Dans l'environnement de vérification, la réponse est `403 Forbidden` (page HTML nginx), et `appeler_api()` affiche `Erreur HTTP 403 : <html>...`. La même demande par département fonctionne (exercice 2). Si votre poste obtient un `200`, cette question ne produit pas d'erreur : c'est une information utile, pas un échec de l'exercice.
</details>

4. Demander les DPE du département `99`, qui n'existe pas en France métropolitaine ni en outre-mer, avec `size` à 1. Le code obtenu est-il une erreur ? Comment le savoir dans le programme ?
<details>
<summary>Correction</summary>

```python
data = appeler_api({"size": 1, "qs": "code_departement_ban:99"})
print(data["total"])     # 0
print(data["results"])   # []
```

Le code est `200` : la requête est correcte, elle ne trouve simplement aucune ligne. Il ne faut donc pas traiter cette situation comme une erreur HTTP. Le test à faire dans le programme porte sur le contenu : `if data["total"] == 0:` ou `if not data["results"]:`.
</details>

5. Demander les 10 000 premières lignes du département 69, **sans** `select` (donc avec toutes les colonnes), avec `timeout=2`. Afficher un message si le délai est dépassé, avec la durée d'attente.
<details>
<summary>Correction</summary>

```python
import time

debut = time.perf_counter()
try:
    response = requests.get(
        URL,
        params={"size": 10000, "qs": "code_departement_ban:69"},
        timeout=2,
    )
    print(response.status_code, len(response.json()["results"]))
except requests.exceptions.Timeout:
    print(f"Pas de réponse en 2 secondes ({time.perf_counter() - debut:.1f} s)")
```

Résultat constaté : sur le département 13, la requête a dépassé les 2 secondes à chaque essai (`Pas de réponse en 2 secondes (2.1 s)`). Sur le département 69, elle a répondu en 2,6 s lors d'un essai, puis en moins de 2 secondes lors d'un autre. Les temps varient selon l'instant et l'état du serveur : si votre appel réussit, c'est un résultat normal, pas une erreur de votre code. Lors d'un premier essai, la même demande a pris près de 5 minutes (52 Mo de données). Pour vérifier la logique, on peut aussi demander 1 000 lignes : elles arrivent en moins d'une seconde (0,4 à 0,6 s).

Points à retenir :
- `timeout` ne limite pas la durée totale : il mesure l'attente de la réponse. Une réponse qui arrive lentement mais régulièrement peut ne pas déclencher le délai.
- Pour réduire le temps, on demande moins de lignes et moins de colonnes (`select`). Un `select` sur 10 000 lignes du département 13 dépasse aussi les 2 secondes lors de nos essais.
</details>

6. Interroger une adresse qui n'existe pas (`https://nexistepas.data-invalid.example/lines`) avec `appeler_api()`. Quelle exception est levée, et pourquoi ne peut-on pas la lire dans un code HTTP ?
<details>
<summary>Correction</summary>

```python
requests.get("https://nexistepas.data-invalid.example/lines", timeout=2)
# requests.exceptions.ConnectionError: ... Max retries exceeded ...
```

Aucune réponse HTTP n'est reçue : le nom de domaine n'est pas résolu, donc il n'y a pas de code de réponse à lire. C'est pour cela qu'il faut traiter `ConnectionError` séparément des erreurs `HTTPError`.
</details>

> **Note : ne pas afficher les erreurs sans les traiter**
> `print()` dans un bloc `except` suffit pour un script de test. Dans un vrai programme, une fonction doit soit renvoyer une valeur utilisable, soit relancer l'erreur, pour que l'appelant sache qu'il n'a pas de données. La fonction `appeler_api()` renvoie `None` dans ce cas : l'appelant doit vérifier ce `None` avant de l'utiliser.

## Exercice 6 – Sélectionner et filtrer

Pandas sélectionne des colonnes avec `df[...]`, des lignes et des colonnes avec `df.loc[lignes, colonnes]`, et filtre les lignes avec une condition booléenne. Comme au chapitre 1, `and`, `or` et `not` deviennent `&`, `|` et `~` avec Pandas, chaque condition étant mise entre parenthèses.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `df["colonne"]` | Sélectionne une colonne (une `Series`). | `df["etiquette_dpe"]` |
| `df[["a", "b"]]` | Sélectionne plusieurs colonnes (un DataFrame). | `df[["numero_dpe", "etiquette_dpe"]]` |
| `df.loc[condition, colonnes]` | Filtre des lignes et choisit des colonnes. | `df.loc[df["surface_habitable_logement"] > 100, ["numero_dpe"]]` |
| `isin()` | Teste si une valeur appartient à une liste. | `df["etiquette_dpe"].isin(["E", "F", "G"])` |
| `query()` | Filtre avec une expression en texte. | `df.query("etiquette_dpe in ['E', 'F', 'G']")` |

### Exemple

```python
# Colonnes choisies
print(df[["numero_dpe", "etiquette_dpe"]].head(3))

# Lignes filtrées : surface supérieure à 100 m²
grands = df.loc[df["surface_habitable_logement"] > 100, ["numero_dpe", "surface_habitable_logement"]]
print(len(grands))   # 275

# Passoires énergétiques : étiquettes E, F ou G
passoires = df[df["etiquette_dpe"].isin(["E", "F", "G"])]
print(len(passoires))   # 434
```

### Exercices

1. Afficher les colonnes `numero_dpe` et `date_reception_dpe` des cinq premières lignes.
<details>
<summary>Correction</summary>

```python
print(df[["numero_dpe", "date_reception_dpe"]].head())
```
</details>

2. Combien de logements ont une surface habitable supérieure à 100 m² ? Afficher la plus petite et la plus grande surface.
<details>
<summary>Correction</summary>

```python
print((df["surface_habitable_logement"] > 100).sum())   # 275
print(df["surface_habitable_logement"].min())            # 9.0
print(df["surface_habitable_logement"].max())            # 623.2
```
`min()` et `max()` ignorent les valeurs manquantes. Le fait que `sum()` sur une condition booléenne compte les lignes `True` est une astuce courante.
</details>

3. Obtenir les passoires énergétiques (étiquettes E, F ou G) avec `query()`, puis vérifier que le résultat est identique à celui obtenu avec `isin()`.
<details>
<summary>Correction</summary>

```python
par_query = df.query("etiquette_dpe in ['E', 'F', 'G']")
par_isin = df[df["etiquette_dpe"].isin(["E", "F", "G"])]
print(len(par_query), len(par_isin))   # 434 434
print(par_query.equals(par_isin))      # True
```
</details>

> **Note : les parenthèses dans les conditions Pandas**
> `df[(df["surface_habitable_logement"] > 100) & (df["etiquette_dpe"] == "G")]` fonctionne. Sans les parenthèses autour de chaque condition, Python évalue `&` avant `>` et l'erreur qui en résulte est difficile à lire. On écrit donc toujours les parenthèses.

## Exercice 7 – Trier et agréger

Trier avec `sort_values()`, compter les occurrences avec `value_counts()`, calculer des statistiques par groupe avec `groupby()`. Ces trois outils couvrent la plupart des analyses d'un jeu de données tabulaire.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `sort_values()` | Trie les lignes selon une colonne. `ascending=False` pour décroissant. | `df.sort_values("surface_habitable_logement", ascending=False)` |
| `value_counts()` | Compte les occurrences d'une colonne. `normalize=True` donne les proportions. | `df["etiquette_dpe"].value_counts()` |
| `groupby()` | Regroupe les lignes par valeur d'une colonne. | `df.groupby("etiquette_dpe")` |
| `mean()`, `median()`, `count()` | Statistiques appliquées à chaque groupe. | `.mean()` |
| `round(n)` | Arrondit à `n` décimales. | `.round(1)` |

### Exemple

```python
# Répartition des étiquettes
print(df["etiquette_dpe"].value_counts())

# Surface moyenne par étiquette
print(df.groupby("etiquette_dpe")["surface_habitable_logement"].mean().round(1))
```

### Exercices

1. Afficher la répartition des étiquettes DPE en proportions arrondies à 3 décimales.
<details>
<summary>Correction</summary>

```python
print(df["etiquette_dpe"].value_counts(normalize=True).round(3))
```
Résultat constaté : C 0,411 ; D 0,320 ; E 0,138 ; F 0,054 ; B 0,042 ; G 0,024 ; A 0,010.
</details>

2. Afficher les 3 logements de plus grande surface, avec les colonnes `numero_dpe`, `surface_habitable_logement` et `etiquette_dpe`.
<details>
<summary>Correction</summary>

```python
top3 = df.sort_values("surface_habitable_logement", ascending=False).head(3)
print(top3[["numero_dpe", "surface_habitable_logement", "etiquette_dpe"]])
```
La plus grande surface constatée est 623,2 m².
</details>

3. Calculer la surface moyenne par étiquette, arrondie à 1 décimale. Les étiquettes A et B ont-elles des surfaces plus grandes que les autres ?
<details>
<summary>Correction</summary>

```python
print(df.groupby("etiquette_dpe")["surface_habitable_logement"].mean().round(1))
```
Résultat constaté : A 148,5 ; B 94,4 ; C 64,2 ; D 63,1 ; E 65,5 ; F 63,0 ; G 62,5 (m²).

Les étiquettes A et B ont des surfaces plus grandes, mais l'étiquette A ne repose que sur 20 logements : la moyenne est sensible à quelques très grands logements. Les étiquettes C à G ont des surfaces proches : la surface n'explique pas à elle seule l'étiquette.
</details>

4. Compter les DPE par étiquette et par année de réception, sans encore convertir les dates. Expliquer pourquoi cette question n'est pas possible directement.
<details>
<summary>Correction</summary>

La question n'est pas possible directement tant que `date_reception_dpe` est du texte : il faut en extraire l'année, ce qui se fait à l'exercice 9 avec `pd.to_datetime()`. Les dates au format `AAAA-MM-JJ` se trient correctement même en texte, mais extraire l'année reste plus propre et plus sûr que de découper la chaîne à la main.
</details>

> **Note : `value_counts()` et `groupby()`**
> `value_counts()` répond à « combien de lignes par valeur ». `groupby()` répond à « quelle statistique par groupe ». Pour compter les lignes par groupe avec `groupby()`, on écrit `df.groupby("etiquette_dpe").size()`.

## Exercice 8 – Exporter et relire un fichier CSV

Pour garder une trace des données extraites, on les écrit dans un fichier CSV avec `to_csv()`. On le relit avec `read_csv()`. Il faut indiquer les types des colonnes qui doivent rester du texte, comme les codes postaux.

### Mémo

| Nom de la commande | Description | Argument pertinent | Exemple |
|--------------------|-------------|--------------------|---------|
| `df.to_csv()` | Écrit le DataFrame dans un fichier CSV. | `index=False`, `encoding` | `df.to_csv("dpe_69.csv", index=False, encoding="utf-8")` |
| `pd.read_csv()` | Lit un fichier CSV. | `dtype` | `pd.read_csv("dpe_69.csv", dtype={"code_postal_ban": str})` |

### Exemple

```python
df.to_csv("dpe_69_extrait.csv", index=False, encoding="utf-8")

relu = pd.read_csv("dpe_69_extrait.csv", dtype={"code_postal_ban": str})
print(relu.shape)   # (2000, 5)
```

### Exercices

1. Écrire `df` dans le fichier `dpe_69_extrait.csv` sans l'index, puis le relire dans une variable `relu`. Vérifier que les dimensions sont identiques.
<details>
<summary>Correction</summary>

```python
df.to_csv("dpe_69_extrait.csv", index=False, encoding="utf-8")
relu = pd.read_csv("dpe_69_extrait.csv", dtype={"code_postal_ban": str})
print(df.shape, relu.shape)   # (2000, 5) (2000, 5)
```
</details>

2. Expliquer ce que fait `index=False`, puis écrire la même opération sans cette option. Combien de colonnes supplémentaires apparaissent à la relecture ?
<details>
<summary>Correction</summary>

Sans `index=False`, Pandas écrit aussi l'index (0, 1, 2…) comme première colonne. À la relecture, cette colonne apparaît sans nom explicite (`Unnamed: 0`) et s'ajoute aux cinq colonnes : six colonnes au total.

Le réflexe à garder : écrire avec `index=False` sauf si l'index porte une information.
</details>

3. Sans l'option `dtype`, le code postal est relu comme un nombre ou un texte selon les cas. Relire le fichier avec `dtype={"code_postal_ban": str}`, puis vérifier le type de la colonne.
<details>
<summary>Correction</summary>

```python
relu = pd.read_csv("dpe_69_extrait.csv", dtype={"code_postal_ban": str})
print(relu["code_postal_ban"].dtype)   # object (texte)
print(relu["code_postal_ban"].head(3).tolist())   # ['69400', '69120', '69008']
```
Un code postal est un identifiant, pas une quantité : on le garde en texte pour ne pas perdre les zéros de tête (par exemple `01000` dans un autre département).
</details>

> **Note : `encoding="utf-8"`**
> Les noms de colonnes et les valeurs peuvent contenir des caractères accentués. Écrire et lire en UTF-8 évite les caractères mal affichés.

## Exercice 9 – Mini-projet dans un notebook : passoires par année

On reprend les données du chapitre pour répondre à une question : **quelle part des DPE sont des passoires énergétiques (étiquettes E, F ou G), année par année ?** Ce mini-projet réunit tout le chapitre : requête, boucle, DataFrame, filtre, agrégation, export.

### Contexte

Une passoire énergétique est un logement classé E, F ou G. La part de passoires est un indicateur suivi pour la rénovation énergétique. Ici, on la calcule sur l'extrait des 2 000 premiers DPE du département 69, qui ne représente pas l'ensemble des logements : la conclusion doit en tenir compte.

### Consignes

Dans un notebook Jupyter (voir chapitre 1, exercice 7), avec le kernel `env-ademe` :

1. Récupérer 20 pages de 100 DPE du département 69 avec `extraire_pages()`, puis créer le DataFrame.
2. Supprimer la colonne `_score`.
3. Convertir `date_reception_dpe` en date avec `pd.to_datetime()`, puis créer une colonne `annee` avec `.dt.year`.
4. Calculer, pour chaque année, le nombre de DPE et la part de passoires, arrondie à 3 décimales.
5. Exporter ce tableau par année dans `passoires_par_annee.csv`.

### Correction

```python
dates = pd.to_datetime(df["date_reception_dpe"])
df["annee"] = dates.dt.year

df["passoire"] = df["etiquette_dpe"].isin(["E", "F", "G"])
bilan = df.groupby("annee").agg(
    nb_dpe=("numero_dpe", "count"),
    part_passoires=("passoire", "mean"),
).round(3)

print(bilan)
bilan.to_csv("passoires_par_annee.csv", encoding="utf-8")
```

Résultat constaté (2 000 DPE) :

| Année | Nombre de DPE | Part de passoires |
|-------|---------------|-------------------|
| 2021 | 95 | 0,242 |
| 2022 | 17 | 0,353 |
| 2023 | 30 | 0,267 |
| 2024 | 44 | 0,136 |
| 2025 | 76 | 0,092 |
| 2026 | 1 738 | 0,221 |

Au total, 434 DPE sur 2 000 sont des passoires (21,7 %).

### Questions d'interprétation

1. Pourquoi la ligne 2022 ne compte-t-elle que 17 DPE alors que 2026 en compte 1 738 ?
<details>
<summary>Correction</summary>

Les 2 000 lignes ne sont pas un échantillon aléatoire : elles ne couvrent que quelques années, avec une forte concentration en 2026. Les années à petit effectif (2022 avec 17 DPE) donnent une part très instable : une ou deux lignes en plus changent fortement le pourcentage. Pour une conclusion sur l'évolution, il faudrait extraire davantage de données, en filtrant par date avec `date_reception_dpe_gte` et `date_reception_dpe_lte`.
</details>

2. La part de passoires est-elle la même pour toutes les années ? Peut-on conclure sur une tendance ?
<details>
<summary>Correction</summary>

Non : les parts vont de 9,2 % (2025) à 35,3 % (2022). Mais avec des effectifs de 17 à 95 pour les années autres que 2026, les écarts peuvent venir du hasard de l'extrait. Ce résultat décrit ces 2 000 lignes ; il ne prouve pas une tendance.
</details>

3. Ajouter une colonne `surface_m2_classe` qui vaut `"petit"` si la surface est inférieure à 50 m², `"moyen"` si elle est entre 50 et 100 m² incluse, et `"grand"` au-delà. Combien de lignes sont dans chaque classe ? Attention aux 54 surfaces manquantes.
<details>
<summary>Correction</summary>

```python
import numpy as np

df["surface_m2_classe"] = np.select(
    [df["surface_habitable_logement"] < 50,
     df["surface_habitable_logement"] <= 100,
     df["surface_habitable_logement"] > 100],
    ["petit", "moyen", "grand"],
    default="inconnu",
)
print(df["surface_m2_classe"].value_counts())
```

Résultat constaté : petit 793, moyen 878, grand 275, inconnu 54.

`np.select` vérifie les conditions dans l'ordre et met `"inconnu"` pour les valeurs manquantes, qui ne satisfont aucune condition.
</details>

> **Note : `groupby().agg()` avec des noms explicites**
> `agg(nb_dpe=("numero_dpe", "count"))` crée la colonne `nb_dpe` en une seule étape. Cette forme évite un renommage ultérieur de colonnes.

## Exercice 10 (facultatif) – Parcourir toutes les pages avec le curseur `after`

La limite de 10 000 lignes par pagination (exercice 3) empêche de parcourir un très grand volume avec `page`. L'API fournit un autre mécanisme : le champ `next` de la réponse contient l'URL de la page suivante, avec un curseur `after`. On suit simplement cette adresse jusqu'à ce qu'elle soit vide.

### Mémo

| Élément | Description |
|---------|-------------|
| `data.get("next")` | Adresse de la page suivante, ou `None` pour la dernière page. |
| `while url:` | Boucle tant qu'il reste une page. |
| `after=...` | Curseur interne ajouté par l'API ; on ne le construit pas soi-même. |

### Exemple

```python
url = requests.Request("GET", URL, params={
    "size": 1000,
    "qs": "code_departement_ban:69",
}).prepare().url

lignes = []
pages = 0
while url and pages < 3:
    data = requests.get(url, timeout=30).json()
    lignes.extend(data["results"])
    url = data.get("next")
    pages += 1

print(len(lignes))   # 3000
```

### Exercice

Modifier l'exemple pour suivre le curseur `next` pendant 10 pages de 1 000 lignes au maximum, puis afficher le nombre de `numero_dpe` distincts. Expliquer pourquoi on ne parcourt pas tout le jeu dans ce chapitre.

<details>
<summary>Correction</summary>

```python
url = requests.Request("GET", URL, params={
    "size": 1000,
    "qs": "code_departement_ban:69",
}).prepare().url

lignes = []
pages = 0
while url and pages < 10:
    data = requests.get(url, timeout=30).json()
    lignes.extend(data["results"])
    url = data.get("next")
    pages += 1

print(len(lignes))                                       # 10000
print(len({ligne["numero_dpe"] for ligne in lignes}))   # 10000
```

Le département 69 compte plus de 500 000 DPE : tout récupérer demanderait plus de 500 requêtes successives, ce qui n'est pas l'objet de ce chapitre. La boucle est donc bornée à 10 pages. Pour une extraction complète, il faudrait ajouter un `timeout` et une gestion des erreurs (exercice 5), et filtrer davantage (une période, une commune) pour ne télécharger que ce qui sert au besoin.
</details>

> **Note : limites d'usage de l'API**
> L'API ADEME limite le nombre et le coût des requêtes. Les limites suivantes s'appliquent par intervalle de 60 secondes :
>
> | Type d'utilisateur | Requêtes | Téléchargement (contenus statiques) | Téléchargement (autres appels) | Temps de traitement cumulé |
> |--------------------|----------|-------------------------------------|--------------------------------|----------------------------|
> | Anonyme | 600 | 8 MB/s | 500 kB/s | 20 s |
> | Authentifié (session ou clé d'API) | 1 200 | 16 MB/s | 1 MB/s | 60 s |
>
> Au-delà du temps de traitement cumulé, les requêtes sont rejetées avec le code **429** (`Too Many Requests`) jusqu'à ce que l'usage repasse sous la limite. Dans cet exercice, les 10 requêtes restent loin du seuil de 600 requêtes, mais une boucle qui enchaîne des pages lourdes peut atteindre la limite de temps de traitement. En cas de réponse 429, il faut attendre avant de réessayer, plutôt que de relancer la boucle immédiatement.

> **Note : ne pas construire le curseur à la main**
> La valeur `after` change à chaque page et dépend de l'ordre interne de l'API. On suit toujours l'URL donnée par `next`, sans la modifier.

## Liens utiles

- [Documentation de l'API ADEME (dataset dpe03existant)](https://data.ademe.fr/datasets/dpe03existant/api-doc?operation=readLines)
- [Données DPE de l'ADEME](https://data.ademe.fr/datasets/dpe03existant)
- [Documentation de requests](https://requests.readthedocs.io/)
- [Documentation de Pandas : DataFrame](https://pandas.pydata.org/docs/reference/frame.html)
- [Pandas : pour les utilisateurs de SQL, groupby et filtres](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html)
