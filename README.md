# DATA-API

Ce référentiel regroupe les supports de la formation « Bases de Python & Manipulation de Données ». Le fil rouge est la récupération et l'exploitation des DPE (diagnostics de performance énergétique) via l'API de l'ADEME.

Les données sont celles de l'API ADEME (jeu `dpe03existant`), les mêmes que celles utilisées dans le repo `data-science-python`. Les appels filtrent les résultats sur un département (`code_departement_ban`) ou un code postal (`code_postal_ban`).

Les exercices sont réalisés en Python 3.12, dans Visual Studio Code, avec des notebooks Jupyter pour l'exploration et des scripts pour les appels API. Les API ADEME sont complétées par une API de test FastAPI lancée en local, décrite plus bas.

## Public et prérequis

La formation s'adresse aux développeurs ayant déjà une expérience en programmation (C++, C#, Java ou équivalent) et souhaitant découvrir Python pour interagir avec des API REST et manipuler des données.

Aucune connaissance préalable de Python, Pandas ou de l'API ADEME n'est requise.

Avant la formation, il faut disposer de :

- Python 3.10 à 3.12 installé sur le poste ;
- Visual Studio Code, avec la possibilité d'installer des extensions ;
- un navigateur Web récent ;
- une connexion Internet permettant d'accéder aux API utilisées ;
- Postman installé sur le poste.

## Modalités d'évaluation

Les acquis sont évalués progressivement à travers des exercices pratiques et des mises en situation : prise en main de Python, communication avec une API REST, gestion de l'authentification et exploitation des données récupérées.

## Objectifs

- [ ] Découvrir Python, son écosystème (`pip`, environnements virtuels) et son environnement de développement (Visual Studio Code, Jupyter Notebook)
- [ ] Manipuler les variables, les principaux types de données, les listes et les dictionnaires
- [ ] Comprendre le fonctionnement d'une API REST et des échanges HTTP
- [ ] Utiliser la documentation d'une API pour construire une requête adaptée
- [ ] Interroger une API avec `requests` (`GET`, paramètres, pagination dans une boucle) et lire une réponse JSON
- [ ] Transformer les données récupérées en DataFrame Pandas, puis les filtrer, les sélectionner et les organiser
- [ ] Utiliser les principales méthodes HTTP : `GET`, `POST`, `PUT` et `DELETE`
- [ ] Gérer l'authentification d'une API (clé d'API, Bearer Token)
- [ ] Exploiter les codes de réponse HTTP et gérer les erreurs, exceptions et timeouts
- [ ] Tester une API avec Postman avant de l'implémenter en Python

## API de test

En plus des API de l'ADEME, la formation utilise une API FastAPI développée en local, lancée avec uvicorn, sans Docker. Elle reprend les bases vues dans le chapitre 6 du repo M2-SISE et ajoute les routes et mécanismes nécessaires aux chapitres 2 et 3 : `GET`, `POST`, `PUT` et `DELETE`, ainsi qu'une authentification par clé d'API ou Bearer Token.

Les données sont stockées dans une petite base SQLite, alimentée au démarrage par un extrait de DPE. Les routes `GET`, `POST`, `PUT` et `DELETE` lisent et modifient cette base, ce qui permet de tester chaque route sur des données réelles sans dépendre d'un service distant.

Son fonctionnement sert de support de test :

- les requêtes sont d'abord testées dans Postman ;
- puis implémentées en Python avec `requests` ;
- la documentation interactive de l'API est disponible via Swagger UI (`/docs`).

## Planning

1. Chapitre 1 : Prise en main de Python (caractéristiques et domaines d'usage, syntaxe, `pip` et environnements virtuels, Visual Studio Code, Jupyter Notebook, variables et types de données, listes et dictionnaires)
2. Chapitre 2 : Récupérer et exploiter des données d'une API avec Python et Pandas (fonctionnement d'une API REST, bibliothèque `requests`, méthode `GET`, lecture de la documentation d'une API, paramètres, interrogation de l'API ADEME dans une boucle sur les pages, parcours du JSON, sélection des informations utiles, transformation en DataFrame, filtre, sélection et organisation des données, exploitation dans un notebook Jupyter)
3. Chapitre 3 : Consommer des API REST en profondeur (méthodes `POST`, `PUT` et `DELETE`, headers, authentification par clé d'API ou Bearer Token, codes de réponse HTTP, gestion des erreurs et exceptions, timeouts). Les requêtes sont testées dans Postman sur l'API FastAPI locale avant d'être implémentées en Python.

## Fonctions abordées

| Chapitre | Fonctions et packages |
|----------|-----------------------|
| 1 | `print()`, `type()`, `input()`, `if`, `for`, `while`, `def`, `list`, `dict`, `append()`, `len()`, `pip install`, `python -m venv`, `ipykernel` |
| 2 | `requests.get()`, `params=`, `response.json()`, `response.status_code`, `pd.DataFrame()`, `pd.json_normalize()`, `head()`, `info()`, `describe()`, `loc[ , ]`, `query()`, `sort_values()`, `groupby()`, `value_counts()`, `to_csv()`, `read_csv()` |
| 3 | `requests.post()`, `requests.put()`, `requests.delete()`, `headers=`, `timeout=`, `json=`, `response.raise_for_status()`, `requests.exceptions.RequestException`, `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, `requests.exceptions.HTTPError`, `try` / `except` |

## Liens utiles

- [Données DPE de l'ADEME](https://data.ademe.fr/datasets/dpe03existant)
- [Documentation de l'API ADEME (dataset dpe03existant)](https://data.ademe.fr/datasets/dpe03existant/api-doc?operation=readLines)
- [Documentation de la bibliothèque requests](https://requests.readthedocs.io/)
- [Documentation de Pandas](https://pandas.pydata.org/docs/)
- [Documentation de FastAPI](https://fastapi.tiangolo.com/)
- [Postman](https://www.postman.com/downloads/)
