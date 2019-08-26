# github_tags_manager
Gerenciador de tags - Desafio LabHacker

### Acessar a aplicação: [Clique](https://manage-git-tags.herokuapp.com/login/)

## Configuração local

- Criar aplicação de OAuth no Github
- Fornecer dados da Aplicação para o docker-compose
- No Github configurar a aplicação para retornar ao endpoint desejado como na imagem
- ![Exemplo de configuração das urls](https://i.imgur.com/KLl9Aww.jpg)

## Como subir a aplicação?

Utilizando o Docker, rodar o comando

```shell
$ docker-compose up --build -d
```

## Para parar a aplicação 
```shell
$ docker-compose stop
```