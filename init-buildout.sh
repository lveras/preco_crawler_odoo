#!/usr/bin/env bash
set -e -x
echo "----> Instalando dependências"
sudo apt-get -y install python3 python3-dev python3-pip mercurial python3-psycopg2 libpq-dev build-essential autoconf libtool pkg-config python3-opengl python-imaging python-pyrex python-pyside.qtopengl qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 libssl-dev libsasl2-dev libldap2-dev
echo "----> Instalando dependências"
sudo pip3 install virtualenv
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
