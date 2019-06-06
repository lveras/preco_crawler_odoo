# eSCE

## Instalação
###Passos para instalação do PostGresSQL

1º Instalando o Banco de Dados

    apt-get install postgresql
    service postgresql status
    chown postgres /var/log/postgresql

2º Criando usuario

    sudo su - postgres -c "psql postgres -c \
    \"CREATE USER odoo SUPERUSER INHERIT CREATEDB CREATEROLE; \
    ALTER USER odoo PASSWORD 'odoo';\""


###Passos para instalação do Odoo V12

1º Criar uma pasta vazia com permissão de escrita.

    mkdir sce

2º Configurar um Virtual Env na pasta criada, 
com permissão de acesso às bibliotecas do sistema:
	
	cd sce

3º Clonar repositório do github: 	

	git clone git@gitlab.abgf.gov.br:e-sce/odoo12.git .

4º Executando script de Instalação/Atualização

	./init-buildout.sh
 
5º Enjoy!
 
 Mais informações veja a documentação oficial: https://github.com/anybox/anybox.recipe.odoo/
