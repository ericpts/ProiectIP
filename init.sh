#!/bin/bash

function init_colorization() {
    pushd extern/colorization
    bash ./models/fetch_release_models.sh
    popd

    pushd extern
    patch -p1 < caffe_use_cpu.patch
    popd
}

function init_python_requirements() {
    sudo pip3 install -r requirements.txt
}

function init_cifar() {
    pushd extern/cifar
    python3 -c 'import cifar10; cifar10.maybe_download_and_extract()'
    popd
}

function init_coconuts() {
    mkdir -p colorzr/files/coconuts/data
    mkdir -p colorzr/files/coconuts/cache
}


# init_colorization
init_python_requirements
init_cifar
init_coconuts
