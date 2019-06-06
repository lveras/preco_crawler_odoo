# odoo-brazil-buildout


Passos para instalação do PostGresSQL

1º Instalando o Banco de Dados
	apt-get install postgresql
	service postgresql status
	chown postgres /var/log/postgresql
	sudo -i -u postgres

2º Criando usuario
	CREATE USER odoo SUPERUSER INHERIT CREATEDB CREATEROLE;
	ALTER USER odoo PASSWORD 'odoo'; 


Passos para instalação do Odoo V12


1º Criar uma pasta vazia com permissão de escrita.

	mkdir sce

2º Configurar um Virtual Env na pasta criada, 
com permissão de acesso às bibliotecas do sistema:
	
	cd sce

3º Clonar repositório do github: 	

	git clone git@gitlab.abgf.gov.br:e-sce/odoo12.git .

4º Inatalar dependencias 

	sudo apt-get install python3 python-dev python3-dev git mercurial virtualenv 
	sudo apt-get install libsasl2-dev libldap2-dev libssl-dev
	virtualenv -p python3 .

5º Atualizar e/ou Instalar o buildout dentro da virtualenv

	bin/pip install -U pip zc.buildout 
	bin/pip install babel chardet

5º Execute o buildout, para fazer o download do Odoo e suas dependencias

	bin/buildout 

6º Iniciando o Odoo
	
	bin/start_odoo
 
 7º Enjoy!
 
 Mais informações veja a documentação oficial: https://github.com/anybox/anybox.recipe.odoo/
