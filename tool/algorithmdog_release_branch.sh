#!/bin/python
git checkout release
rm -rf roomai/doudizhupoker
rm tests/testDouDiZhuPoker*.py
python -m unittest discover -s tests
