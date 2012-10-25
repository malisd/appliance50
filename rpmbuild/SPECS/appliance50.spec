###########################################################################
Summary: Configures the CS50 Appliance.
Name: appliance50
Version: 17
Release: 9
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Vendor: CS50
URL: https://manual.cs50.net/appliance50
BuildArch: i386
BuildRoot: %{_tmppath}/%{name}-root
Requires: system-release = 17
Requires: acpid
Requires: alsa-plugins-pulseaudio
Requires: at-spi2-atk
Requires: bc

# ar, strings
Requires: binutils

Requires: bind-utils
Requires: cgdb
Requires: check50
Requires: clang
Requires: coreutils 
Requires: cs50-2012-fall
Requires: ctags
Requires: dconf-editor

## @xfce-desktop
# Mandatory Packages
Requires: Thunar
Requires: desktop-backgrounds-compat
Requires: xfce-utils
Requires: xfce4-panel
Requires: xfce4-session
Requires: xfce4-settings
Requires: xfconf
Requires: xfdesktop
Requires: xfwm4
# Default Packages
#Requires: ConsoleKit
#Requires: NetworkManager-gnome
Requires: Terminal
#Requires: abrt-desktop
Requires: fedora-icon-theme
Requires: gdm
Requires: gtk-xfce-engine
#Requires: gvfs
#Requires: leafpad
#Requires: openssh-askpass
#Requires: orage
#Requires: polkit-gnome
#Requires: thunar-archive-plugin
#Requires: thunar-volman
#Requires: tumbler
Requires: xarchiver
Requires: xfce4-appfinder
Requires: xfce4-icon-theme
Requires: xfce4-mixer
#Requires: xfce4-power-manager
#Requires: xfce4-session-engines
Requires: xfwm4-theme-nodoka
#Requires: xscreensaver-base

# TODO: decide if can be removed from .ks
# (here so that can install with yum on an EC2 Fedora AMI)
Requires: dejavu-fonts-common
Requires: dejavu-sans-fonts
Requires: dejavu-sans-mono-fonts
Requires: dejavu-serif-fonts

Requires: diffutils
Requires: dkms
Requires: emacs
Requires: evince

# http://juraboy.wordpress.com/2011/07/26/installing-freenx-in-fedora-15/
Requires: freenx-server

Requires: garcon
Requires: glibc-debuginfo
Requires: gcc
Requires: gdb
Requires: gdm
Requires: gconf-editor
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
Requires: mlocate
Requires: mod_suphp
Requires: mysql
Requires: mysql-server
Requires: nano
Requires: nautilus-dropbox
Requires: ncftp

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

Requires: parole
Requires: parole-mozplugin
Requires: patch
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
Requires: style50
Requires: submit50
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
Requires: yum-utils

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
declare -a deprecated=(
 "/home/jharvard/Desktop/Trash.desktop"
)
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

# /etc/group
/usr/sbin/groupadd -r courses > /dev/null 2>&1
/usr/sbin/groupadd students > /dev/null 2>&1

# /etc/passwd
/usr/sbin/adduser --comment "John Harvard" --gid students --groups wheel jharvard > /dev/null 2>&1
/bin/echo crimson | /usr/bin/passwd --stdin jharvard > /dev/null 2>&1
echo "   Reset John Harvard's password to \"crimson\"."

# /home/jharvard/Dropbox
/bin/mkdir /home/jharvard/Dropbox > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/Dropbox > /dev/null 2>&1
/bin/chmod 0700 /home/jharvard/Dropbox > /dev/null 2>&1

# /var/lib/samba/private/passdb.tdb
/bin/echo -e "crimson\ncrimson" | /usr/bin/smbpasswd -a -s jharvard > /dev/null 2>&1
echo "   Reset John Harvard's password for Samba to \"crimson\"."

# ensure proper ownership
/bin/find /home/jharvard -path /home/jharvard/logs -prune -o -exec /bin/chown jharvard:students {} \; > /dev/null 2>&1
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
declare -a off=(avahi-daemon ip6tables mdmonitor saslauthd sendmail)
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
declare -a on=(iptables ntpd rsyslog smb sshd)
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
/usr/bin/mysql --force --user=root > /dev/null 2>&1 <<"EOF"
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

# /home/jharvard/logs
/bin/mkdir /home/jharvard/logs > /dev/null 2>&1
/bin/chown root:root /home/jharvard/logs > /dev/null 2>&1
/bin/chmod 0755 /home/jharvard/logs > /dev/null 2>&1

# /home/jharvard/logs/httpd
/bin/mkdir /home/jharvard/logs/httpd > /dev/null 2>&1
/bin/chown -R root:root /home/jharvard/logs/httpd > /dev/null 2>&1
/bin/chmod 0755 /home/jharvard/logs/httpd > /dev/null 2>&1
/bin/chmod 0644 /home/jharvard/logs/httpd/* > /dev/null 2>&1

# /home/jharvard/logs/mysqld
/bin/mkdir /home/jharvard/logs/mysqld > /dev/null 2>&1
/bin/chown mysql:mysql /home/jharvard/logs/mysqld > /dev/null 2>&1
/bin/chmod 0755 /home/jharvard/logs/mysqld > /dev/null 2>&1
/bin/touch /home/jharvard/logs/mysqld/{localhost.err,localhost.log,localhost-slow.log} > /dev/nul 2>&1
/bin/chown jharvard:mysql /home/jharvard/logs/mysqld/{localhost.err,localhost.log,localhost-slow.log} > /dev/nul 2>&1
/bin/chmod 0660 /home/jharvard/logs/mysqld/{localhost.err,localhost.log,localhost-slow.log} > /dev/nul 2>&1

# /home/jharvard/public_html
/bin/mkdir /home/jharvard/public_html > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/public_html > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/public_html > /dev/null 2>&1

# /home/jharvard/vhosts/localhost/html
/bin/mkdir -p /home/jharvard/vhosts/localhost/html > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/vhosts > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/vhosts > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/vhosts/localhost > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/vhosts/localhost > /dev/null 2>&1
/bin/chown jharvard:students /home/jharvard/vhosts/localhost/html > /dev/null 2>&1
/bin/chmod 0711 /home/jharvard/vhosts/localhost/html > /dev/null 2>&1

# /home/jharvard/.ssh
/bin/chmod 0600 /home/jharvard/.ssh/{authorized_keys,config,known_hosts} > /dev/null 2>&1

# /etc/sudoers.d/appliance50
/bin/chmod 0440 /etc/sudoers.d/appliance50 > /dev/null 2>&1

# /etc/ssh
/bin/chmod 0600 /etc/ssh/* > /dev/null 2>&1
/bin/chmod 0645 /etc/ssh/*.pub > /dev/null 2>&1

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

## install FreeNX
# rm avoids REMOTE HOST IDENTIFICATION HAS CHANGED
/bin/rm -f /root/.ssh/known_hosts > /dev/null 2>&1
/sbin/nxsetup --install --setup-nomachine-key > /dev/null 2>&1

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
