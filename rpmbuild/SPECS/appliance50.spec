###########################################################################
Summary: Configures the CS50 Appliance.
Name: appliance50
Version: 17
Release: 0
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Vendor: CS50
URL: https://manual.cs50.net/appliance50
BuildArch: i386
BuildRoot: %{_tmppath}/%{name}-root
Requires: generic-release = 17
Requires: acpid
Requires: alsa-plugins-pulseaudio
Requires: at-spi2-atk
Requires: bc

# gcov, gprof (for Problem Set 6)
Requires: binutils

Requires: bind-utils

# TODO
#Requires: check50

Requires: clang
Requires: coreutils 

# TODO
#Requires: cs50-2012-fall

Requires: ctags
Requires: dconf-editor
Requires: diffutils
Requires: dkms
Requires: emacs
Requires: evince
Requires: garcon
Requires: glibc-debuginfo
Requires: gcc
Requires: gdb
Requires: gdm
Requires: gconf-editor
Requires: geany
Requires: geany-plugins-debugger
Requires: geany-plugins-geanyvc
Requires: geany-plugins-shiftcolumn
Requires: geany-plugins-webhelper
Requires: gedit
Requires: gedit-plugins
Requires: git
Requires: glib2
Requires: gnome-icon-theme-extras
Requires: gnome-icon-theme-legacy
Requires: gnome-icon-theme-symbolic
Requires: gnome-menus
Requires: gnome-packagekit
Requires: google-chrome-stable
Requires: httpd
Requires: icedtea-web
Requires: indent
Requires: iptables
Requires: java
Requires: java-devel
Requires: kernel
Requires: kernel-devel
Requires: kernel-headers
Requires: library50-c
Requires: library50-php
Requires: lynx
Requires: make
Requires: man
Requires: man-pages
Requires: mercurial
Requires: mlocate
Requires: mod_suphp
Requires: mysql
Requires: mysql-server
Requires: nano
Requires: nautilus-dropbox
Requires: ncftp

# -lncurses
Requires: ncurses
Requires: ncurses-debuginfo
Requires: ncurses-devel

# http://nodejs.tchol.org/
Requires: nodejs-stable-release
Requires: nodejs
Requires: npm

# -lcrypt
Requires: nss-softokn-debuginfo

Requires: ntp
Requires: orca
Requires: openssh-clients
Requires: openssh-server

# broken in F15
# TODO: check if broken in F16
# http://comments.gmane.org/gmane.linux.redhat.fedora.xfce/311
# http://comments.gmane.org/gmane.linux.redhat.fedora.general/397725
Requires: PackageKit-yum-plugin

Requires: parole
Requires: parole-mozplugin
Requires: patch

# workaround for Fedora 16's lack of php-zip
# https://bugzilla.redhat.com/show_bug.cgi?id=551513
#Requires: pcre-devel

Requires: php
Requires: php-devel
Requires: php-mysql
Requires: php-pear
Requires: php-pecl-xdebug
Requires: php-PHPMailer
Requires: php-phpunit-DbUnit
Requires: php-phpunit-PHPUnit
Requires: php-tidy
Requires: php-xml
Requires: phpMyAdmin
Requires: pulseaudio
Requires: python
Requires: pyxdg
Requires: render50
Requires: ristretto
Requires: rpm 
Requires: rsnapshot
Requires: rsync
Requires: ruby
Requires: rubygems
Requires: samba
Requires: screen
Requires: sed
Requires: setup
Requires: shadow-utils

# TODO
#Requires: submit50

Requires: sudo
Requires: system-config-firewall
Requires: system-config-keyboard
Requires: system-config-language
Requires: system-config-network
Requires: system-config-services
Requires: teamviewer7
Requires: telnet
Requires: tidy
Requires: traceroute
Requires: tree

# TODO
#Requires: tunnel50

Requires: valgrind
Requires: vim
Requires: vim-X11
Requires: wget
Requires: words
Requires: xfce4-panel
Requires: xfce4-genmon-plugin
Requires: xfce4-screenshooter
Requires: xfce4-screenshooter-plugin
Requires: xorg-x11-fonts-misc
Requires: xterm
Requires: yum-plugin-fastestmirror
Requires: yum-plugin-priorities
Requires: yum-plugin-protectbase
Requires: yum-updatesd
Requires: yum-utils

# workaround for Fedora 16's lack of php-zip
# https://bugzilla.redhat.com/show_bug.cgi?id=551513
Requires: zlib-devel

Requires(post): coreutils 
Requires(post): glib2
Requires(post): mlocate
Requires(post): mysql
Requires(post): mysql-server
Requires(post): php-pear
Requires(post): rpm 
Requires(post): rsync
Requires(post): sed
Requires(post): shadow-utils
Requires(post): yum-utils


############################################################################
%description
The CS50 Appliance is a virtual machine that lets you
take CS50, even if you're not a student at Harvard.


############################################################################
%prep
/bin/rm -rf %{_builddir}/%{name}
/bin/cp -a %{_sourcedir}/%{name} %{_builddir}/


############################################################################
%install
/bin/rm -rf %{buildroot}
/bin/mkdir -p %{buildroot}/tmp/
/bin/cp -a %{_builddir}/%{name} %{buildroot}/tmp/


############################################################################
%clean
/bin/rm -rf %{buildroot}


############################################################################
%post

# prepare to update desktop
# http://forum.xfce.org/viewtopic.php?id=5775
/usr/bin/killall xfconfd > /dev/null 2>&1

# /tmp/%{name}-%{version}-%{release}
declare tmp=/tmp/%{name}

# remove deprecated directories and files
declare -a deprecated=()
for dst in "${deprecated[@]}"
do
    if [ -e $dst.lock ]
    then
        echo "   Did not remove $dst because of lockfile."
    else
        /bin/rm -rf $dst
        echo "   Removed $dst."
    fi
done

# install directories
for src in $(/bin/find $tmp -mindepth 1 -type d | /bin/sort)
do
    declare dst=${src#$tmp}
    declare dir=$(/usr/bin/dirname $dst)
    declare base=$(/bin/basename $dst)
    if [ -e $dir/$base.lock ] || [ -e $dir/.$base.lock ]
    then
        echo "   Did not install $dst because of lockfile."
    else
        /usr/bin/rsync --devices --dirs --links --perms --quiet --specials --times $src $dir > /dev/null 2>&1
        echo "   Installed $dst."
    fi
done

# install files
for src in $(/bin/find $tmp ! -type d | /bin/sort)
do
    declare dst=${src#$tmp}
    declare dir=$(/usr/bin/dirname $dst)
    declare base=$(/bin/basename $dst)
    if [ -e $dir/$base.lock ] || [ -e $dir/.$base.lock ]
    then
        echo "   Did not install $dst because of lockfile."
    else
        if [ -e $dst ] && ! /usr/bin/cmp -s $src $dst
        then
            /bin/mv $dst $dst.rpmsave
        fi
        /usr/bin/rsync --devices --links --perms --quiet --specials --times $src $dst > /dev/null 2>&1
        echo "   Installed $dst."
    fi
done

# /boot/grub2/grub.cfg
#/bin/sed -i -e 's/^GRUB_TIMEOUT=.*$/GRUB_TIMEOUT=2/' /etc/default/grub
#/sbin/grub2-mkconfig -o /boot/grub2/grub.cfg > /dev/null 2>&1

# /etc/group
/usr/sbin/groupadd -r courses > /dev/null 2>&1
/usr/sbin/groupadd students > /dev/null 2>&1

# /etc/passwd
/usr/sbin/adduser --comment "John Harvard" --gid students --groups wheel jharvard > /dev/null 2>&1
/bin/echo crimson | /usr/bin/passwd --stdin jharvard > /dev/null 2>&1
echo "   Reset John Harvard's password to \"crimson\"."

# /var/lib/samba/private/passdb.tdb
/bin/echo -e "crimson\ncrimson" | /usr/bin/smbpasswd -a -s jharvard > /dev/null 2>&1
echo "   Reset John Harvard's password for Samba to \"crimson\"."

# ensure proper ownership
/bin/find /home/jharvard -path /home/jharvard/logs -prune -o -exec /bin/chown jharvard:students {} \;
echo "   Updated ownership of John Harvard's home directory."

# might be causing new panel to be created during reinstall
#/usr/bin/xfce4-panel > /dev/null 2>&1

# lock root
/usr/bin/passwd -l root > /dev/null 2>&1
echo "   Locked superuser's account."

# disable services
declare -a off=(netconsole)
for service in "${off[@]}"
do
    /sbin/chkconfig $service off > /dev/null 2>&1
    echo "   Disabled $service."
done
declare -a off=(avahi-daemon ip6tables mdmonitor saslauthd)
for service in "${off[@]}"
do
    /bin/systemctl disable $service.service > /dev/null 2>&1
    echo "   Disabled $service."
done

# enable services
declare -a on=(dkms_autoinstaller network)
for service in "${on[@]}"
do
    /sbin/chkconfig $service on > /dev/null 2>&1
    echo "   Enabled $service."
done
declare -a on=(httpd iptables mysqld ntpd rsyslog smb sshd yum-updatesd)
for service in "${on[@]}"
do
    /bin/systemctl enable $service.service > /dev/null 2>&1
    echo "   Enabled $service."
done

# reset MySQL privileges
/bin/systemctl stop mysqld.service > /dev/null 2>&1
/bin/mv /etc/my.cnf /etc/.my.cnf
/bin/cp -a /etc/.my.cnf /etc/my.cnf
/bin/cat > /etc/my.cnf <<"EOF"
[mysqld]
datadir=/var/lib/mysql
skip-grant-tables
skip-networking
socket=/var/lib/mysql/mysql.sock
user=mysql
EOF
/bin/systemctl start mysqld.service > /dev/null 2>&1
/usr/bin/mysql --user=root > /dev/null 2>&1 <<"EOF"
DELETE FROM mysql.user WHERE User = '';
DELETE FROM mysql.user WHERE User = 'root';
DELETE FROM mysql.user WHERE User = 'jharvard';
INSERT INTO mysql.user (Host, User, Password, Grant_priv, Super_priv) VALUES('localhost', 'jharvard', PASSWORD('crimson'), 'Y', 'Y');
FLUSH PRIVILEGES;
GRANT ALL ON *.* TO 'jharvard'@'localhost';
EOF
/bin/systemctl stop mysqld.service > /dev/null 2>&1
/bin/mv /etc/.my.cnf /etc/my.cnf
/bin/systemctl start mysqld.service > /dev/null 2>&1
echo "   Reset John Harvard's password for MySQL to \"crimson\"."

# ensure /home/jharvard/logs exists
/bin/mkdir /home/jharvard/logs > /dev/null 2>&1
/bin/chown -R root:root /home/jharvard/logs > /dev/null 2>&1
/bin/chmod 0755 /home/jharvard/logs > /dev/null 2>&1
/bin/chmod 0644 /home/jharvard/logs/* > /dev/null 2>&1

# ensure /home/jharvard/public_html exists
/bin/mkdir /home/jharvard/public_html > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/public_html > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/public_html > /dev/null 2>&1

# ensure /home/jharvard/vhosts/localhost/html exists
/bin/mkdir -p /home/jharvard/vhosts/localhost/html > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/vhosts > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/vhosts > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/vhosts/localhost > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/vhosts/localhost > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/vhosts/localhost/html > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/vhosts/localhost/html > /dev/null 2>&1

# /etc/sudoers.d/appliance50
/bin/chmod 0440 /etc/sudoers.d/appliance50

# /etc/ssh
/bin/chmod 0600 /etc/ssh/*
/bin/chmod 0645 /etc/ssh/*.pub

# restart services
declare -a restart=(httpd iptables network smb sshd)
for service in "${restart[@]}"
do
    /bin/systemctl reload-or-try-restart $service.service > /dev/null 2>&1
    echo "   Restarted $service."
done

# recompile schemas
# https://github.com/Quixotix/gedit-source-code-browser
#/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
#/bin/chmod -R a+rX /usr/share/glib-2.0/schemas/
#echo "   Recompiled schemas."

# rebuild icon cache
#/usr/bin/gtk-update-icon-cache /usr/share/icons/hicolor/ > /dev/null 2>&1
#echo "   Rebuilt icon cache."

# redraw panel
/bin/find /home/jharvard/.config/xfce4/panel -type f -exec /bin/touch {} \;
echo "   Updated John Harvard's panel."

# redraw desktop
#/usr/bin/xfdesktop --reload > /dev/null 2>&1
#echo "   Updated John Harvard's and superuser's desktops."

## import keys (to avoid warnings during future software updates)
# http://linux.dropbox.com/fedora/rpm-public-key.asc
/bin/rpm --import /etc/pki/rpm-gpg/rpm-public-key.asc
# https://dl-ssl.google.com/linux/linux_signing_key.pub
/bin/rpm --import /etc/pki/rpm-gpg/linux_signing_key.pub
/bin/rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-i386

# remove sources
/bin/rm -rf /tmp/%{name}

# rebuild mlocate.db
/etc/cron.daily/mlocate.cron

# return 0
/bin/true


##########################################################################
%files
%defattr(-,root,root,-)
/tmp/%{name}

# TODO: fix?
#%defattr(-,root,students,1770)
#/opt/%{name}/usr/local/samba/lib/usershares


##########################################################################
%changelog
* Wed Jan 4 2012 David J. Malan <malan@harvard.edu> - 3-1
- Initial build
