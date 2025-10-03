
# COMMENTS.md — Guia de execução

Este projeto expõe uma API FastAPI que simula um jogo hipotético muito semelhante a Banco Imobiliário, onde várias de suas mecânicas foram simplificadas. Numa partida desse jogo, os
jogadores se alteram em rodadas, numa ordem definida aleatoriamente no começo da partida com quatro jogadores com as seguintes caracteristicas:
impulsivo, exigente, cauteloso e aleatorio.

## Para executar o projeto
é necessario ter o docker instalado na maquina
ter o git intalado na maquina
clonar o projeto

## Link para instalação do docker
https://docs.docker.com/compose/install/

## Subir com Docker Compose ()
No terminal no caminho do projeto clonado execute
docker compose up --build 

Ou para executar em segundo plano e deixar o terminal livre
docker compose up -d --build

A API fica em `http://localhost:8080`

- Endpoint: `POST /jogo/simular`
- Swagger: `http://localhost:8080/docs`

## Teste rápido
curl.exe -X POST "http://localhost:8080/jogo/simular"

## Pelo Postman
Crie uma requisição POST para:

"http://localhost:8080/jogo/simular"

## Controlar rodadas
curl.exe -X POST "http://localhost:8080/jogo/simular?max_rodadas=500"

## Encerrar os containers
docker compose down
