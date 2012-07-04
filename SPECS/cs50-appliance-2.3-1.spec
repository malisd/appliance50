###########################################################################
Summary: Configures the CS50 Appliance.
Name: cs50-appliance
Version: 2.3
Release: 1
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Vendor: CS50
URL: https://manual.cs50.net/Appliance
BuildArch: i386
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: generic-release = 15
Requires: acpid
Requires: adobe-release
Requires: alsa-plugins-pulseaudio
Requires: bind-utils
Requires: coreutils 
Requires: cs50-eclipse
Requires: cs50-library-c
Requires: cs50-library-php
Requires: ctags
Requires: dconf-editor
Requires: diffutils
Requires: dkms
Requires: emacs
Requires: firefox
Requires: firstboot
Requires: flash-plugin
Requires: ftp
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
Requires: httpd
Requires: icedtea-web
Requires: indent
Requires: iptables
Requires: java >= 1.6.0
Requires: kernel-devel
Requires: kernel-headers
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
Requires: ncurses
Requires: ncurses-devel
Requires: nfs-utils
Requires: ntp
Requires: openssh-clients
Requires: openssh-server

# broken in F15
# http://comments.gmane.org/gmane.linux.redhat.fedora.xfce/311
# http://comments.gmane.org/gmane.linux.redhat.fedora.general/397725
Requires: PackageKit-yum-plugin

Requires: parole
Requires: parole-mozplugin
Requires: patch
Requires: php
Requires: php-mysql
Requires: php-pecl-xdebug
Requires: php-PHPMailer
Requires: php-xml
Requires: phpMyAdmin
Requires: proftpd
Requires: pulseaudio
Requires: python
Requires: RBTools
Requires: render50
Requires: ristretto
Requires: rpm 
Requires: rsnapshot
Requires: rsync
Requires: ruby
Requires: rubygems
Requires: samba
Requires: scratch
Requires: screen
Requires: sed
Requires: setup
Requires: shadow-utils
Requires: submit50
Requires: sudo
Requires: system-config-firewall
Requires: system-config-keyboard
Requires: system-config-language
Requires: system-config-network
Requires: system-config-services
Requires: teamviewer6
Requires: telnet
Requires: tidy
Requires: traceroute
Requires: usermin
Requires: valgrind
Requires: vim
Requires: vim-X11
Requires: webmin
Requires: wget
Requires: xfce4-panel
Requires: xfce4-screenshooter
Requires: xorg-x11-fonts-misc
Requires: xterm
Requires: yum-plugin-fastestmirror
Requires: yum-plugin-priorities
Requires: yum-plugin-protectbase
Requires: yum-updatesd
Requires: yum-utils

Requires(post): coreutils 
Requires(post): glib2
Requires(post): mlocate
Requires(post): mysql
Requires(post): mysql-server
Requires(post): rpm 
Requires(post): rsync
Requires(post): scratch
Requires(post): sed
Requires(post): shadow-utils
Requires(post): yum-utils


############################################################################
%description
The CS50 Appliance is a virtual machine that lets you
take CS50, even if you're not a student at Harvard.


############################################################################
%prep
/bin/rm -rf %{_builddir}/%{name}-%{version}-%{release}/
/bin/cp -a %{_sourcedir}/%{name}-%{version}-%{release} %{_builddir}/


############################################################################
%install
/bin/rm -rf %{buildroot}
/bin/mkdir -p %{buildroot}/tmp/
/bin/cp -a %{_builddir}/%{name}-%{version}-%{release} %{buildroot}/tmp/


############################################################################
%clean
/bin/rm -rf %{buildroot}


############################################################################
%post

# /tmp/%{name}-%{version}-%{release}
declare tmp=/tmp/%{name}-%{version}-%{release}

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
    if [ -e $dst.lock ]
    then
        echo "   Did not install $dst because of lockfile."
    else
        /usr/bin/rsync --devices --dirs --links --perms --quiet --specials --times $src/ $dst
        echo "   Installed $dst."
    fi
done

# install files
for src in $(/bin/find $tmp ! -type d | /bin/sort)
do
    declare dst=${src#$tmp}
    if [ -e $dst.lock ]
    then
        echo "   Did not install $dst because of lockfile."
    else
        if [ -e $dst ] && ! /usr/bin/cmp -s $src $dst
        then
            /bin/mv $dst $dst.rpmsave
        fi
        /usr/bin/rsync --devices --links --perms --quiet --specials --times $src $dst
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

# /var/lib/samba/private/passdb.tdb
/bin/echo -e "crimson\ncrimson" | /usr/bin/smbpasswd -a -s jharvard > /dev/null
echo "   Reset John Harvard's password for Samba to \"crimson\"."

# synchronize with /etc/skel/{.config,.local}
/usr/bin/rsync --archive --backup --links --quiet --suffix=.rpmsave /etc/skel/{.config,.local} /home/jharvard/
/bin/chown -R jharvard:students /home/jharvard/{.config,.local}
/usr/bin/rsync --archive --backup --links --quiet --suffix=.rpmsave /etc/skel/{.config,.local} /root/
echo "   Synchronized John Harvard and superuser with /etc/skel/{.config,.local}."

# disable services
declare -a off=(avahi-daemon dnsmasq firstboot ip6tables mdmonitor netconsole nfslock proftpd saslauthd)
for service in "${off[@]}"
do
    /sbin/chkconfig $service off > /dev/null 2>&1
    echo "   Disabled $service."
done

# enable services
declare -a on=(dkms_autoinstaller httpd iptables mysqld network netfs nfs ntpd rpcbind sendmail smb sshd usermin webmin yum-updatesd)
for service in "${on[@]}"
do
    /sbin/chkconfig $service on > /dev/null 2>&1
    echo "   Enabled $service."
done

# reset superuser's password for MySQL
/sbin/service mysqld stop > /dev/null 2>&1
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
/sbin/service mysqld start > /dev/null 2>&1
/usr/bin/mysql --user=root > /dev/null 2>&1 <<"EOF"
UPDATE mysql.user SET Password=PASSWORD('crimson') WHERE User='root';
FLUSH PRIVILEGES;
EOF
/sbin/service mysqld stop > /dev/null 2>&1
/bin/mv /etc/.my.cnf /etc/my.cnf
/sbin/service mysqld start > /dev/null 2>&1
echo "   Reset superuser's password for MySQL to \"crimson\"."

# reset John Harvard's password for MySQL
/usr/bin/mysql --force --user=root --password=crimson > /dev/null 2>&1 <<"EOF"
DROP USER ''@'%';
DROP USER ''@'localhost';
DROP USER ''@'localhost.localdomain';
DROP USER 'jharvard'@'%';
CREATE USER 'jharvard'@'%' IDENTIFIED BY 'crimson';
GRANT USAGE ON *.* TO 'jharvard'@'%' IDENTIFIED BY 'crimson';
GRANT ALL PRIVILEGES ON `jharvard\_%`.* TO 'jharvard'@'%';
EOF
echo "   Reset John Harvard's password for MySQL to \"crimson\"."

# restart services
declare -a restart=(httpd iptables network rpcbind nfs netfs proftpd smb sshd usermin webmin)
for service in "${restart[@]}"
do
    /sbin/service $service restart > /dev/null 2>&1
    echo "   Restarted $service."
done

# recompile schemas
# https://github.com/Quixotix/gedit-source-code-browser
/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
/bin/chmod -R a+rX /usr/share/glib-2.0/schemas/
echo "   Recompiled schemas."

# rebuild icon cache
/usr/bin/gtk-update-icon-cache /usr/share/icons/hicolor/ > /dev/null 2>&1
echo "   Rebuilt icon cache."

# redraw panel
/bin/sleep 2
/bin/touch /root/.config/xfce4/panel/launcher-*/*
echo "   Updated superuser's panel."
/bin/touch /home/jharvard/.config/xfce4/panel/launcher-*/*
echo "   Updated John Harvard's panel."

# remove sources
/bin/rm -rf /tmp/%{name}-%{version}-%{release}

# fix Scratch's audio
/bin/sed -i -e 's/^SCRATCH_SND_PLUGIN=vm-sound-alsa/SCRATCH_SND_PLUGIN=vm-sound-pulse/' /usr/bin/scratch

# import keys (to avoid warnings during future software updates)
/bin/rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
/bin/rpm --import http://linux.dropbox.com/fedora/rpm-public-key.asc
/bin/rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-i386

# rebuild mlocate.db
/etc/cron.daily/mlocate.cron

# return 0
/bin/true


##########################################################################
%files
%defattr(-,root,root,-)
/tmp/%{name}-%{version}-%{release}
%defattr(-,root,students,1770)
/tmp/%{name}-%{version}-%{release}/usr/local/samba/lib/usershares


##########################################################################
%changelog
* Sun Sep 4 2011 David J. Malan <malan@harvard.edu> - 2.3-1
- Initial build


##########################################################################
# HOW TO PREPARE...
#
# FIREBUG
# mkdir -p /path/to/SOURCES/tmp/%{name}-%{version}-%{release}/usr/lib/firefox-6/extensions/
# cd /path/to/SOURCES/tmp/%{name}-%{version}-%{release}/usr/lib/firefox-6/extensions/
# wget http://getfirebug.com/releases/firebug/1.8/firebug-1.8.1.xpi
# mkdir tmp/
# cd tmp/
# unzip ../firebug-1.8.1.xpi
# grep em:id install.rdf # to find id (which is firebug@software.joehewitt.com.xpi)
# zip -r firebug@software.joehewitt.com.xpi *
# mv firebug@software.joehewitt.com.xpi ..
# cd ..
# rm -rf firebug-1.8.1.xpi tmp/
#
# LIVE HTTP HEADERS
# mkdir -p /path/to/SOURCES/tmp/%{name}-%{version}-%{release}/usr/lib/firefox-5/extensions/
# cd /path/to/SOURCES/tmp/%{name}-%{version}-%{release}/usr/lib/firefox-5/extensions/
# wget http://releases.mozilla.org/pub/mozilla.org/addons/3829/live_http_headers-0.17-fx+sm.xpi
# mkdir tmp/
# cd tmp/
# unzip ../live_http_headers-0.17-fx+sm.xpi
# Change "<em:maxVersion>4.0.*</em:maxVersion>" to "<em:maxVersion>6.0.*</em:maxVersion>" in install.rdf for Firefox.
# grep em:id install.rdf # to find id (which is {8f8fe09b-0bd3-4470-bc1b-8cad42b8203a})
# zip -r {8f8fe09b-0bd3-4470-bc1b-8cad42b8203a}.xpi *
# mv {8f8fe09b-0bd3-4470-bc1b-8cad42b8203a}.xpi ..
# cd ..
# rm -rf live_http_headers-0.17-fx+sm.xpi tmp/
#
# WEB DEVELOPER
# mkdir -p /path/to/SOURCES/tmp/%{name}-%{version}-%{release}/usr/lib/firefox-5/extensions/
# cd /path/to/SOURCES/tmp/%{name}-%{version}-%{release}/usr/lib/firefox-5/extensions/
# wget https://addons.mozilla.org/firefox/downloads/latest/60/addon-60-latest.xpi?src=addondetail
# mkdir tmp/
# cd tmp/
# unzip ../web_developer-1.1.9-fx+sm.xpi
# Change "<em:maxVersion>4.0.*</em:maxVersion>" to "<em:maxVersion>6.0.*</em:maxVersion>" in install.rdf.
# grep em:id install.rdf # to find id (which is {c45c406e-ab73-11d8-be73-000a95be3b12})
# zip -r {c45c406e-ab73-11d8-be73-000a95be3b12}.xpi *
# mv {c45c406e-ab73-11d8-be73-000a95be3b12}.xpi ..
# cd ..
# rm -rf web_developer-1.1.9-fx+sm.xpi tmp/
