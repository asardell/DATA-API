# Chapitre 3 – Consommer des API REST en profondeur

## Objectifs

Voici les objectifs de ce chapitre :
- [ ] utiliser les méthodes `POST`, `PUT` et `DELETE` avec `requests`
- [ ] envoyer un corps JSON et des en-têtes (headers)
- [ ] utiliser une API protégée par un Bearer Token ou une clé d'API
- [ ] interpréter les codes de réponse `2xx`, `4xx` et `5xx`
- [ ] gérer les erreurs HTTP, les erreurs de connexion et les timeouts
- [ ] sécuriser les appels avec un timeout et des réessais
- [ ] tester chaque requête dans Postman avant de l'écrire en Python

## Sommaire

- [Chapitre 3 – Consommer des API REST en profondeur](#chapitre-3--consommer-des-api-rest-en-profondeur)
  - [Objectifs](#objectifs)
  - [Sommaire](#sommaire)
  - [Introduction : quatre méthodes HTTP et une API de test](#introduction--quatre-méthodes-http-et-une-api-de-test)
  - [Préparation : lancer l'API de test et installer Postman](#préparation--lancer-lapi-de-test-et-installer-postman)
    - [Installer les dépendances de l'API](#installer-les-dépendances-de-lapi)
    - [Lancer l'API](#lancer-lapi)
    - [Installer Postman](#installer-postman)
  - [Exercice 1 – Lancer l'API et lire sa documentation](#exercice-1--lancer-lapi-et-lire-sa-documentation)
    - [Mémo](#mémo)
    - [Exemple](#exemple)
    - [Exercices](#exercices)
  - [Exercice 2 – GET : lire et paginer les DPE](#exercice-2--get--lire-et-paginer-les-dpe)
    - [Mémo](#mémo-1)
    - [Exemple](#exemple-1)
    - [Exercices](#exercices-1)
  - [Exercice 3 – POST : créer un DPE](#exercice-3--post--créer-un-dpe)
    - [Mémo](#mémo-2)
    - [Exemple](#exemple-2)
    - [Exercices](#exercices-2)
  - [Exercice 4 – PUT : remplacer un DPE](#exercice-4--put--remplacer-un-dpe)
    - [Mémo](#mémo-3)
    - [Exemple](#exemple-3)
    - [Exercices](#exercices-3)
  - [Exercice 5 – DELETE : supprimer un DPE](#exercice-5--delete--supprimer-un-dpe)
    - [Mémo](#mémo-4)
    - [Exemple](#exemple-4)
    - [Exercices](#exercices-4)
  - [Exercice 6 – Authentification : Bearer Token et clé d'API](#exercice-6--authentification--bearer-token-et-clé-dapi)
    - [Mémo](#mémo-5)
    - [Exemple](#exemple-5)
    - [Exercices](#exercices-5)
  - [Exercice 7 – Codes de réponse et exceptions](#exercice-7--codes-de-réponse-et-exceptions)
    - [Mémo](#mémo-6)
    - [Notions Python de ce chapitre](#notions-python-de-ce-chapitre)
    - [Exemple : une exception personnalisée](#exemple--une-exception-personnalisée)
    - [Exercices](#exercices-6)
  - [Exercice 8 – Timeouts et réessais](#exercice-8--timeouts-et-réessais)
    - [Mémo](#mémo-7)
    - [Exemple](#exemple-6)
    - [Exercices](#exercices-7)
  - [Liens utiles](#liens-utiles)

## Introduction : quatre méthodes HTTP et une API de test

Le chapitre 2 n'utilisait que `GET`, qui lit des données sans les modifier. Une API permet aussi de créer, remplacer et supprimer des ressources :

| Méthode | Rôle | Réussite habituelle | Si on la répète à l'identique |
|---------|------|---------------------|-------------------------------|
| `GET` | lire une ressource | `200` | même résultat |
| `POST` | créer une ressource | `201` | crée un doublon, ou renvoie `409` |
| `PUT` | remplacer une ressource entière | `200` | même résultat |
| `DELETE` | supprimer une ressource | `204` | la ressource est déjà absente : `404` |

Les appels de ce chapitre visent une **API de test** écrite avec **FastAPI**, qui tourne sur votre poste. Elle reprend les mêmes mécanismes qu'une API réelle, sans dépendre d'un service distant : on peut donc créer, modifier et supprimer des DPE sans risque.

Les routes disponibles :

| Méthode | Route | Protection | Ce qu'elle fait |
|---------|-------|------------|-----------------|
| `GET` | `/health` | aucune | vérifie que l'API répond |
| `GET` | `/dpe?etiquette=&limit=&offset=` | aucune | liste les DPE, avec filtre et pagination |
| `GET` | `/dpe/{numero_dpe}` | aucune | lit un DPE (`404` s'il n'existe pas) |
| `POST` | `/dpe` | Bearer Token | crée un DPE (`201`, `409` si déjà présent) |
| `PUT` | `/dpe/{numero_dpe}` | Bearer Token | remplace un DPE (`200`, `404` si absent) |
| `DELETE` | `/dpe/{numero_dpe}` | Bearer Token | supprime un DPE (`204`, `404` si absent) |
| `GET` | `/cle-api/passoires` | clé d'API | compte les passoires énergétiques |
| `GET` | `/lent?secondes=` | aucune | répond après le délai demandé, pour tester les timeouts |

Les données sont 200 DPE de la formation, copiés dans la base SQLite au démarrage. La base est recréée à chaque lancement : chaque séance repart du même état.

Les valeurs d'authentification ci-dessous sont **des valeurs de formation**, à ne jamais réutiliser pour un vrai service :
- token Bearer : `token-formation-2026`
- clé d'API : `cle-formation-2026`

## Préparation : lancer l'API de test et installer Postman

### Installer les dépendances de l'API

Activer l'environnement du chapitre 1, puis installer les dépendances du dossier `api_test` :

```powershell
# Activer l'environnement créé au chapitre 1 (chemin complet vers son dossier)
<chemin-vers-env-ademe>\Scripts\activate.bat
pip install -r C:\Users\<votre-nom>\Documents\GitHub\DATA-API\requirements.txt
```

### Lancer l'API

Depuis le dossier `api_test` :

```powershell
cd C:\Users\<votre-nom>\Documents\GitHub\DATA-API\api_test
uvicorn main:app --reload
```

Ouvrir ensuite `http://127.0.0.1:8000/docs` dans le navigateur. Laisser le terminal ouvert pendant tout le chapitre : arrêter le serveur avec `Ctrl + C`.

> **Note : utiliser `127.0.0.1` plutôt que `localhost`**
> Sur ce poste Windows, chaque appel à `http://localhost:8000` prend environ 2 secondes de plus : le système essaie d'abord l'adresse IPv6, puis revient à IPv4. Ce délai fausse les mesures de timeout de l'exercice 8. Le chapitre utilise donc `127.0.0.1`, qui répond immédiatement. Si votre poste ne présente pas ce délai, `localhost` fonctionne aussi.

### Installer Postman

Installer [Postman](https://www.postman.com/downloads/) (version gratuite suffisante). Pour chaque exercice, la section **Dans Postman** indique la requête à construire. Dans Postman :
- la méthode se choisit dans la liste à gauche de l'URL ;
- les paramètres se saisissent dans l'onglet **Params** ;
- l'en-tête `Authorization` se configure dans l'onglet **Auth**, type **Bearer Token** ;
- le corps JSON se saisit dans l'onglet **Body**, option **raw**, format **JSON**.

> **Note : menus de Postman**
> Les noms des onglets peuvent varier légèrement selon la version de Postman. Dans ce cas, chercher l'onglet qui correspond à la fonction décrite.

## Exercice 1 – Lancer l'API et lire sa documentation

L'API génère sa documentation à partir du code. Trois adresses sont disponibles pendant que l'API tourne :
- `http://127.0.0.1:8000/docs` : interface Swagger, pour lire et tester les routes ;
- `http://127.0.0.1:8000/redoc` : documentation lisible ;
- `http://127.0.0.1:8000/openapi.json` : le schéma de l'API, importable dans Postman.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `requests.get()` | Envoie une requête `GET`. | `requests.get(url, timeout=2)` |
| `response.json()` | Lit le corps JSON. | `response.json()["status"]` |
| `timeout=` | Délai maximal d'attente, en secondes. | `timeout=2` |

### Exemple

```python
import requests

BASE = "http://127.0.0.1:8000"

reponse = requests.get(f"{BASE}/health", timeout=2)
print(reponse.status_code)   # 200
print(reponse.json())        # {'status': 'ok'}
```

### Exercices

1. Dans Postman, créer une requête `GET` sur `http://127.0.0.1:8000/health` et l'envoyer. Reproduire le même appel en Python et afficher le code de réponse.
<details>
<summary>Correction</summary>

Dans Postman : méthode `GET`, URL `http://127.0.0.1:8000/health`, bouton **Send** : le code `200` et le corps `{"status": "ok"}` s'affichent.

En Python : l'exemple ci-dessus donne `200` et `{'status': 'ok'}`.
</details>

2. Ouvrir `http://127.0.0.1:8000/openapi.json` dans le navigateur. Combien de routes sont décrites ? Lister celles qui ont la méthode `POST`, `PUT` ou `DELETE`.
<details>
<summary>Correction</summary>

Il y a 8 routes décrites, dont 3 avec `POST`, `PUT` ou `DELETE` :
- `POST /dpe`
- `PUT /dpe/{numero_dpe}`
- `DELETE /dpe/{numero_dpe}`

Le schéma JSON est utile pour importer l'API dans un autre outil, comme Postman (menu d'importation, à partir d'une URL).
</details>

## Exercice 2 – GET : lire et paginer les DPE

Le chapitre 2 a montré `GET` sur une API externe. Ici, la route `/dpe` accepte deux paramètres de pagination : `limit` (nombre de lignes, entre 1 et 100) et `offset` (nombre de lignes à sauter). Une valeur hors de ces bornes renvoie une erreur `422`.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `params=` | Ajoute les paramètres à l'URL. | `params={"limit": 5}` |
| `offset` | Nombre de lignes à sauter, pour passer à la page suivante. | `offset=5` |
| `response.json()["total"]` | Nombre total de DPE correspondant au filtre. | `200` |

### Exemple

```python
import requests

BASE = "http://127.0.0.1:8000"
reponse = requests.get(f"{BASE}/dpe", params={"limit": 2, "offset": 0}, timeout=2)
donnees = reponse.json()
print(donnees["total"])                       # 200
print(donnees["results"][0]["numero_dpe"])    # 2169E0410532J
```

### Exercices

1. Récupérer le DPE `2169E0410532J` avec la route `/dpe/{numero_dpe}`. Afficher son étiquette.
<details>
<summary>Correction</summary>

```python
reponse = requests.get(f"{BASE}/dpe/2169E0410532J", timeout=2)
print(reponse.json()["etiquette_dpe"])   # D
```
</details>

2. Demander un DPE qui n'existe pas (`ZZZZ00000`). Afficher le code et le message d'erreur.
<details>
<summary>Correction</summary>

```python
reponse = requests.get(f"{BASE}/dpe/ZZZZ00000", timeout=2)
print(reponse.status_code)   # 404
print(reponse.json())        # {'detail': 'DPE ZZZZ00000 introuvable'}
```
Le corps de l'erreur est un JSON avec la clé `detail`. C'est la forme utilisée par FastAPI pour toutes ses erreurs.
</details>

3. Afficher la deuxième page de 5 DPE : les lignes 6 à 10 de la liste triée par `numero_dpe`. Quels sont leurs numéros ?
<details>
<summary>Correction</summary>

```python
reponse = requests.get(f"{BASE}/dpe", params={"limit": 5, "offset": 5}, timeout=2)
for dpe in reponse.json()["results"]:
    print(dpe["numero_dpe"])
```
Le résultat dépend du tri des numéros, qui est donné par l'API ; il ne faut pas le recopier en dur, car il change si la base est modifiée (exercices 3 à 5).
</details>

4. Demander `limit=0`, puis `etiquette=Z`. Lire le code de réponse et la liste des erreurs.
<details>
<summary>Correction</summary>

```python
print(requests.get(f"{BASE}/dpe", params={"limit": 0}, timeout=2).status_code)     # 422
print(requests.get(f"{BASE}/dpe", params={"etiquette": "Z"}, timeout=2).status_code)  # 422
erreur = requests.get(f"{BASE}/dpe", params={"etiquette": "Z"}, timeout=2).json()
print(erreur["detail"][0]["loc"], erreur["detail"][0]["msg"])
# ['query', 'etiquette'] String should match pattern '^[A-G]$'
```
Le code `422` signifie que la requête est bien formée mais que ses données ne respectent pas les règles de l'API. Le champ `loc` indique où se situe l'erreur.
</details>

> **Note : `422` et `400`**
> Le `400` signale une requête invalide au sens général. FastAPI utilise `422` pour les données qui ne respectent pas le schéma (type, format, bornes). Les deux codes sont des erreurs client : le programme doit corriger la requête avant de la renvoyer.

## Exercice 3 – POST : créer un DPE

`POST` envoie des données dans le corps de la requête pour créer une ressource. Avec `requests`, le paramètre `json=` transforme un dictionnaire Python en JSON et ajoute automatiquement l'en-tête `Content-Type: application/json`.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `requests.post()` | Envoie une requête `POST`. | `requests.post(url, json=dpe)` |
| `json=` | Corps de la requête, converti en JSON. | `json={"numero_dpe": "..."}` |
| `headers=` | En-têtes HTTP supplémentaires. | `headers={"Authorization": "Bearer ..."}` |
| `status_code` `201` | La ressource a été créée. | |

### Exemple

```python
NOUVEAU_DPE = {
    "numero_dpe": "2569E0000001A",
    "date_reception_dpe": "2026-03-01",
    "code_postal_ban": "69100",
    "etiquette_dpe": "E",
    "surface_habitable_logement": 55.5,
}
ENTETE_AUTH = {"Authorization": "Bearer token-formation-2026"}

reponse = requests.post(f"{BASE}/dpe", json=NOUVEAU_DPE, headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 201
print(reponse.json())        # le DPE créé, tel que l'API l'a enregistré
```

**Dans Postman** : méthode `POST`, URL `http://127.0.0.1:8000/dpe`, onglet **Body** → **raw** → **JSON** avec le contenu ci-dessus, onglet **Auth** → **Bearer Token** avec `token-formation-2026`.

### Exercices

1. Envoyer le même `POST` **sans** l'en-tête `Authorization`. Quel code et quel message obtient-on ?
<details>
<summary>Correction</summary>

```python
reponse = requests.post(f"{BASE}/dpe", json=NOUVEAU_DPE, timeout=2)
print(reponse.status_code)   # 401
print(reponse.json())        # {'detail': 'Authentification requise'}
print(reponse.headers["WWW-Authenticate"])   # Bearer
```
`401` signifie : aucune identité fournie. L'en-tête `WWW-Authenticate` indique au client quel mécanisme utiliser.
</details>

2. Envoyer le `POST` avec l'en-tête `Authorization` correct. Vérifier que le DPE créé est bien lisible avec un `GET`.
<details>
<summary>Correction</summary>

```python
reponse = requests.post(f"{BASE}/dpe", json=NOUVEAU_DPE, headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 201
relecture = requests.get(f"{BASE}/dpe/{NOUVEAU_DPE['numero_dpe']}", timeout=2)
print(relecture.status_code, relecture.json()["etiquette_dpe"])   # 200 E
```
</details>

3. Renvoyer exactement le même `POST` une seconde fois. Quel code obtient-on ? Pourquoi ?
<details>
<summary>Correction</summary>

```python
reponse = requests.post(f"{BASE}/dpe", json=NOUVEAU_DPE, headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 409
print(reponse.json())        # {'detail': 'DPE 2569E0000001A existe déjà'}
```
Le `409` (conflit) signale que la ressource existe déjà. Contrairement à `PUT`, répéter un `POST` ne produit pas le même résultat : c'est pour cela qu'on ne le relance jamais automatiquement (exercice 8).
</details>

4. Envoyer un `POST` avec un code postal de quatre chiffres (`"6910"`). Lire la liste des erreurs renvoyée par l'API.
<details>
<summary>Correction</summary>

```python
dpe_invalide = dict(NOUVEAU_DPE, numero_dpe="2569E0000002B", code_postal_ban="6910")
reponse = requests.post(f"{BASE}/dpe", json=dpe_invalide, headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 422
for erreur in reponse.json()["detail"]:
    print(erreur["loc"], erreur["msg"])
# ['body', 'code_postal_ban'] String should match pattern '^\d{5}$'
```
Le champ `loc` indique le chemin de l'erreur : `body` pour le corps de la requête, puis le nom du champ.
</details>

> **Note : `json=` plutôt que `data=`**
> `data=` envoie les données sous forme de formulaire, ce que l'API ne lit pas. Avec `json=`, `requests` envoie du JSON et règle l'en-tête `Content-Type` tout seul. Avec `data=`, il faudrait écrire `json.dumps()` et l'en-tête à la main.

## Exercice 4 – PUT : remplacer un DPE

`PUT` remplace la ressource **entière** : le corps doit contenir tous les champs, même ceux qui ne changent pas. Répéter le même `PUT` donne toujours le même résultat, ce qui est le sens de la méthode.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `requests.put()` | Envoie une requête `PUT`. | `requests.put(url, json=dpe, headers=...)` |
| `dict(a, champ=valeur)` | Crée une copie d'un dictionnaire en modifiant un champ. | `dict(NOUVEAU_DPE, etiquette_dpe="B")` |

### Exemple

```python
url = f"{BASE}/dpe/{NOUVEAU_DPE['numero_dpe']}"
reponse = requests.put(url, json=dict(NOUVEAU_DPE, etiquette_dpe="B"), headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)           # 200
print(reponse.json()["etiquette_dpe"])   # B
```

**Dans Postman** : méthode `PUT`, URL `http://127.0.0.1:8000/dpe/2569E0000001A`, corps JSON complet, onglet **Auth** avec le Bearer Token.

Ces exercices utilisent le DPE `2569E0000001A` créé à l'exercice 3.

### Exercices

1. Passer l'étiquette du DPE `2569E0000001A` de `E` à `B`, avec un `PUT` complet. Vérifier avec un `GET`.
<details>
<summary>Correction</summary>

```python
url = f"{BASE}/dpe/2569E0000001A"
reponse = requests.put(url, json=dict(NOUVEAU_DPE, etiquette_dpe="B"), headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 200
print(requests.get(url, timeout=2).json()["etiquette_dpe"])   # B
```
</details>

2. Envoyer deux fois de suite le même `PUT`. Les deux réponses sont-elles identiques ?
<details>
<summary>Correction</summary>

```python
corps = dict(NOUVEAU_DPE, etiquette_dpe="B")
r1 = requests.put(url, json=corps, headers=ENTETE_AUTH, timeout=2)
r2 = requests.put(url, json=corps, headers=ENTETE_AUTH, timeout=2)
print(r1.status_code, r2.status_code)   # 200 200
print(r1.json() == r2.json())            # True
```
Les deux réponses sont identiques : c'est ce qu'on appelle l'idempotence. Elle permet de relancer un `PUT` après une erreur réseau sans risque.
</details>

3. Envoyer un `PUT` dont le `numero_dpe` du corps ne correspond pas à celui de l'URL. Quel code obtient-on ?
<details>
<summary>Correction</summary>

```python
reponse = requests.put(url, json=dict(NOUVEAU_DPE, numero_dpe="2569E0000009Z"), headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 400
print(reponse.json()["detail"])   # numero_dpe du corps différent de celui de l'URL
```
</details>

4. Envoyer un `PUT` sur un DPE inexistant (`ZZZZ00000`). Quel code obtient-on ?
<details>
<summary>Correction</summary>

```python
corps = dict(NOUVEAU_DPE, numero_dpe="ZZZZ00000")
reponse = requests.put(f"{BASE}/dpe/ZZZZ00000", json=corps, headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 404
```
Contrairement à `POST`, `PUT` ne crée pas la ressource si elle est absente. C'est une règle de cette API, à vérifier dans sa documentation : certaines API font l'inverse.
</details>

> **Note : `PUT` et `PATCH`**
> `PATCH` modifie seulement certains champs. Cette API ne propose que `PUT`. Pour modifier une seule valeur avec `PUT`, il faut renvoyer tous les champs : c'est pour cela que le corps de l'exemple est une copie complète.

## Exercice 5 – DELETE : supprimer un DPE

`DELETE` supprime la ressource désignée par l'URL. Une suppression réussie renvoie `204 No Content` : le corps de la réponse est vide.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `requests.delete()` | Envoie une requête `DELETE`. | `requests.delete(url, headers=...)` |
| `response.content` | Corps brut de la réponse, en octets. | `b""` pour un `204` |

### Exemple

```python
url = f"{BASE}/dpe/2569E0000001A"
reponse = requests.delete(url, headers=ENTETE_AUTH, timeout=2)
print(reponse.status_code)   # 204
print(reponse.content)       # b''
```

**Dans Postman** : méthode `DELETE`, URL `http://127.0.0.1:8000/dpe/2569E0000001A`, onglet **Auth** avec le Bearer Token.

### Exercices

1. Supprimer le DPE `2569E0000001A`. Vérifier avec un `GET` qu'il n'existe plus.
<details>
<summary>Correction</summary>

```python
print(requests.delete(url, headers=ENTETE_AUTH, timeout=2).status_code)   # 204
print(requests.get(url, timeout=2).status_code)                           # 404
```
</details>

2. Supprimer une seconde fois le même DPE. Quel code obtient-on ?
<details>
<summary>Correction</summary>

```python
print(requests.delete(url, headers=ENTETE_AUTH, timeout=2).status_code)   # 404
```
Le DPE est déjà absent : l'API répond `404`. Dans un programme, ce cas peut être traité comme un succès si le but est « le DPE n'existe plus ».
</details>

3. Tenter une suppression **sans** Bearer Token, sur un DPE existant (`2169E0410532J`). Quel code obtient-on ? Le DPE est-il supprimé ?
<details>
<summary>Correction</summary>

```python
reponse = requests.delete(f"{BASE}/dpe/2169E0410532J", timeout=2)
print(reponse.status_code)   # 401
print(requests.get(f"{BASE}/dpe/2169E0410532J", timeout=2).status_code)   # 200
```
Le DPE reste en place : la vérification d'identité a lieu avant la suppression.
</details>

> **Note : supprimer une ressource doit être une action volontaire**
> Un `DELETE` ne se relance jamais « au cas où » dans un programme, car il ne se défait pas. Dans le chapitre suivant, on verra comment vérifier le résultat avant toute suppression.

## Exercice 6 – Authentification : Bearer Token et clé d'API

Une API protège certaines routes en demandant une identité. Deux mécanismes sont fréquents, et ce chapitre en utilise les deux :
- **Bearer Token** : le client envoie l'en-tête `Authorization: Bearer <token>`. Le token est obtenu auprès du fournisseur de l'API (ici, la valeur fixée dans la formation).
- **Clé d'API** : le client envoie une clé dans un en-tête dédié, ici `X-API-Key: <clé>`.

Les codes de réponse distinguent deux situations :
- `401 Unauthorized` : aucune identité n'a été fournie ;
- `403 Forbidden` : une identité a été fournie, mais elle est refusée.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `headers=` | En-têtes d'une requête seule. | `headers={"X-API-Key": "..."}` |
| `requests.Session()` | Session qui garde des en-têtes communs à toutes les requêtes. | `session = requests.Session()` |
| `session.headers.update()` | Ajoute des en-têtes à la session. | `session.headers.update(ENTETE_AUTH)` |

### Exemple

```python
ENTETE_CLE = {"X-API-Key": "cle-formation-2026"}
reponse = requests.get(f"{BASE}/cle-api/passoires", headers=ENTETE_CLE, timeout=2)
print(reponse.status_code, reponse.json())   # 200 {'nb_passoires': 46}
```

**Dans Postman** : méthode `GET`, URL `http://127.0.0.1:8000/cle-api/passoires`, onglet **Headers**, nom `X-API-Key`, valeur `cle-formation-2026`.

### Exercices

1. Appeler `/cle-api/passoires` sans en-tête, puis avec la clé `faux`. Lire les deux codes.
<details>
<summary>Correction</summary>

```python
print(requests.get(f"{BASE}/cle-api/passoires", timeout=2).status_code)   # 401
print(requests.get(f"{BASE}/cle-api/passoires", headers={"X-API-Key": "faux"}, timeout=2).status_code)   # 403
```
Sans clé, `401` ; avec une mauvaise clé, `403`.
</details>

2. Appeler la même route avec la bonne clé. Quel est le nombre de passoires énergétiques dans la base au démarrage ?
<details>
<summary>Correction</summary>

```python
reponse = requests.get(f"{BASE}/cle-api/passoires", headers=ENTETE_CLE, timeout=2)
print(reponse.json())   # {'nb_passoires': 46}
```
Les 46 passoires sont les DPE étiquetés E, F ou G parmi les 200 de la base de départ (33 + 10 + 3). Le compte change si vous avez gardé le DPE de l'exercice 3 : il faut alors compter 47.
</details>

3. Créer une `Session` avec le Bearer Token dans ses en-têtes, puis créer un DPE sans répéter l'en-tête. Supprimer ensuite ce DPE avec la même session.
<details>
<summary>Correction</summary>

```python
session = requests.Session()
session.headers.update(ENTETE_AUTH)

nouveau = dict(NOUVEAU_DPE, numero_dpe="2569E0000003C")
print(session.post(f"{BASE}/dpe", json=nouveau, timeout=2).status_code)                     # 201
print(session.delete(f"{BASE}/dpe/2569E0000003C", timeout=2).status_code)                    # 204
```
La session évite de répéter les en-têtes. Elle garde aussi la connexion ouverte entre les appels, ce qui accélère les séries de requêtes. Les en-têtes de la session sont envoyés à **toutes** les requêtes de la session : ne pas y mettre un token réservé à une seule route.
</details>

> **Note : ne pas mettre la clé dans l'URL**
> Une clé passée en paramètre (`?api_key=...`) apparaît dans l'historique du navigateur, dans les journaux du serveur et dans les copies d'URL. L'en-tête reste plus sûr. Ne jamais écrire un token ou une clé réelle dans un script versionné : les lire depuis une variable d'environnement ou un fichier `.env` ignoré par Git.

## Exercice 7 – Codes de réponse et exceptions

Chaque réponse porte un code à trois chiffres. Son premier chiffre donne la famille :

| Famille | Sens | Codes vus dans ce chapitre |
|---------|------|----------------------------|
| `2xx` | succès | `200` lecture ou modification, `201` création, `204` suppression sans contenu |
| `4xx` | erreur côté client : la requête doit être corrigée | `400`, `401`, `403`, `404`, `409`, `422` |
| `5xx` | erreur côté serveur : la requête n'est peut-être pas en cause | `500`, `503` (non produits par cette API) |

`requests` ne lève pas d'exception pour un `4xx` ou un `5xx` par défaut : il faut les tester soi-même, avec `response.ok` ou `response.raise_for_status()`. Les erreurs de transport (délai dépassé, connexion impossible) lèvent en revanche des exceptions.

### Mémo

| Nom de la commande | Description |
|--------------------|-------------|
| `response.ok` | `True` pour les codes inférieurs à 400. |
| `response.raise_for_status()` | Lève `HTTPError` pour les codes `4xx` et `5xx`. |
| `requests.exceptions.HTTPError` | Erreur de code HTTP. |
| `requests.exceptions.Timeout` | Délai dépassé. |
| `requests.exceptions.ConnectionError` | Connexion impossible. |
| `requests.exceptions.RequestException` | Classe parente de toutes les erreurs de `requests`. |

### Notions Python de ce chapitre

Les exemples suivants utilisent quelques mots-clés nouveaux, à connaître avant de lire le code :

| Élément | Description | Exemple |
|---------|-------------|---------|
| `raise` | Lève une exception, c'est-à-dire interrompt le code en cours et signale une erreur. Seul, dans un `except`, `raise` relance l'exception d'origine. | `raise ValueError("code invalide")` |
| `class` | Définit une classe, un modèle qui regroupe des données et des fonctions. Ici, `ApiErreur(Exception)` hérite d'`Exception` : c'est une exception que l'on peut lever et intercepter comme les autres. | `class ApiErreur(Exception):` |
| `__init__` | Méthode appelée à la création d'un objet. Elle reçoit les valeurs passées entre parenthèses. | `def __init__(self, code, message):` |
| `self` | Premier paramètre des méthodes : désigne l'objet en cours. | `self.code = code` |
| `super()` | Appelle la méthode de la classe parente, ici le constructeur d'`Exception`. | `super().__init__("texte")` |
| `**kwargs` | Dans une définition, regroupe les arguments nommés en un dictionnaire. Dans un appel, `**dico` fait l'inverse : il transforme un dictionnaire en arguments nommés. | `def f(**kwargs):` puis `f(timeout=2)` |
| `dict()` | Crée un dictionnaire. Les arguments nommés deviennent les clés. | `dict(a=1, b=2)` donne `{'a': 1, 'b': 2}` |

> **Note : `**kwargs` ne sert qu'à transmettre des options**
> `appeler()` transmet ses arguments nommés (`json=`, `headers=`, `params=`) à `requests.request()` sans les lister un par un. Le `kwargs.setdefault("timeout", 2)` ajoute un délai par défaut, sauf si l'appelant en fournit un.

### Exemple : une exception personnalisée

Pour que le reste du programme n'ait pas à connaître les détails de `requests`, on regroupe les erreurs dans une seule exception :

```python
import requests

BASE = "http://127.0.0.1:8000"

class ApiErreur(Exception):
    """Erreur renvoyée par l'API ou par le réseau, avec son code."""

    def __init__(self, code, message):
        super().__init__(f"{code} : {message}")
        self.code = code
        self.message = message

MESSAGES = {
    401: "authentification requise",
    403: "accès refusé",
    404: "ressource introuvable",
    409: "la ressource existe déjà",
    422: "données invalides",
}

def appeler(methode, chemin, **kwargs):
    """Envoie une requête et renvoie le JSON, ou lève ApiErreur."""
    kwargs.setdefault("timeout", 2)
    try:
        reponse = requests.request(methode, f"{BASE}{chemin}", **kwargs)
    except requests.exceptions.Timeout:
        raise ApiErreur("timeout", "pas de réponse dans le délai")
    except requests.exceptions.ConnectionError:
        raise ApiErreur("connexion", "API injoignable")

    if reponse.ok:
        return None if reponse.status_code == 204 else reponse.json()

    if reponse.status_code >= 500:
        message = "erreur interne du serveur"
    else:
        message = MESSAGES.get(reponse.status_code, reponse.text[:80])
    raise ApiErreur(reponse.status_code, message)
```

### Exercices

1. Appeler `appeler("GET", "/dpe/ZZZZ00000")` et intercepter `ApiErreur`. Afficher le code et le message.
<details>
<summary>Correction</summary>

```python
try:
    appeler("GET", "/dpe/ZZZZ00000")
except ApiErreur as e:
    print(e.code, e.message)   # 404 ressource introuvable
```
</details>

2. Appeler `appeler("POST", "/dpe", json=NOUVEAU_DPE)` **sans** authentification, puis avec. Vérifier les deux comportements.
<details>
<summary>Correction</summary>

```python
try:
    appeler("POST", "/dpe", json=NOUVEAU_DPE)
except ApiErreur as e:
    print(e.code, e.message)   # 401 authentification requise

resultat = appeler("POST", "/dpe", json=NOUVEAU_DPE, headers=ENTETE_AUTH)
print(resultat["numero_dpe"])   # 2569E0000001A
```
</details>

3. Appeler `appeler("DELETE", "/dpe/2569E0000001A", headers=ENTETE_AUTH)` deux fois de suite. Que renvoie la fonction la première fois ? Et la seconde ?
<details>
<summary>Correction</summary>

```python
print(appeler("DELETE", "/dpe/2569E0000001A", headers=ENTETE_AUTH))   # None (204)
try:
    appeler("DELETE", "/dpe/2569E0000001A", headers=ENTETE_AUTH)
except ApiErreur as e:
    print(e.code)   # 404
```
Une suppression réussie renvoie `None` ; la seconde lève `ApiErreur` avec le code `404`.
</details>

4. Lire le détail d'une erreur `422` : pourquoi `appeler()` renvoie-t-il seulement le message « données invalides » ? Comment obtenir la liste des champs fautifs ?
<details>
<summary>Correction</summary>

La fonction ne garde que le message générique pour le code `422`. Pour obtenir les champs fautifs, il faut ajouter le corps de la réponse à l'exception : `reponse.json()["detail"]`. Dans un programme, la fonction peut stocker ce détail dans une propriété supplémentaire de `ApiErreur` :

```python
try:
    appeler("POST", "/dpe", json=dict(NOUVEAU_DPE, code_postal_ban="6910"), headers=ENTETE_AUTH)
except ApiErreur as e:
    print(e.code)   # 422
```

Pour afficher le détail, reprendre la requête avec `requests.post()` et lire `reponse.json()["detail"]` comme à l'exercice 3 :

```python
import requests

reponse = requests.post(
    f"{BASE}/dpe",
    json=dict(NOUVEAU_DPE, code_postal_ban="6910"),
    headers=ENTETE_AUTH,
)

if not reponse.ok:
    print(reponse.status_code)              # 422
    for erreur in reponse.json()["detail"]:
        print(erreur["loc"], erreur["msg"])
```
</details>

5. Quelle est la différence entre `response.ok` et `response.raise_for_status()` ? Écrire la requête `appeler("GET", "/dpe/ZZZZ00000")` version `requests` avec `raise_for_status()`, et intercepter l'erreur.
<details>
<summary>Correction</summary>

`response.ok` renvoie `True` ou `False` et laisse le programme décider quoi faire. `raise_for_status()` lève une exception pour toute erreur `4xx` ou `5xx`.

`response.ok` convient quand on veut traiter les codes différemment (un `404` n'est pas un bug, un `500` peut l'être). `raise_for_status()` convient quand toute erreur HTTP doit interrompre le traitement. La fonction `appeler()` combine les deux approches.

```python
reponse = requests.get(f"{BASE}/dpe/ZZZZ00000", timeout=2)
try:
    reponse.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(e)   # 404 Client Error: Not Found for url: http://127.0.0.1:8000/dpe/ZZZZ00000
```
</details>

## Exercice 8 – Timeouts et réessais

Le paramètre `timeout` protège le programme contre un serveur qui ne répond pas. La route `/lent?secondes=` attend le nombre de secondes demandé avant de répondre, ce qui permet de voir le délai en action.

Le paramètre `timeout` peut être un nombre (délai pour la connexion et la réception) ou un couple `(connexion, lecture)`.

### Mémo

| Nom de la commande | Description | Exemple |
|--------------------|-------------|---------|
| `timeout=2` | Délai unique, en secondes. | `requests.get(url, timeout=2)` |
| `timeout=(3, 5)` | Délai de connexion de 3 s, délai de lecture de 5 s. | |
| `requests.exceptions.ReadTimeout` | Le serveur a accepté la connexion mais n'a pas répondu à temps. | |
| `time.sleep()` | Attend un nombre de secondes avant de continuer. | `time.sleep(1)` |

### Exemple

```python
import requests

try:
    reponse = requests.get(f"{BASE}/lent", params={"secondes": 3}, timeout=2)
    print(reponse.json())
except requests.exceptions.ReadTimeout:
    print("Pas de réponse en 2 secondes.")
# Pas de réponse en 2 secondes.
```

### Exercices

1. Appeler `/lent` avec `secondes=1` et `timeout=2`, puis avec `secondes=3` et `timeout=2`. Quel est le résultat de chaque appel ?
<details>
<summary>Correction</summary>

```python
import time

for secondes in [1, 3]:
    debut = time.time()
    try:
        reponse = requests.get(f"{BASE}/lent", params={"secondes": secondes}, timeout=2)
        print(secondes, "OK", reponse.status_code, round(time.time() - debut, 1), "s")
    except requests.exceptions.ReadTimeout:
        print(secondes, "ReadTimeout", round(time.time() - debut, 1), "s")
```

Résultat constaté : `1 OK 200 1.0 s` puis `3 ReadTimeout 2.0 s`. Le délai est mesuré sur l'attente de la réponse : le programme ne reste pas bloqué 3 secondes.
</details>

2. Appeler `/lent` avec `secondes=3` et `timeout=(3, 5)`. Que se passe-t-il, et pourquoi ?
<details>
<summary>Correction</summary>

```python
reponse = requests.get(f"{BASE}/lent", params={"secondes": 3}, timeout=(3, 5))
print(reponse.status_code)   # 200
```

Le délai de lecture (5 s) dépasse l'attente de 3 secondes : la réponse arrive à temps. Le délai de connexion (3 s) ne joue pas ici, car la connexion s'établit immédiatement.
</details>

3. Écrire une fonction `appeler_avec_reessais()` qui relance la requête jusqu'à 3 fois en cas de `timeout`, avec une pause d'une seconde entre deux essais. Tester avec `/lent?secondes=3`.
<details>
<summary>Correction</summary>

```python
import time

def appeler_avec_reessais(methode, chemin, tentatives=3, **kwargs):
    """Relance la requête après un timeout, jusqu'au nombre de tentatives demandé."""
    for essai in range(1, tentatives + 1):
        try:
            return appeler(methode, chemin, **kwargs)
        except ApiErreur as e:
            if e.code != "timeout" or essai == tentatives:
                raise
            print(f"Essai {essai} : délai dépassé, nouvel essai dans 1 s")
            time.sleep(1)

try:
    appeler_avec_reessais("GET", "/lent", params={"secondes": 3})
except ApiErreur as e:
    print("Abandon :", e.code, e.message)
```

Résultat : deux messages « Essai ... », puis `Abandon : timeout pas de réponse dans le délai`.
</details>

4. Pourquoi ne relance-t-on pas automatiquement un `POST` de la même façon ? Tester avec un `POST` sur `/dpe` et une requête dont la réponse arrive après le délai.
<details>
<summary>Correction</summary>

Un `POST` peut avoir été **traité** par le serveur même si la réponse n'a pas été reçue à temps. Le relancer peut créer un doublon, ou produire un `409` difficile à interpréter. Un `GET`, un `PUT` ou un `DELETE` peuvent en général être relancés sans risque, car leur répétition donne le même résultat (`PUT`) ou un état déjà atteint (`DELETE` renvoie alors `404`).

Règle pratique : relancer automatiquement les lectures (`GET`) ; pour une écriture, vérifier d'abord si la ressource existe avant de renvoyer la requête.
</details>

> **Note : un timeout ne veut pas dire que l'action a échoué**
> Quand un timeout survient, le serveur a pu terminer le travail sans que le client le sache. C'est la raison de la règle ci-dessus.

## Liens utiles

- [Documentation de requests : timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
- [Documentation de requests : authentification](https://requests.readthedocs.io/en/latest/user/authentication/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Codes de réponse HTTP (MDN)](https://developer.mozilla.org/fr/docs/Web/HTTP/Status)
- [Postman : télécharger l'application](https://www.postman.com/downloads/)
