clear

echo "=== Default settings ==="
python3 pwgen.py
python3 pwgen.py
python3 pwgen.py
python3 pwgen.py
echo

echo "=== Length 79, alphanumeric, no 0Oo1Il ==="
python3 pwgen.py --length 79 --sets uld --uppercase ABCDEFGHJKLMNPQRSTUVWXYZ --lowercase abcdefghijkmnpqrstuvwxyz --digits 23456789
echo

echo "=== Length 79, all character sets ==="
python3 pwgen.py --length 79 --sets uldpn
echo

echo "=== Length 79, upper-case ASCII (defined as codepoints) ==="
python3 pwgen.py --length 79 --sets n --unicode 41-5a
echo

echo "=== All of these should cause an error ==="
python3 pwgen.py --length 0
python3 pwgen.py --sets ""
python3 pwgen.py --sets x
python3 pwgen.py --sets u --uppercase ""
python3 pwgen.py --sets n --unicode "110000-110000"
python3 pwgen.py --sets n --unicode ""
python3 pwgen.py --sets n --unicode ","
python3 pwgen.py --sets n --unicode "0--1"
python3 pwgen.py --sets n --unicode "41"
python3 pwgen.py --sets n --unicode "42-41"
python3 pwgen.py --sets n --unicode "41--42"
echo
