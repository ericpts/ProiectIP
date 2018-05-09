#!/bin/bash
#
# Install caffe for distro's which do not provide it.
#
# You should totally switch to Debian, but this script is provided for the more
# stubborn.

# Exit on first error.
set -e

CAFFE_REPO="https://github.com/BVLC/caffe"
# Pin the repo to a fixed repo, so that we do not encounted breaking changes.
CAFFE_COMMIT="864520713a4c5ffae7382ced5d34e4cadc608473"

function install_system_deps() {
    sudo apt update

    # General Dependencies
    sudo apt install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev protobuf-compiler
    sudo apt install -y --no-install-recommends libboost-all-dev libhdf5-serial-dev libhdf5-dev

    # BLAS -- for better CPU performance
    sudo apt install -y libatlas-base-dev libblas-dev libopenblas-dev

    # Python -- It comes preinstalled on Ubuntu 14.04
    # Required if you want to use Python wrappers for Caffe
    sudo apt install -y python-dev libpython2.7-dev python3.6-dev libpython3.6-dev


    # Remaining dependencies
    sudo apt install -y libgflags-dev libgoogle-glog-dev liblmdb-dev

    # Build essentials.
    sudo apt install build-essential cmake git pkg-config
}

# Because caffe by default does not build, we need to manually adjust the
# Makefile and Makefile.config files in order to fix them.
#
# This script should be run when the cwd is the caffe repo (i.e. caffe/).
function adjust_makefiles() {
    # Use CPU only.
    sed -i "/CPU_ONLY/s/^# //g" Makefile.config

    # Enable the python layer.
    sed -i "/WITH_PYTHON_LAYER/s/^# //g" Makefile.config

    # Enable python3.
    sed -i "/python3/s/^# //g" Makefile.config

    # Use python3.6, not 3.5.
    sed -i "s/python3.5/python3.6/g" Makefile.config

    # Use python3.6, not 3.5.
    sed -i "s/boost_python3/boost_python-py36/g" Makefile.config

    # Disable python2.
    sed -i "/python2/s/^/# /g" Makefile.config

    # Add /usr/include/hdf5/serial to INCLUDE_DIRS.
    sed -i "/INCLUDE_DIRS/s/$/ \/usr\/include\/hdf5\/serial/g" Makefile.config

    # Replace hdf5 with hdf5_serial in linked libraries.
    sed -i "s/hdf5/hdf5_serial/g" Makefile

    # Add opencv_imgproc as a library dep.
    # sed -i "/opencv_imgproc/s/$/ opencv_imgcodecs/g" Makefile
}

function build_caffe() {
    echo "Building caffe..."
    if [ ! -e "caffe" ]; then
        git clone "$CAFFE_REPO" caffe
    fi
    pushd caffe

    git reset --hard 864520713a4c5ffae7382ced5d34e4cadc608473
    git clean -f -

    sudo pip3 install -r python/requirements.txt

    cp Makefile.config.example Makefile.config
    adjust_makefiles

    # Finally, build the library with all processors.
    # The computer will have all its resources hogged during this process.
    make all -j$(nproc)

    # Also build the python extensions.
    make pycaffe -j$(nproc)

    make distribute -j$(nproc)

    popd
}

function install_caffe() {
    echo "Installing caffe..."

    pushd caffe

    # Since no install target is provided, we have to copy the files manually.
    sudo cp -r distribute/python/caffe/ /usr/local/lib/python3.6/dist-packages/
    sudo cp build/lib/libcaffe.so* /usr/lib

    popd
}

pushd extern

install_system_deps
build_caffe
install_caffe

popd
