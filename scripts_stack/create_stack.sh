#!/bin/bash

echo "Criando a stack..."

# Criando a stack
aws cloudformation create-stack --stack-name RodStack --template-body file://projeto_aws.yaml --capabilities CAPABILITY_IAM

# Verificando se a criação foi bem sucedida
if [ $? -eq 0 ]; then
    echo "Aguardando a criação da stack..."

    # Aguardando a criação da stack
    aws cloudformation wait stack-create-complete --stack-name RodStack

    # Verificando se a stack foi criada com sucesso
    if [ $? -eq 0 ]; then
        output=$(aws cloudformation describe-stacks --stack-name RodStack --query "Stacks[0].Outputs[?OutputKey=='ALBDNSNameOutput'].OutputValue" --output text)
        echo "Stack criada com sucesso."
        echo "DNS: $output"
    else
        echo "Erro ao aguardar a criação da stack."
    fi
else
    echo "Erro ao criar a stack."
fi
