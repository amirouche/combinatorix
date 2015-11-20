check:
	nose2 -C --coverage combinatorix.py --coverage-report html

doc:
	pandoc README.md -t rst > README.rst
