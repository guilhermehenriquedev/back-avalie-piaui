
# API Avalie PI

Sistema de integração para sistema de avaliação do estado do Piaui

## Instalação

Faça o clone do projeto via SSH, após, com o python 3.10 instalado na maquina faça os procedimentos a seguir

```bash
  1. git@gitlab.ati.pi.gov.br:seadpi/api-avalie.git
  2. python3 -m venv venv #criando ambiente virtual
  3. source venv/bin/activate #entrando no ambiente virtual
```

Faça a instalação do pacotes do projeto.
```bash
  1. pip install -r requirements.txt
```

Crie o arquivo de configuração da aplicação com o .env na raiz do projeto
```bash
  ENVIRONMENT=TST
  ALLOWED_HOSTS=*
  DB_NAME=name_db
  DB_USER=user_db
  DB_PASSWORD=pass_db
  DB_HOST=host_db
  DB_PORT=port_db
```

Após com as configurações efetuadas, faça as mirgações do banco de dados.
```bash
  1. python manage.py makemigrations
  2. python manage.py migrate
```
