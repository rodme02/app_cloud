#!/bin/bash

# Verifica se foram passados dois argumentos
if [ "$#" -ne 2 ]; then
  echo "Uso: $0 <id> <nome>"
  exit 1
fi

# Atribui os argumentos a variáveis
ID=$1
NAME=$2

# Obtém o DNS usando o comando AWS CLI
DNS=$(aws cloudformation describe-stacks --stack-name RodStack --query "Stacks[0].Outputs[?OutputKey=='ALBDNSNameOutput'].OutputValue" --output text)

# Verifica se o DNS foi obtido com sucesso
if [ -z "$DNS" ]; then
  echo "Erro ao obter o DNS do load balancer"
  exit 1
fi

# Faz a requisição POST usando curl
curl -X POST "http://$DNS/create_user" -H "Content-Type: application/json" -d "{\"id\": $ID, \"name\": \"$NAME\"}"

# Verifica se a requisição curl foi bem-sucedida
if [ $? -ne 0 ]; then
  echo "Erro ao fazer a requisição POST"
  exit 1
fi

