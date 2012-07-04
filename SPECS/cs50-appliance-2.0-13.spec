############################################################################
Summary: Configures the CS50 Appliance.
Name: cs50-appliance
Version: 2.0
Release: 13
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Source: %{name}-%{version}
Vendor: CS50
URL: https://manual.cs50.net/Appliance
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: generic-release = 15
Requires: acpid bind-utils cs50-eclipse cs50-library-c dkms emacs firefox ftp garcon gcc gdb gdm gconf-editor gedit generic-logos generic-release git gnome-icon-theme-legacy gnome-menus gnome-packagekit httpd iptables java kernel-devel kernel-headers make man man-pages mercurial mod_suphp mysql mysql-server nano ncftp ntp openssh-clients openssh-server PackageKit-yum-plugin patch php php-mysql php-pecl-xdebug php-xml phpMyAdmin proftpd rcs render50 rsnapshot ruby rubygems setup sudo system-config-firewall system-config-keyboard system-config-language system-config-network system-config-services teamviewer6 telnet tidy usermin valgrind vim vim-X11 webmin wget xfce4-panel xorg-x11-fonts-misc xterm yum-plugin-fastestmirror yum-plugin-priorities yum-plugin-protectbase yum-updatesd yum-utils
BuildArch: i386


############################################################################
%description
The CS50 Appliance is a virtual machine that lets you
"take" CS50, even if you're not a student at Harvard.


############################################################################
%prep
/bin/rm -rf %{_builddir}/%{name}-%{version}-%{release}/
/bin/cp -a %{_sourcedir}/%{name}-%{version}-%{release} %{_builddir}/


############################################################################
%build


############################################################################
%check


############################################################################
%install
/bin/rm -rf %{buildroot}
/bin/mkdir -p %{buildroot}/tmp/
/bin/cp -a %{_builddir}/%{name}-%{version}-%{release} %{buildroot}/tmp/


############################################################################
%clean
/bin/rm -rf %{buildroot}


############################################################################
%pre

# /etc/group
/usr/sbin/groupadd -r courses > /dev/null 2>&1
/usr/sbin/groupadd students > /dev/null 2>&1

# /home/jharvard/
/usr/sbin/adduser --comment "John Harvard" --gid students --groups wheel jharvard > /dev/null 2>&1
/bin/echo crimson | /usr/bin/passwd --stdin jharvard > /dev/null


############################################################################
%post

# /etc/gdm/custom.conf

# /etc/banner

# /etc/gconf/gconf.xml.defaults/

# /etc/profile.d/cs50.sh

# /etc/sysconfig/network

# /etc/sysconfig/network-scripts/ifcfg-eth0

# /etc/sysconfig/network-scripts/ifcfg-eth1

# /etc/sysconfig/network-scripts/ifcfg-eth2

# off
/sbin/chkconfig auditd off
/sbin/chkconfig dnsmasq off
/sbin/chkconfig ip6tables off
/sbin/chkconfig lvm2-monitor off
/sbin/chkconfig mdmonitor off
/sbin/chkconfig netconsole off
/sbin/chkconfig netfs off
/sbin/chkconfig nfslock off
/sbin/chkconfig proftpd off
/sbin/chkconfig saslauthd off

# on
/sbin/chkconfig dkms_autoinstaller on
/sbin/chkconfig httpd on
/sbin/chkconfig iptables on
/sbin/chkconfig mysqld on
/sbin/chkconfig network on
/sbin/chkconfig ntpd on
/sbin/chkconfig sendmail on
/sbin/chkconfig sshd on
/sbin/chkconfig usermin on
/sbin/chkconfig webmin on
/sbin/chkconfig yum-updatesd on


#/bin/rm -rf /tmp/%{name}-%{version}-%{release}


############################################################################
%preun


############################################################################
%postun


##########################################################################
%triggerin -- garcon

files = (
 /etc/xdg/menus/xfce-applications.menu
 /usr/share/desktop-directories/CS50.directory
 /usr/share/applications/cs50-appliance.desktop
 /usr/share/applications/cs50-2010-fall.desktop
 /usr/share/applications/cs50-2011-fall.desktop
 /usr/share/applications/teamviewer.desktop
)


# /etc/xdg/menus/xfce-applications.menu

# /usr/share/desktop-directories/CS50.directory

# /usr/share/applications/cs50-appliance.desktop

# /usr/share/applications/cs50-2010-fall.desktop

# /usr/share/applications/cs50-2011-fall.desktop

# /usr/share/applications/teamviewer.desktop


##########################################################################
%triggerin -- gdm

# /etc/pam.d/gdm

# /etc/pam.d/gdm-password


##########################################################################
%triggerin -- httpd

# /etc/httpd/conf/httpd.conf

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- iptables 

# /etc/sysconfig/iptables


##########################################################################
%triggerin -- mod_suphp

# /etc/suphp.conf

# /etc/httpd/conf.d/mod_suphp.conf

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- mysql-server

# /etc/my.cnf

# root
/sbin/service mysqld stop > /dev/null
/bin/sed -i -e 's/^#skip-grant-tables/skip-grant-tables/' /etc/my.cnf
/bin/sed -i -e 's/^#skip-networking/skip-networking/' /etc/my.cnf
/sbin/service mysqld start > /dev/null
/usr/bin/mysql --user=root > /dev/null 2>&1 <<"EOF"
UPDATE mysql.user SET Password=PASSWORD('crimson') WHERE User='root';
FLUSH PRIVILEGES;
EOF
/sbin/service mysqld stop > /dev/null
/bin/sed -i -e 's/^skip-grant-tables/#skip-grant-tables/' /etc/my.cnf
/bin/sed -i -e 's/^skip-networking/#skip-networking/' /etc/my.cnf
/sbin/service mysqld start > /dev/null

# jharvard, etc.
/usr/bin/mysql --force --user=root --password=crimson > /dev/null 2>&1 <<"EOF"
DROP USER ''@'%';
DROP USER ''@'localhost';
DROP USER ''@'localhost.localdomain';
DROP USER 'jharvard'@'%';
CREATE USER 'jharvard'@'%' IDENTIFIED BY 'crimson';
GRANT USAGE ON *.* TO 'jharvard'@'%' IDENTIFIED BY 'crimson';
GRANT ALL PRIVILEGES ON `jharvard\_%`.* TO 'jharvard'@'%';
EOF

/bin/true


##########################################################################
%triggerin -- nano

# /etc/nanorc


##########################################################################
%triggerin -- openssh-server

# /etc/ssh/sshd_config

/sbin/service sshd restart > /dev/null 2>&1


##########################################################################
%triggerin -- php

# /etc/php.ini

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- phpMyAdmin

# /etc/httpd/conf.d/phpMyAdmin.conf

# /etc/phpMyAdmin/config.inc.php

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- rsnapshot

# /etc/rsnapshot.conf

# /etc/cron.d/rsnapshot


##########################################################################
%triggerin -- setup

# /etc/hosts


##########################################################################
%triggerin -- sudo

# /etc/sudoers


##########################################################################
%triggerin -- usermin

# /etc/usermin/miniserv.conf

# /etc/usermin/changepass/config

# /etc/usermin/webmin.acl

/sbin/service usermin restart > /dev/null 2>&1


##########################################################################
%triggerin -- vim

# /etc/vimrc


##########################################################################
%triggerin -- webmin

# /etc/webmin/miniserv.conf

# /etc/webmin/proftpd/config

/sbin/service webmin restart > /dev/null 2>&1


##########################################################################
%triggerin -- xfce4-panel

# /etc/xdg/xfce4/panel/default.xml

# /etc/skel/.config/xfce4/panel/launcher-3/Eclipse.desktop

# /etc/skel/.config/xfce4/panel/launcher-4/Firefox.desktop

# /etc/skel/.config/xfce4/panel/launcher-5/Terminal.desktop

# /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml
/bin/mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
/bin/ln -sf /etc/xdg/xfce4/panel/default.xml /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml

# /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml

# /home/jharvard/.config/xfce4/panel/
/usr/bin/sudo -u jharvard /bin/mkdir -p /home/jharvard/.config/xfce4/panel/
/usr/bin/sudo -u jharvard /usr/bin/rsync --delete --copy-links --recursive /etc/skel/.config/xfce4/panel/* /home/jharvard/.config/xfce4/panel/

# /home/jharvard/.config/xfce4/xfconf/
/usr/bin/sudo -u jharvard /bin/mkdir -p /home/jharvard/.config/xfce4/xfconf/
/usr/bin/sudo -u jharvard /usr/bin/rsync --delete --copy-links --recursive /etc/skel/.config/xfce4/xfconf/* /home/jharvard/.config/xfce4/xfconf/

# /root/.config/xfce4/panel/
/bin/mkdir -p /root/.config/xfce4/panel/
/usr/bin/rsync --copy-links --delete --recursive /etc/skel/.config/xfce4/panel/* /root/.config/xfce4/panel/

# /root/.config/xfce4/xfconf/
/bin/mkdir -p /root/.config/xfce4/xfconf/
/usr/bin/rsync --copy-links --delete --recursive /etc/skel/.config/xfce4/xfconf/* /root/.config/xfce4/xfconf/


##########################################################################
%triggerin -- xorg-x11-fonts-misc

# /etc/X11/Xresources


##########################################################################
%files
%defattr(-,root,root,-)
/


##########################################################################
%changelog
* Sun Jul 24 2011 David J. Malan <dmalan@harvard.edu> - 2.0-13

* Sat Jul 23 2011 David J. Malan <dmalan@harvard.edu> - 2.0-11
- Defined EDITOR.
- Made release distribution-specific with %{?dist}.

* Sat Jul 16 2011 David J. Malan <dmalan@harvard.edu> - 2.0-9
- Various updates.

* Sat Jul 16 2011 David J. Malan <dmalan@harvard.edu> - 2.0-7
- Various updates.

* Sat Jul 16 2011 David J. Malan <dmalan@harvard.edu> - 2.0-6
- Reconfigured phpMyAdmin.

* Wed Jul 13 2011 David J. Malan <dmalan@harvard.edu> - 2.0-1
- Removed Fall 2009 from Menu.

* Tue Jul 12 2011 David J. Malan <dmalan@harvard.edu> - 
- Initial build
