#!/bin/bash

function format() {
    # Format all .py files which are not part of migrations.
    python3 -m yapf \
        --recursive \
        --in-place \
        --parallel \
        --verbose \
        --style pep8 \
        $(find colorzr -type f -name "*.py" | grep -v "migrations")
}

format
