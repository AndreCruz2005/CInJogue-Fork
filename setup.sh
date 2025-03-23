echo "Iniciando setup do Backend..."
cd backend || exit

echo "Criando ambiente virtual..."
python -m venv .venv
source .venv/Scripts/activate 

echo "Instalando dependências do backend..."
pip install -r requirements.txt

echo "Iniciando servidor Flask..."
nohup python flaskr/app.py &  

cd ..

echo "Iniciando setup do Frontend..."
cd frontendJS || exit

echo "Instalando dependências do frontend..."
npm install

echo "Iniciando servidor de desenvolvimento..."
nohup npm run dev &

echo "Setup concluído! Acesse o frontend em http://localhost:8000/"