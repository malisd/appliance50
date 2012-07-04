# set umask
umask 0077

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
export LDLIBS="-lcs50 -lm"

# configure prompt
if [ "$PS1" ]; then
  export PS1="\u@\h (\w): "
fi
