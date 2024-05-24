#!/bin/bash

# Verifica se foi passado um argumento
if [ "$#" -ne 1 ]; then
  echo "Uso: $0 <id>"
  exit 1
fi

# Atribui o argumento a uma variável
ID=$1

# Obtém o DNS usando o comando AWS CLI
DNS=$(aws cloudformation describe-stacks --stack-name RodStack --query "Stacks[0].Outputs[?OutputKey=='ALBDNSNameOutput'].OutputValue" --output text)

# Verifica se o DNS foi obtido com sucesso
if [ -z "$DNS" ]; then
  echo "Erro ao obter o DNS do load balancer"
  exit 1
fi

# Faz a requisição DELETE usando curl
curl -X DELETE "http://$DNS/delete_user/$ID"

# Verifica se a requisição curl foi bem-sucedida
if [ $? -ne 0 ]; then
  echo "Erro ao fazer a requisição DELETE"
  exit 1
fi
