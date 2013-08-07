if [[ $(echo $0 | awk '/^\//') == $0 ]]; then
    ABSPATH=$(dirname $0)
else
    ABSPATH=$PWD/$(dirname $0)
cd ABSPATH
clear
python Fur.py