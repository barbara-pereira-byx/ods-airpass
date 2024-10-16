# Sistema de Gestão de Reservas Aéreas

Este projeto é um sistema de gestão de reservas aéreas desenvolvido em Python usando o framework Django. Ele permite o cadastro e gerenciamento de voos, reservas, passageiros e pilotos, com acesso restrito aos funcionários que realizam e gerenciam esses processos.

## Descrição Geral: 
O ODS AirPass é um software crucial para o sucesso da gestão de reservas em voos nacionais e internacionais, prestando apoio aos funcionários de aeroportos na execução de tarefas cotidianas e significantes. Através dele, é possível obter reservas flexíveis e exclusivas, razão pela qual garante o conforto do cliente e o apoio imediato diante de imprevistos indesejáveis. Além da realização das reservas, o software conta com um estruturado Sistema de Gerenciamento de Banco de Dados, que armazena informações relevantes sobre as reservas, aviões, voos, pilotos, passageiros e funcionários.


## Requisitos

Antes de iniciar, certifique-se de que você tem os seguintes softwares instalados:

- Python 3.11 ou superior
- Git
- Pip (gerenciador de pacotes do Python)
- Virtualenv (para criar um ambiente virtual)

## Instalação

Siga os passos abaixo para clonar o repositório, configurar o ambiente virtual, instalar as dependências e rodar o projeto localmente.

### 1. Clone o Repositório

Abra o terminal e execute o seguinte comando para clonar o projeto:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

### 2. Crie e Ative o Ambiente Virtual

Para isolar as dependências do projeto, você deve criar um ambiente virtual:

Linux/MacOS
```bash
cd seu-repositorio
python3 -m venv venv
source venv/bin/activate
```


Windows
```bash
cd seu-repositorio
python -m venv venv
venv\Scripts\activate
```

### 3.  Instale as Dependências

Com o ambiente virtual ativo, instale as dependências do projeto executando:

```bash
pip install -r requirements.txt
```

### 4.  Configure o Banco de Dados

1. Instale o MySQL
Se você ainda não tem o MySQL instalado, faça o download e instale a versão apropriada para o seu sistema operacional a partir do site oficial do MySQL.

2. Crie o Banco de Dados
Após instalar o MySQL, entre no MySQL como root ou com um usuário que tenha permissões de criação:

```bash
mysql -u root -p
```
Crie o banco de dados com o nome ods_airpass_db:

```sql
CREATE DATABASE ods_airpass_db;
```
3. Instale o Conector MySQL para Python
Certifique-se de que o pacote mysqlclient está listado no seu requirements.txt. Caso ainda não esteja, adicione-o manualmente ou instale via pip:

```bash
pip install mysqlclient
```
4. Aplique as Migrações
Agora, com o banco de dados MySQL configurado, execute as migrações para criar as tabelas no banco:

```bash
python manage.py migrate
```
Depois disso, seu banco de dados MySQL estará pronto para uso no projeto!

### 5.  Crie um Superusuário (Opcional)

Crie as tabelas necessárias no banco de dados. Por padrão, o projeto usa o SQLite, que já vem configurado no Django para desenvolvimento local:

```bash
python manage.py createsuperuser
```
### 6.  Execute o Servidor de Desenvolvimento
Agora você pode rodar o servidor localmente:


```bash
python manage.py runserver
```

Abra o navegador e acesse o seguinte endereço:

```bash
http://127.0.0.1:8000
```
