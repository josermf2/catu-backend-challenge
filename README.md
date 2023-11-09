# Catu - Desafio Back

## 🏖️ Aloha!

Olá, jovem Padawan&reg;! Você está no repositório de desafios backend da Catu.

A proposta aqui é simples:

- Fazer um _fork_ do repositório
- Criar sua solução no seu repo
- Nos enviar o link para o seu repo, que deve ser público

## 📖 Catu Logger

O desafio consiste em criar uma API REST que consiga persistir logs. Como nós queremos ter log de tudo o que acontece no nosso WMS, já criamos um modelo com os seguintes atributos:

- Data de criação
- Usuário que executou a ação
- Tipo da ação (create, edit, update, delete)
- Tipo do objeto (string)
- Identificador do objeto (int)

Precisamos que seja possível realizar as seguintes operações utilizando a API:

- Criar um novo log, passando todos os atributos como um payload JSON
- Selecionar logs
  - Sem nenhum filtro
  - Filtrando por data de criação (inicio e fim)
  - Filtrando por usuário
- Selecionar, para cada dia, a quantidade de ações executadas (agrupadas por dia)
  - Pode receber um range de datas (inicio e fim)
    - Exemplo:
      - inicio: 04/11/2023
      - fim: 07/11/2023
      - response:
        - 04/11/2023: foram executados 12 CREATE, 15 EDIT, 10 UDPDATE e 0 DELETE
        - 05/11/2023: foram executados 5 CREATE, 11 EDIT, 5 UDPDATE e 0 DELETE
        - 06/11/2023: foram executados 2 CREATE, 7 EDIT, 3 UDPDATE e 6 DELETE
        - 07/11/2023: foram executados 0 CREATE, 0 EDIT, 0 UDPDATE e 0 DELETE

Ao fim do desafio você deverá ter três endpoints que farão os comportamentos acima serem possíveis.

> **Importante**: Não se preocupe em fazer o endpoint que agrupa por dia e conta as operações inteiramente utilizando o framework. Se quiser criar uma query SQL, pra nós funciona!

## 🔧 Stack

Este desafio foi criado utilizando **[Django](https://www.djangoproject.com/)**, mais especificamente o **[Django Rest Framework](https://www.django-rest-framework.org/)**, fazendo com que a linguagem utilizada seja Python.

Para executar o projeto, você precisa ter o python3 executando em sua máquina (ou um contâiner) e executar os comandos:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 8080
```

Ao executar o projeto, você terá:

- Uma requisição `GET` para `http://localhost:8080/log/hello-world` retornando `{
    "message": "Hello, world!"
}`

- Uma requisição `POST` para `http://localhost:8080/log/ping` com um payload `JSON`, retornando os dados da sua requisição

A partir dai é só você fazer sua mágica!

> **Importante**: você não precisa se preocupar com CORS, faça funcionar com seu app preferido de requisições para APIs

## O que estamos avaliando?

É sempre importante entendermos o motivo das coisas. Este teste pretende avaliar:

- Capacidade de avaliação de requisitos e de comunicação para tirar dúvidas
- Habilidade em começar e finalizar PoCs
- Estrutura lógica da solução
- Legibilidade e organização da solução

## 🖥️ É isso! Happy Coding!

Para sanar qualquer dúvida, entre em contato com o nosso time!
