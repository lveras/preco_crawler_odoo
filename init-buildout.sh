#!/usr/bin/env bash
set -e -x
echo "----> Instalando dependências"
sudo apt-get install python3 python-dev python3-dev postgresql
echo "----> Instalando dependências"
virtualenv -p python3 .
bin/pip install -U zc.buildout pip
echo "----> Executando buildout"
if bin/buildout; then
    echo "----> Instalado/Atualizado com sucesso!"
else
    echo "----> Erro encontrado"
    echo "----> Reinstalando setuptools"
    bin/pip uninstall setuptools -y && bin/pip install setuptools==41.0.1
fi

echo "----> Executando buildout"
bin/buildout
echo "----> Instalado/Atualizado com sucesso!"

echo "----> Iniciando ODOO"
echo "----> Para acessar: http://localhost:8069"
bin/start_odoo
