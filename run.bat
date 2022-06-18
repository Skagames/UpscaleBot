Rem set the path to the correct location of the bat file
REM set path=%~dp0

Rem Activate the correct environment
call %path%/venv/Scripts/activate

Rem go back to the correct location of the bat file
cd %path%

Rem Run the program
python main.py