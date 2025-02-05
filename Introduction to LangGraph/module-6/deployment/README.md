# Local deployment steps

## CLI

```
pip install -U langgraph-cli
```

## Build Docker Image for LangGraph Server

```
# 'my_image' porque es lo que pone en el docker-compose.yml; si se cambia ahí, cambiar aquí también
$ cd module-6/deployment
$ langgraph build -t my-image
```

Se puede hacer directamente con docker:

```
# Generar el dockerfile
$ langgraph dockerfile ./Dockerfile
```

```
$ docker build -t my-image .
```

Ya se puede lanzar:

```
docker-compose up -d
```

# Launch

En el mismo directorio tiene que haber un archivo '.env' con las siguientes variables de entorno:

- `OPENAI_API_KEY`
- `LANGSMITH_API_KEY`

```
docker compose up
```

# Connect

Once running, we can access the deployment through:

API: http://localhost:8123
Docs: http://localhost:8123/docs
LangGraph Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123

# Stop

```
docker compose down
```
