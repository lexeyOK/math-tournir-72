git clone https://github.com/diduk001/math-tournir-72.git
cd math-tournir-72/

python3 --version
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv -a $(pwd) -r requirements.txt math-tournir-72

pip install -r  requirements.txt

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

flask run

deactivate
lsvirtualenv
workon math-tournir-72
