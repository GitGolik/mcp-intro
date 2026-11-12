# MCP Intro — Programming Learning Server

Ce projet met en place un serveur MCP simple qui expose des données de révision en programmation à un client ou à un agent.

L’objectif est de permettre à un agent de répondre à des questions comme :

> « Je veux étudier les décorateurs Python. Que dois-je réviser en premier ? »

Pour cela, le serveur expose des informations sur des notions de programmation, tandis que le client ou l’agent les utilise pour construire une réponse utile.

## MCP Architecture Summary

**MCP (Model Context Protocol)** est un protocole qui permet à une application d’IA de communiquer avec des capacités externes de façon standardisée. Au lieu de créer une intégration spécifique pour chaque base de données, fichier ou API, un développeur peut exposer ces fonctionnalités dans un serveur MCP.

Dans ce projet, l’architecture est la suivante :

```text
Étudiant
   ↓
Agent / application hôte
   ↓
Client MCP
   ↓
Serveur MCP de programmation
   ↓
Données locales (topics.json)
```

### Rôle du MCP host

Le **MCP host** est l’application qui gère l’interaction globale avec l’utilisateur. Il reçoit la demande, choisit les capacités à utiliser et produit la réponse finale.

Dans ce projet, l’agent est le host : il reçoit une question comme *« Je veux réviser les décorateurs Python, que dois-je voir en premier ? »* et décide de demander au serveur les informations nécessaires.

### Rôle du MCP client

Le **MCP client** est le composant qui communique directement avec un serveur MCP. Il découvre les outils et les ressources disponibles, envoie les requêtes et récupère les résultats.

Un host peut utiliser plusieurs clients, car il peut être connecté à plusieurs serveurs. Dans ce projet, le client se connecte uniquement au serveur de programmation local.

### Rôle du MCP server

Le **MCP server** est le programme qui expose des capacités aux clients MCP. Il ne décide pas seul de la réponse à donner à l’utilisateur : il fournit des fonctions et des données que le client peut utiliser.

Ici, `server/learning_server.py` expose des informations sur les notions de programmation, comme les fonctions, les décorateurs ou les structures de données.

### Tools et resources

Les **tools** sont des fonctions que le client peut appeler pour effectuer une action ou obtenir un résultat calculé. Par exemple, `search_topics("decorators")` pourrait rechercher les notions liées aux décorateurs.

Les **resources** sont des contenus que le client peut consulter, généralement en lecture seule. Par exemple, une resource `learning://topics` pourrait retourner le catalogue complet des notions disponibles.

| Notion | Tool | Resource |
|---|---|---|
| Utilisation | Appel d’une fonction | Lecture d’un contenu |
| Exemple | Rechercher un thème | Consulter le catalogue |
| Objectif | Effectuer une action ou un traitement | Fournir des données |
| Exemple dans ce projet | `search_topics` | `learning://topics` |

### Principe de sécurité

Un serveur MCP devrait exposer uniquement les capacités réellement nécessaires. Cela limite les risques : un serveur qui donne accès à beaucoup de fichiers, de commandes ou de services sensibles augmente la surface d’attaque.

Dans ce projet, le serveur expose seulement des informations de révision en programmation. Il ne doit pas permettre de modifier le système, d’accéder à des fichiers personnels ou d’exécuter des commandes arbitraires.

## Structure du projet

```text
mcp-intro/
├── server/
│   ├── __init__.py
│   └── learning_server.py
├── client/
│   ├── __init__.py
│   ├── mcp_client.py
│   └── agent.py
├── data/
│   └── topics.json
├── output/
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

| Dossier ou fichier | Rôle |
|---|---|
| `server/` | Contient le serveur MCP et les capacités exposées |
| `client/` | Contient le client MCP et l’agent qui utilise le serveur |
| `data/` | Contient les données locales utilisées par le serveur |
| `output/` | Contient les sorties générées, comme une réponse d’exemple |
| `README.md` | Explique le projet, son installation et son utilisation |
| `requirements.txt` | Liste les dépendances Python |
| `.env.example` | Montre les variables de configuration sans contenir de secrets |
| `.gitignore` | Indique les fichiers qui ne doivent pas être versionnés |

## Installation

1. Clone ou crée le projet.
2. Crée un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Installe les dépendances :

```bash
pip install -r requirements.txt
```

4. Crée un fichier `.env` à partir de l’exemple, si nécessaire :

```bash
cp .env.example .env
```

Ne commit jamais le fichier `.env`, car il peut contenir des informations privées.

## Utilisation

### Lancer le serveur MCP

Depuis la racine du projet, active d’abord l’environnement virtuel :

```bash
source .venv/bin/activate
```

Puis lance le serveur :

```bash
python -m server.learning_server
```

Le serveur utilise le nom `Programming Learning Server`.

À ce stade, il ne contient pas encore de tools ni de resources. Son objectif est de démarrer correctement avant d’ajouter des fonctionnalités.

## Tests

Le serveur devra être testé avant d’être utilisé par l’agent.

Les tests prévus comprennent :

- Vérifier que les tools sont bien exposés.
- Appeler les tools avec des entrées valides.
- Vérifier le comportement en cas d’entrée inconnue.
- Consulter la resource du catalogue de notions.
- Vérifier que les opérations de lecture ne modifient pas les données.

## Limites actuelles

- Le serveur n’est pas encore implémenté.
- Les tools et la resource ne sont pas encore créés.
- Le fichier `data/topics.json` ne contient pas encore de données.
- Le client et l’agent ne sont pas encore connectés au serveur.
- Les instructions de lancement précises seront ajoutées lors des prochaines étapes.

## Sécurité et serveurs tiers

Avant d’utiliser un serveur MCP développé par un tiers, il faut vérifier :

- Qui développe et maintient le serveur.
- Quelles permissions il demande.
- Quels fichiers, services ou comptes il peut consulter.
- S’il peut modifier ou supprimer des données.
- S’il envoie des informations à l’extérieur.
- Comment les secrets et les identifiants sont gérés.
- Si les dépendances sont maintenues et à jour.

Un serveur MCP ne doit recevoir que les permissions strictement nécessaires à son fonctionnement.

## MCP Tools

### `search_topics`

Recherche des notions de programmation dans le fichier local `data/topics.json`.

La recherche porte sur :

- Le titre du thème.
- Le résumé.
- Les prérequis.
- Les concepts clés.

Le tool retourne une liste de thèmes correspondants. Si aucun thème ne correspond, il retourne une liste vide.

Exemple d’appel :

```json
{
  "query": "decorators"
}
```
### `get_topic_details`

Retourne les informations complètes d’un thème à partir de son identifiant unique.

Le tool attend un `topic_id`, par exemple :

```text
python-decorators
```

Si l’identifiant existe, il retourne toutes les informations du thème : titre, résumé, prérequis, concepts clés, erreurs fréquentes et idée d’exercice.

Si l’identifiant n’existe pas, il retourne un message d’erreur clair au lieu de provoquer une erreur Python.
