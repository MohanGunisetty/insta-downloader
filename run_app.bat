
@echo off
echo Starting Instagram Downloader...

cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Starting Server...
echo Open http://localhost:8000 in your browser
python app/main.py
