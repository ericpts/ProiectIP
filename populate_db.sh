#!/bin/bash

function populate_db() {
    pushd colorzr
    
    python3 manage.py populate_db_with_users 10
    python3 manage.py populate_db_with_profiles
    python3 manage.py populate_db_with_image_uploads 5
    python3 manage.py populate_db_with_comments 100
    python3 manage.py populate_db_with_ratings 50

    popd 
}

populate_db