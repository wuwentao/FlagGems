set -e
clear
sh ~/clear-triton-cache.sh
export FLAGTREE_AABS=1
export TRITON_PRINT_AUTOTUNING=1
python3 -m pytest -s test_mm.py -m mm1 --quick --ref=cpu -x  #--log-cli-level=debug
