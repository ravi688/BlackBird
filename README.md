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


## Frontend
```
cd blackbird/frontend/blackbird
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```
> [!NOTE]
> Make sure to run the following commands to build and perform lint checks for any type or semantic errors in your typescript code.
```
npm run build
npm run lint
```

## Docker
```
cd blackbird
docker compose up --build --force-recreate
```

## License
MIT
