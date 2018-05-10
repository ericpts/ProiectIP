#!/bin/bash

function clear_db() {
    pushd colorzr
    
    python3 manage.py delete_all_users

    popd
}

clear_db