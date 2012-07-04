# are we in an interactive shell?
if [ "$PS1" ]; then

  # set umask
  umask 0077

  # configure prompt
  export PS1="\u@\h (\w): "

  # protect user
  alias cp="cp -i"
  alias mv="mv -i"
  alias rm="rm -i"

  # allow core dumps
  ulimit -c unlimited

  # disable auto-logout
  export TMOUT=0

  # set locale
  export LANG=C

  # set editor
  export EDITOR=nano

  # gcc
  export CC=gcc
  export CFLAGS="-ggdb -std=c99 -Wall -Werror -Wformat=0"
  export LDLIBS="-lcs50 -lgc -lm"

fi
