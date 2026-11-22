# BlackBird
Over the air update infrastructure software

## Backend
```
cd blackbird/backend
python3 -m venv .python_env
source .python_env/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
You will have swag ui available at `http://localhost:8000/docs'`
