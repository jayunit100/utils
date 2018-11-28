## Manage python

echo "# Usage : eval $(./pyme.sh 3.3.0)"

function install_pyenv {
    echo "# Pyme ~ Installing pyenv ..."
    if which curl | grep -q curl ; then 
        if which pyenv | grep -q pyenv ; then
            echo "# Pyenv found !"
        else
            echo "# Bootstrapping..."
            curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
        fi
    fi
}

function install_python {
    echo "# Pyme ~ Installing python $1..."
    if pyenv versions | grep -q $1 ; then
        echo "# Version exists already"        
    else
        pyenv install $1
    fi
    theEnv=`pyenv which python | grep $1`
    echo "# Pyme ~ Python lives at : $theEnv"
    export PATHZ="$PATH:`dirname $theEnv`";
    echo "#"
    echo "#"
    echo "export PATH=$PATHZ"
    echo "# To export this automatically, next time, run"
    echo "# eval "$(./pyme.sh $1)""

}

install_pyenv
install_python $1
