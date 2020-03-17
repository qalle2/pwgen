@echo off
cls

echo === test.bat: default settings ===
python pwgen.py
python pwgen.py
python pwgen.py
python pwgen.py
echo.

echo === test.bat: length 40; alphanumeric; no 0Oo1Il ===
python pwgen.py --length 40 --sets uld --uppercase ABCDEFGHJKLMNPQRSTUVWXYZ --lowercase abcdefghijkmnpqrstuvwxyz --digits 23456789
echo.

echo === test.bat: length 40; all character sets ===
python pwgen.py --length 40 --sets uldpn
echo.

echo === test.bat: length 40; uppercase as Unicode ===
python pwgen.py --length 40 --sets n --unicode 41-5a
echo.

echo === test.bat: all of these should cause an error ===
python pwgen.py --length 0
python pwgen.py --sets ""
python pwgen.py --sets x
python pwgen.py --sets u --uppercase ""
python pwgen.py --sets n --unicode ""
python pwgen.py --sets n --unicode ","
python pwgen.py --sets n --unicode 110000
python pwgen.py --sets n --unicode "0--1"
python pwgen.py --sets n --unicode 42-41
echo.

echo === test.bat: help ===
python pwgen.py --help
