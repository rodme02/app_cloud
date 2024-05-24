#!/bin/bash

echo "Deletando a stack..."

# Deletando a stack
aws cloudformation delete-stack --stack-name RodStack

# Verificando se a deleção foi bem sucedida
if [ $? -eq 0 ]; then
    echo "Aguardando a deleção da stack..."

    # Aguardando a deleção da stack
    aws cloudformation wait stack-delete-complete --stack-name RodStack

    # Verificando se a stack foi deletada com sucesso
    if [ $? -eq 0 ]; then
        echo "Stack deletada com sucesso."
    else
        echo "Erro ao aguardar a deleção da stack."
    fi
else
    echo "Erro ao deletar a stack."
fi
