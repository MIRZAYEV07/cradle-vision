#! /usr/bin/env bash

# Exit in case of error
set -e

if [ ! -d ./cradle-vision ] ; then
    echo "Run this script from outside the project, to generate a sibling dev-fsfp project with independent git"
    exit 1
fi

rm -rf ./dev-fsfp

cookiecutter --no-input -f ./cradle-vision project_name="Dev FSFP"
