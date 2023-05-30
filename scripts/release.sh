#!/bin/bash

set -e

NEXT_RELEASE=$1

if [ "${NEXT_RELEASE}" == "" ]; then
    echo Missing next release parameter
    exit 1
fi

pre-commit run --all-files
# ../netbox/venv/bin/pylint --rcfile=.pylintrc fwadmin

pip install twine -U

sed -i "s/0.0.1-dev1/${NEXT_RELEASE}/g" setup.py fwadmin/__init__.py
rm -rf dist

python3 setup.py sdist
# keyring --disable # Executed once
twine upload -u dainok dist/*
# git tag ${NEXT_RELEASE}
# git push
# git push origin --tags
