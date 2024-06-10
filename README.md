# Chat Application service

This project is a Django-based chat application that uses Django Channels for WebSocket communication and Kafka for message brokering. The project uses Docker Compose for container orchestration.

## Prerequisites

- Docker
- Docker Compose


## Setting Up the Project

1. **Clone the repository:**

   ```bash
   git clone git@github.com:AbdallahMGomaa/chatApp.git
   cd chatApp
   ```
   
2. **Create .env file:**
    ```bash
    touch .env
    ```
3. **Add the following environment variables to the .env file:**
    ```makefile
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=*
    
    POSTGRES_HOST=db
    POSTGRES_DB=chat_db
    POSTGRES_USER=chat_user
    POSTGRES_PASSWORD=password
    POSTGRES_PORT=5432
    
    ZOOKEEPER_PORT=2181
    
    KAFKA_BROKER_URL=kafka:9092
    KAFKA_BROKER_ID=1
    KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
    KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
    
    REDIS_HOST=redis
    REDIS_PORT=6379
    
    DJANGO_PORT=8000
    GUNICORN_WORKERS=3
    ```
4. **Build and run docker containers:**
   ```bash
   docker-compose up --build
   ```
   
## Usage

- Access the Django admin panel at `http://localhost:8000/admin`
- Connect to Websocket endpoint on `ws://localhost:8000/ws/chat/`
- Use postman for testing REST APIs or Websockets, import the postman collection `Chat app.postman_collection.json` into postman.

## Websocket terminal client for testing
