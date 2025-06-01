## 📘 Docker Compose конфігурація

Цей файл описує налаштування та запуск трьох сервісів:  
сервер документації, локальна база даних PostgreSQL та бекенд API на FastAPI.
Фаїл [docker-compose.yaml](..%2F..%2Fdocker-compose.yaml)

### 🔧 Основний код

```yaml
services:
  documentation:
    image: squidfunk/mkdocs-material:latest
    container_name: mkdocs_graduationproject
    command: serve --dev-addr=0.0.0.0:2638 --watch-theme
    restart: unless-stopped
    ports:
      - "2638:2638"
    volumes:
      - ./documentation:/docs:ro

  local_database:
    image: postgres:16-alpine
    container_name: groupproject_database
    hostname: local_database
    restart: always
    env_file:
      - .env
    ports:
      - "6661:${POSTGRES_PORT}"
    volumes:
      - postgres_datastorage:/var/lib/postgresql/data
    networks:
      - main_network

  backend_api:
    build:
      dockerfile: Dockerfile
      context: ./backend_api
    container_name: backend_api_course_project
    hostname: backend_api
    restart: always
    env_file:
      - .env
    volumes:
      - ./backend_api/app:/app
    ports:
      - "4321:4321"
    command: |
      sh -c "
      uvicorn main:app --port=4321 --host=0.0.0.0 --reload
      "
    networks:
      - main_network

networks:
  main_network:
    driver: bridge

volumes:
  postgres_datastorage:
    external: false
