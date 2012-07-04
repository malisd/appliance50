# configure prompt
if [ "$PS1" ]; then
  export PS1="\u@\h (\w): "
fi

# disable auto-logout
export TMOUT=0

# if not root
if [[ $UID -ne 0 ]]; then

  # set umask
  umask 0077

  # configure gcc
  export CC=gcc
  export CFLAGS="-ggdb -std=c99 -Wall -Werror"
  export LDLIBS="-lcs50 -lm"

  # protect user
  alias cp="cp -i"
  alias mv="mv -i"
  alias rm="rm -i"

  # allow core dumps
  ulimit -c unlimited

fi

# set editor
export EDITOR=nano

# set locale
export LANG=C
