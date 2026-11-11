# MCP Intro — Programming Learning Server

Ce projet met en place un serveur MCP simple qui expose des données
de révision en programmation à un client ou à un agent.

## Structure

- `server/` : serveur MCP
- `client/` : client et agent consommant le serveur
- `data/` : données locales
- `output/` : sorties générées
- `README.md` : documentation du projet
- `requirements.txt` : dépendances Python
- `.env.example` : exemple de variables d’environnement
- `.gitignore` : fichiers à ne pas versionner

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## À faire

- Créer les MCP tools dans `server/learning_server.py`
- Créer une MCP resource dans `server/learning_server.py`
- Remplir `data/topics.json`
- Implémenter le client dans `client/mcp_client.py`
- Implémenter l’agent dans `client/agent.py`
