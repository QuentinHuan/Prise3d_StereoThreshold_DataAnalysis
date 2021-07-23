echo "requires Python3"
python --version

echo "script will install: numpy, matplotlib, scipy, pillow (using pip)"
read "continue ?"
pip install numpy
pip install matplotlib
pip install scipy
pip install pillow

echo "done"