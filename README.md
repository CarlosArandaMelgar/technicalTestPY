TechnicalTest/
├── env/                 
├── src/
│   ├── ETL.py           # Script de procesamiento ETL
│   ├── backend.py       # Backend FastAPI
├── utils/               # CSV
├── sales_dashboard.db   # BD
├── requirements.txt     # Dependencias
├── .gitignore          


# Comandos para inicializar proyecto:

    1- python -m venv env
    2- .\env\Scripts\activate
    3- pip install -r requirements.txt

# Comandos para correr proyecto:

    4- py .\src\ETL.py
    5- uvicorn src.backend:app --reload


Opcional Windows CMD Command Policy: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass



    