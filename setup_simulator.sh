#!/bin/bash

set -e

# Path definitions for ETSS-Perf-Sim (EPS)
EPS_WORKSPACE=$(realpath $(dirname "${0}"))
EPS_ETISS=${EPS_WORKSPACE}/etiss
EPS_ETISS_BUILD=${EPS_ETISS}/build_dir
export EPS_ETISS_INSTALLED=${EPS_ETISS_BUILD}/installed # exported as needed by CMake for simulator build
EPS_ETISS_HOTFIX=${EPS_WORKSPACE}/etiss_hotfix
EPS_ETISS_PLUGINS=${EPS_WORKSPACE}/etiss_plugins
EPS_SIM=${EPS_WORKSPACE}/simulator

# Setup ETISS
echo ""
echo "*** Installing ETISS ***"

cd ${EPS_ETISS}/PluginImpl
if [ ! -L SoftwareEvalLib ]; then
    echo " > Linking SoftwareEval Library to ETISS"
    ln -s ${EPS_ETISS_PLUGINS}/SoftwareEvalLib SoftwareEvalLib
fi

echo " > Applying hot-fixes to ETISS"
cp ${EPS_ETISS_HOTFIX}/include/etiss/* ${EPS_ETISS}/include/etiss
cp ${EPS_ETISS_HOTFIX}/src/* ${EPS_ETISS}/src

echo " > Installing..."
mkdir -p ${EPS_ETISS_BUILD}
cd ${EPS_ETISS_BUILD}
cmake -DCMAKE_BUILD_TYPE=Release -DETISS_BUILD_MANUAL_DOC=ON -DCMAKE_INSTALL_PREFIX:PATH=${EPS_ETISS_INSTALLED} ..
make -j$(nproc) install


# Setup simulator
echo ""
echo "*** Installing simulator ***"
cd ${EPS_SIM}
mkdir -p build
cd build
cmake -DETISS_DIR=${EPS_ETISS_INSTALLED}/lib/CMake/ETISS ..
make -j $(nproc)
