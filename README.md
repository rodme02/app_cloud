# app_cloud

Documentação Técnica de Implementação de Arquitetura Cloud na AWS
1. Introdução
Este documento descreve a implementação de uma arquitetura cloud na AWS utilizando o CloudFormation. O objetivo é provisionar uma infraestrutura que inclui um Application Load Balancer (ALB), instâncias EC2 com Auto Scaling e um banco de dados DynamoDB. Este guia detalha as decisões técnicas tomadas, o processo de implementação e a estimativa de custos associada.

2. Objetivo
Provisionar uma arquitetura na AWS utilizando CloudFormation, incluindo:

Application Load Balancer (ALB)
Instâncias EC2 com Auto Scaling
Banco de dados DynamoDB
3. Escolha da Região
A escolha da região AWS é baseada na otimização de custos e desempenho. Após análise, a região selecionada foi us-east-1 devido ao menor custo de recursos e alta disponibilidade.

4. Requisitos Técnicos
4.1 Infraestrutura como Código (IaC) com CloudFormation
Utilizar CloudFormation para criar e gerenciar todos os recursos na AWS.
Estruturar o código com comentários explicativos para cada recurso.
O script deve permitir criar, atualizar e destruir a infraestrutura com um único comando.
4.2 EC2 com Auto Scaling
Criar um Launch Configuration com uma AMI que tenha a aplicação pré-instalada.
Provisionar um Auto Scaling Group (ASG) utilizando o Launch Configuration.
Definir políticas de escalabilidade baseadas em CloudWatch Alarms (ex: CPU Utilization > 70%).
Garantir a integração do ASG com o ALB através do Target Group.
4.3 Application Load Balancer (ALB)
Provisionar um ALB para distribuir o tráfego entre as instâncias EC2.
Configurar Target Groups para gerenciar as instâncias EC2.
Implementar Health Checks para garantir que o tráfego seja direcionado apenas para instâncias saudáveis.
4.4 Banco de Dados DynamoDB
Provisionar uma instância DynamoDB.
Configurar Security Groups para garantir que apenas as instâncias EC2 possam se conectar ao banco de dados.
5. Diagrama da Arquitetura AWS

6. Decisões Técnicas
6.1 Infraestrutura como Código (IaC)
Utilizamos CloudFormation para garantir a replicabilidade e a facilidade de gestão da infraestrutura. Cada recurso foi comentado detalhadamente para facilitar o entendimento e a manutenção.

6.2 Auto Scaling e Load Balancing
O uso de Auto Scaling garante a alta disponibilidade e a escalabilidade da aplicação, enquanto o ALB distribui o tráfego de forma eficiente entre as instâncias.

6.3 Segurança
Foram configurados Security Groups para restringir o acesso ao DynamoDB apenas às instâncias EC2, garantindo a segurança dos dados.

7. Guia Passo a Passo
7.1 Preparação
Faça o download dos scripts CloudFormation do repositório: Link para o Repositório.
7.2 Criação da Infraestrutura
Execute o comando abaixo para criar a infraestrutura:

sh
Copy code
aws cloudformation create-stack --stack-name NomeDoStack --template-body file://caminho/para/o/template.yaml --parameters file://caminho/para/os/parametros.json
7.3 Atualização da Infraestrutura
Para atualizar a infraestrutura, execute:

sh
Copy code
aws cloudformation update-stack --stack-name NomeDoStack --template-body file://caminho/para/o/template.yaml --parameters file://caminho/para/os/parametros.json
7.4 Destruição da Infraestrutura
Para destruir a infraestrutura, execute:

sh
Copy code
aws cloudformation delete-stack --stack-name NomeDoStack
8. Análise de Custo com a Calculadora AWS
8.1 Estimativa de Custos
A tabela abaixo apresenta uma estimativa dos custos mensais associados à arquitetura proposta:

Recurso	Custo Mensal Estimado
EC2 (Auto Scaling)	$XX.XX
Application Load Balancer	$XX.XX
DynamoDB	$XX.XX
Total	$XX.XX
8.2 Otimizações de Custo
Para otimizar custos, recomenda-se:

Utilizar instâncias reservadas ou spot instances para as EC2.
Monitorar o uso do DynamoDB para ajustar a capacidade provisionada.
9. Conclusão
Este documento descreve a implementação de uma arquitetura cloud na AWS utilizando CloudFormation, com ênfase na criação automatizada e gerenciamento de recursos essenciais como ALB, EC2 com Auto Scaling e DynamoDB. A análise de custo e as otimizações propostas visam garantir a eficiência econômica e operacional da solução.

Para qualquer dúvida ou suporte, consulte o repositório do projeto ou entre em contato com o administrador do sistema.
