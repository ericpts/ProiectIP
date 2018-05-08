#!/bin/sh
# Install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install the experimental NVIDIA Mac drivers
#   Download from http://www.nvidia.com/download/driverResults.aspx/103826/en-us
# Install cuDNN v5 for 8.0 RC or use the latest when it's available
#   Register and download from https://developer.nvidia.com/rdp/cudnn-download 
#   or this path: https://developer.nvidia.com/rdp/assets/cudnn-8.0-osx-x64-v5.0-ga-tgz
#   extract to the NVIDIA CUDA folder and perform necessary linking
#   into your /usr/local/cuda/lib and /usr/local/cuda/include folders
#   You will need to use sudo because the CUDA folder is owned by root
#   Now Caffe support Cudnn v6
sudo tar -xvf ~/Downloads/cudnn-8.0-osx-x64-v6.0.tar /Developer/NVIDIA/CUDA-8.0/
sudo ln -s /Developer/NVIDIA/CUDA-8.0/lib/libcudnn.dylib /usr/local/cuda/lib/libcudnn.dylib
sudo ln -s /Developer/NVIDIA/CUDA-8.0/lib/libcudnn.5.dylib /usr/local/cuda/lib/libcudnn.5.dylib
sudo ln -s /Developer/NVIDIA/CUDA-8.0/lib/libcudnn_static.a /usr/local/cuda/lib/libcudnn_static.a
sudo ln -s /Developer/NVIDIA/CUDA-8.0/include/cudnn.h /usr/local/cuda/include/cudnn.h

# Install the brew dependencies
#   Do not install python through brew. Only misery lies there
#   We'll use the versions repository to get the right version of boost and boost-python
#   We'll also explicitly upgrade libpng because it's out of date
#   Do not install numpy via brew. Your system python already has it.

brew install -vd snappy leveldb gflags glog szip lmdb
brew tap homebrew/science
brew install hdf5 opencv
brew upgrade libpng
brew tap homebrew/versions

brew install --build-from-source --with-python -vd protobuf
brew install --build-from-source -vd boost boost-python

# Clone the caffe repo
cd ~/Documents
git clone https://github.com/BVLC/caffe.git
# Setup Makefile.config
#   You can download mine directly from here, but I'll explain all the selections
#     For XCode 8.0 and later (Sierra):
#       https://gist.github.com/rizkyario/5c0f7435ce7d3bcd3e236cca99042587
#   First, we'll enable only CPU
#     CPU_ONLY := 1
#   In order to use the built-in Accelerate.framework, you have to reference it.
#   Astonishingly, nobody has written this anywhere on the internet.
#     BLAS := atlas
#     If you use El Capitan (10.11), we'll use the 10.11 sdk path for vecLib:
#       BLAS_INCLUDE := /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers
#     Otherwise (10.12), let's use the 10.12 sdk path:
#       BLAS_INCLUDE := /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.12.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers
#     BLAS_LIB := /System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A
#   Configure to use system python and system numpy
#     PYTHON_INCLUDE := /System/Library/Frameworks/Python.framework/Headers \
#          /System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/core/include
#     PYTHON_LIB := /System/Library/Frameworks/Python.framework/Versions/2.7/lib
#   Configure to enable Python layers. Some projects online need this
#     WITH_PYTHON_LAYER := 1

curl https://gist.githubusercontent.com/rizkyario/5c0f7435ce7d3bcd3e236cca99042587/raw/122cf8558f1497c50fd8febdbfe697746dc30a13/Makefile.config -o Makefile.config

# Add opencv_imgcodecs to Makefile
# LIBRARIES += glog gflags protobuf boost_system boost_filesystem m hdf5_hl hdf5 opencv_imgcodecs

# Go ahead and build.
make all
make test
make runtest

# To get python going, first we need the dependencies
#   On a super-clean Mac install, you'll need to easy_install pip.
sudo -H easy_install pip
#   Now, we'll install the requirements system-wide. You may also muck about with a virtualenv.
#   Astonishingly, --user is not better known. 
pip install --user -r python/requirements.txt
#   Go ahead and run pytest now. Horrible @rpath warnings which can be ignored.

# Fix Malloc error. This is a leveldb issue
brew install https://gist.githubusercontent.com/rizkyario/5bcaa5c1b7a1d06e7e1a6c1193ff54af/raw/c0a06f1b98388333955f49e30e01dfdde2d82526/leveldb.rb

#make sure latest version of numpy is installed
sudo easy_install -U numpy

make -j8 pytest
# Now, install the package
#   Make the distribution folder
make distribute
#   Install the caffe package into your local site-packages
cp -r distribute/python/caffe ~/Library/Python/2.7/lib/python/site-packages/
#   Finally, we have to update references to where the libcaffe libraries are located.
#   You can see how the paths to libraries are referenced relatively
#     otool -L ~/Library/Python/2.7/lib/python/site-packages/caffe/_caffe.so
#   Generally, on a System Integrity Protection -enabled (SIP-enabled) Mac this is no good.
#   So we're just going to change the paths to be direct
cp distribute/lib/libcaffe.so.1.0.0-rc3 ~/Library/Python/2.7/lib/python/site-packages/caffe/libcaffe.so.1.0.0-rc3
install_name_tool -change @rpath/libcaffe.so.1.0.0-rc3 ~/Library/Python/2.7/lib/python/site-packages/caffe/libcaffe.so.1.0.0-rc3 ~/Library/Python/2.7/lib/python/site-packages/caffe/_caffe.so
# Verify that everything works
#   start python and try to import caffe
python -c 'import caffe'
# If you got this far without errors, congratulations, you installed Caffe on a modern Mac OS X 