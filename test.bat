@echo off
cls

echo === test.bat: one password of length 8 ===
python pwgen.py 8
echo.

echo === test.bat: two alphanumeric passwords of length 12, no digits 0 or 1 ===
python pwgen.py --character-sets "uld" --digits "23456789" --count 2 12
echo.

echo === test.bat: two Unicode passwords of length 10 ===
python pwgen.py --character-sets "n" --count 2 10
echo.

echo === test.bat: all of these should cause an error ===
python pwgen.py
python pwgen.py --nonexistent 8
python pwgen.py 0
python pwgen.py --character-sets "" 8
python pwgen.py --character-sets "u" --uppercase "" 8
