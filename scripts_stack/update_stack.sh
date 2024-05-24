#!/bin/bash

echo "Atualizando a stack..."

# Atualizando a stack
aws cloudformation update-stack --stack-name RodStack --template-body file://projeto_aws.yaml --capabilities CAPABILITY_IAM

# Verificando se a atualização foi bem sucedida
if [ $? -eq 0 ]; then
    echo "Aguardando a atualização da stack..."

    # Aguardando a atualização da stack
    aws cloudformation wait stack-update-complete --stack-name RodStack

    # Verificando se a stack foi atualizada com sucesso
    if [ $? -eq 0 ]; then
        echo "Stack atualizada com sucesso."
    else
        echo "Erro ao aguardar a atualização da stack."
    fi
else
    echo "Erro ao atualizar a stack."
fi
