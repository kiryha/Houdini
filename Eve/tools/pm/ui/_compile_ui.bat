set UIFILE=%1
set UIDIR=%~dp$PATH:1
set FILENAME=%~n1
set SNAME=%UIDIR%%FILENAME%.py

CALL C:\Users\kko8\AppData\Local\Programs\Python\Python311\Scripts\pyside6-uic.exe %UIFILE% -o %SNAME%
