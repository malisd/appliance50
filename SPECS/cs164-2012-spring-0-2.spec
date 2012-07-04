###########################################################################
Summary: CS164
Name: cs164-2012-spring
Version: 0
Release: 2
License: GPLv2 with exceptions or CDDL
Group: System Environment/Base
Vendor: CS50
BuildArch: i386
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: cs50-appliance = 3
Provides: cs164


############################################################################
%description
Mobile Software Engineering


############################################################################
%prep
/bin/rm -rf %{_builddir}/%{name}-%{version}-%{release}/
/bin/cp -a %{_sourcedir}/%{name}-%{version}-%{release} %{_builddir}/


############################################################################
%install
/bin/rm -rf %{buildroot}
/bin/cp -a %{_builddir}/%{name}-%{version}-%{release} %{buildroot}/


############################################################################
%clean
/bin/rm -rf %{buildroot}


############################################################################
%post

# its presence disables Indexes; removal will be integrated to cs50-appliance RPM eventually
/bin/rm -f /etc/httpd/conf.d/welcome.conf > /dev/null 2>&1

# ensure /home/jharvard/logs exists
/bin/mkdir /home/jharvard/logs > /dev/null 2>&1
/bin/chown -R /home/jharvard/logs > /dev/null 2>&1
/bin/chmod 0755 /home/jharvard/logs > /dev/null 2>&1
/bin/chmod 0644 /home/jharvard/logs/* > /dev/null 2>&1

# reload httpd
/bin/systemctl reload httpd.service > /dev/null 2>&1

# install NetBeans
/bin/chmod 0700 /tmp/netbeans-7.1-ml-php-linux.sh
/tmp/netbeans-7.1-ml-php-linux.sh --silent
/bin/rm -f /tmp/netbeans-7.1-ml-php-linux.sh
/bin/chmod -R a+rX /usr/local/netbeans-7.1
/bin/ln -s /usr/local/netbeans-7.1/bin/netbeans /usr/local/bin/ > /dev/null 2>&1

# the installer seems to put this in either location!
/bin/chmod 0644 /usr/local/share/applications/netbeans-7.1.desktop > /dev/null 2>&1
/bin/chmod 0644 /usr/share/applications/netbeans-7.1.desktop > /dev/null 2>&1

# return 0
/bin/true


############################################################################
%preun

# uninstall NetBeans
/usr/local/netbeans-7.1/uninstall.sh --silent
/bin/rm -f /usr/local/bin/netbeans

# remove NetBeans from menu (which its uninstaller forgets to do)
/bin/rm -f /usr/local/share/applications/netbeans-7.1.desktop > /dev/null 2>&1
/bin/rm -f /usr/share/applications/netbeans-7.1.desktop > /dev/null 2>&1


############################################################################
%postun

# restart httpd
/bin/systemctl stop httpd.service > /dev/null 2>&1
/bin/systemctl start httpd.service > /dev/null 2>&1


##########################################################################
%files
%defattr(-,root,root,-)
/etc/httpd/conf.d/cs164.conf
/tmp/netbeans-7.1-ml-php-linux.sh
