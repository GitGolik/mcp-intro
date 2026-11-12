# MCP Servers in Python

## Description

Ce projet implémente un serveur MCP simple en Python avec FastMCP. Il expose un petit catalogue local de notions de programmation à travers des tools et une resource MCP.

Un agent-like client se connecte ensuite au serveur, recherche un thème, récupère ses détails et génère une courte recommandation d’étude. Les données proviennent du fichier local `data/topics.json`.

Le projet couvre les thèmes suivants :

- Fonctions Python
- Listes Python
- Dictionnaires Python
- Décorateurs Python
- Pointeurs en C

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

Ici, `server/learning_server.py` expose des informations sur les notions de programmation.

### Tools et resources

Les **tools** sont des fonctions que le client peut appeler pour effectuer une action ou obtenir un résultat calculé. Par exemple, `search_topics("decorators")` recherche les notions liées aux décorateurs.

Les **resources** sont des contenus que le client peut consulter, généralement en lecture seule. Par exemple, la resource `topics://catalog` retourne le catalogue des thèmes disponibles.

| Notion | Tool | Resource |
|---|---|---|
| Utilisation | Appel d’une fonction | Lecture d’un contenu |
| Exemple | Rechercher un thème | Consulter le catalogue |
| Objectif | Effectuer une action ou un traitement | Fournir des données |
| Exemple dans ce projet | `search_topics` | `topics://catalog` |

### Principe de sécurité

Un serveur MCP devrait exposer uniquement les capacités réellement nécessaires. Cela limite les risques : un serveur qui donne accès à beaucoup de fichiers, de commandes ou de services sensibles augmente la surface d’attaque.

Dans ce projet, le serveur expose seulement des informations de révision en programmation. Il ne permet pas de modifier le système, d’accéder à des fichiers personnels ou d’exécuter des commandes arbitraires.

## Requirements

- Python 3.10 ou version plus récente
- FastMCP
- MCP Inspector, pour tester le serveur
- Node.js et npm, uniquement si tu utilises MCP Inspector via `npx`

## Setup

Depuis la racine du projet :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient :

```text
fastmcp
```

Ne commit jamais le fichier `.env`, s’il est utilisé. Le fichier `.env.example` sert uniquement de modèle.

## How to Run the Server

Depuis la racine du projet, avec l’environnement virtuel activé :

```bash
source .venv/bin/activate
python3 -m server.learning_server
```

Le serveur démarre avec le transport `stdio` et attend une connexion MCP.

Pour arrêter le serveur, utilise :

```text
Ctrl + C
```

## How to Test the Server

Le serveur a été testé avec MCP Inspector.

Dans un premier terminal, arrête tout serveur déjà lancé, puis lance l’Inspector depuis la racine du projet :

```bash
npx @modelcontextprotocol/inspector "$(which python3)" -m server.learning_server
```

Ouvre ensuite l’URL locale affichée par l’Inspector, généralement :

```text
http://localhost:6274
```

Dans l’interface :

1. Clique sur **Connect**.
2. Ouvre l’onglet **Tools**.
3. Vérifie que `search_topics` et `get_topic_details` apparaissent.
4. Teste les tools avec les exemples ci-dessous.
5. Ouvre l’onglet **Resources**.
6. Sélectionne `topics://catalog`.
7. Clique sur **Read Resource**.

### Tests réalisés

- Le serveur démarre avec `python3 -m server.learning_server`.
- Les tools `search_topics` et `get_topic_details` sont visibles dans MCP Inspector.
- `search_topics("decorators")` retourne le thème `Python Decorators`.
- `get_topic_details("python-decorators")` retourne les informations complètes du thème.
- Une recherche sans correspondance retourne une liste vide.
- Un identifiant inconnu retourne un message d’erreur clair.
- La resource `topics://catalog` retourne les identifiants et titres des thèmes disponibles.

### Exemple de test

Appel de `search_topics` avec la requête `decorators` :

```json
[
  {
    "id": "python-decorators",
    "title": "Python Decorators",
    "summary": "Learn how decorators modify or extend the behavior of functions without changing their code.",
    "key_concepts": [
      "Higher-order functions",
      "Wrapper functions",
      "The @decorator syntax",
      "Functions as arguments"
    ]
  }
]
```

Appel de `get_topic_details` avec un identifiant inconnu :

```json
{
  "error": "Topic not found.",
  "message": "No topic found with id 'unknown-topic'."
}
```

## How to Run the Agent

Le fichier `client/agent.py` implémente un agent-like client simple.

Il reçoit une question d’étudiant, se connecte au serveur MCP via le transport stdio, appelle `search_topics` puis `get_topic_details`, et génère une réponse à partir des données retournées par le serveur.

Depuis la racine du projet :

```bash
source .venv/bin/activate
python3 -m client.agent
```

L’agent utilise la question suivante :

```text
I want to study Python decorators. What should I review first?
```

Il enregistre ensuite une réponse d’exemple dans :

```text
output/sample_agent_response.md
```

L’agent n’importe pas directement les fonctions du serveur. Toutes les informations sur les thèmes sont obtenues à travers MCP.

## Available Tools

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

## Available Resources

### `topics://catalog`

Resource en lecture seule qui retourne le catalogue des thèmes disponibles.

Elle contient uniquement :

- L’identifiant de chaque thème (`id`).
- Le titre de chaque thème (`title`).

Elle ne retourne pas les prérequis, les concepts détaillés, les erreurs fréquentes ou les exercices. Pour obtenir ces informations, utiliser le tool `get_topic_details`.

## Third-Party MCP Server Review

### Server selected: Filesystem MCP Server

Le serveur examiné est `@modelcontextprotocol/server-filesystem`, un serveur MCP de référence qui permet de lire, créer, modifier, déplacer et rechercher des fichiers dans des dossiers autorisés.

C’est un serveur local : il est lancé sur la machine de l’utilisateur et communique avec le client MCP via stdio.

Il expose notamment des tools pour lire un fichier, lire plusieurs fichiers, écrire un fichier, créer un dossier, lister un dossier, déplacer un fichier, rechercher des fichiers et obtenir des métadonnées. Les fichiers des dossiers autorisés peuvent aussi être exposés comme resources lisibles.

Le serveur ne demande pas de clé API, mais il reçoit un accès au système de fichiers local. Son accès est limité aux répertoires passés en argument lors du lancement.

Le principal risque est qu’un agent puisse écraser, déplacer ou supprimer des fichiers dans le dossier autorisé. Le tool `write_file` peut remplacer un fichier existant sans avertissement.

Avant de l’utiliser, je limiterais l’accès à un dossier de test précis, par exemple `data/`, plutôt qu’au dossier personnel ou à la racine du système. Je vérifierais également la configuration avant le lancement.

## Example Output

Voici un exemple de réponse générée par l’agent pour la question :

```text
I want to study Python decorators. What should I review first?
```

```md
# Study Recommendation

## Recommended topic

**Python Decorators**

Learn how decorators modify or extend the behavior of functions without changing their code.

## Why this topic is relevant

This topic matches your request. Reviewing it will help you understand the
concepts and avoid common mistakes related to **Python Decorators**.

## Prerequisites

- Python functions
- Function arguments
- Scope

## Key concepts

- Higher-order functions
- Wrapper functions
- The @decorator syntax
- Functions as arguments

## Practice idea

Create a decorator that prints a message before and after a function call.

## Common mistakes to avoid

- Forgetting to return the wrapper function
- Forgetting to call the original function inside the wrapper
- Using a decorator before understanding nested functions
```

## Known Limitations

- Le catalogue contient seulement cinq thèmes.
- La recherche est basée sur une simple correspondance de texte, sans recherche sémantique.
- L’agent choisit toujours le premier résultat retourné par `search_topics`.
- L’agent ne gère pas les questions ambiguës ni les conversations sur plusieurs tours.
- L’agent n’utilise pas de modèle de langage : il formate directement les données retournées par MCP.
- La resource `topics://catalog` expose seulement les identifiants et les titres, pas les détails complets.
- Le serveur utilise un fichier JSON local ; il ne se connecte pas à une base de données ou à une API externe.

## Reflection

### What problem does MCP solve?

MCP résout le problème de l’intégration répétée entre les applications d’IA et les systèmes externes. Au lieu de créer une intégration différente pour chaque API, base de données ou service, un développeur peut exposer ses capacités dans un serveur MCP standardisé.

### What is the difference between an MCP tool and an MCP resource?

Un tool est une fonction que le client peut appeler pour effectuer une action ou obtenir un résultat. Une resource est un contenu que le client peut consulter, généralement en lecture seule.

Dans ce projet, `search_topics` et `get_topic_details` sont des tools, tandis que `topics://catalog` est une resource.

### What does your MCP server expose?

Le serveur expose deux tools et une resource :

- `search_topics` : recherche des thèmes de programmation.
- `get_topic_details` : retourne les détails complets d’un thème.
- `topics://catalog` : retourne le catalogue des thèmes disponibles.

### How does your agent use the MCP server?

L’agent reçoit une question, se connecte au serveur via MCP, appelle `search_topics` pour trouver un thème correspondant, puis appelle `get_topic_details` avec l’identifiant du premier résultat. Il utilise ensuite les données retournées pour générer une recommandation d’étude.

### What should you check before using a third-party MCP server?

Avant d’utiliser un serveur MCP tiers, il faut vérifier son origine, les permissions demandées, les fichiers ou services accessibles, les actions possibles, la gestion des secrets et la maintenance du projet. Il faut aussi limiter les permissions au strict minimum nécessaire.

### What limitation did you observe in your implementation?

La principale limitation est que l’agent choisit toujours le premier résultat de recherche. Si plusieurs thèmes correspondent à une requête, il ne demande pas à l’utilisateur de choisir ni n’analyse automatiquement quelle option est la plus pertinente.

Une autre limite est que la recherche repose sur une correspondance simple de texte. Une recherche avec des mots très différents de ceux du catalogue peut ne retourner aucun résultat, même si le sujet est proche.
