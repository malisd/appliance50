############################################################################
Summary: CS50 Fall 2011
Name: cs50-2011-fall
Version: 1.5
Release: 2
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Source: %{name}-%{version}-%{release}
Vendor: CS50
URL: https://manual.cs50.net/2011
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(pre): cs50-appliance
BuildArch: i386


############################################################################
# ensure RPM is portable by avoiding rpmlib(FileDigests)
# http://lists.rpm.org/pipermail/rpm-list/2009-October/000401.html
%global _binary_filedigest_algorithm 1
%global _source_filedigest_algorithm 1


############################################################################
# ensure RPM is portable by avoiding rpmlib(PayloadIsXz)
# http://www.cmake.org/pipermail/cmake/2010-March/035580.html
%global _binary_payload w9.gzdio


############################################################################
%description
Configures appliance for for Fall 2011.


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
%pre

# /etc/passwd
/usr/sbin/adduser --comment "CS50" --create-home --gid courses --shell /sbin/nologin --skel /dev/null --system cs50 > /dev/null 2>&1

# return 0
/bin/true


############################################################################
%post

# /home/cs50/
/bin/echo "   Installed CS50's home directory."


############################################################################
%postun

# http://www.redhat.com/archives/rpm-list/2003-August/msg00077.html
# http://www.redhat.com/archives/rpm-list/2005-February/msg00017.html
[ $1 != 0 ] && exit 0

# /etc/passwd
/usr/sbin/userdel --remove cs50 > /dev/null 2>&1

# return 0
/bin/true


############################################################################
%files
%defattr(-,cs50,courses,-)
/home/cs50


############################################################################
%changelog
* Fri Oct 24 2011 David J. Malan <malan@harvard.edu> - 1.5-1
- Added support for Problem Set 5.
* Fri Oct 10 2011 David J. Malan <malan@harvard.edu> - 1.4-1
- Added support for Problem Set 5.
* Sat Sep 24 2011 David J. Malan <malan@harvard.edu> - 1.1-2
- Added 3x3.txt and 4x4.txt.
* Fri Sep 23 2011 David J. Malan <malan@harvard.edu> - 1.1-1
- Added pset3 binaries.
* Fri Sep 9 2011 David J. Malan <malan@harvard.edu> - 1.0-2
* Fri Sep 16 2011 David J. Malan <malan@harvard.edu> - 1.0-3
- Added pset2 binaries.
* Fri Sep 9 2011 David J. Malan <malan@harvard.edu> - 1.0-2
- Fixed implementation of pennies.
* Fri Sep 9 2011 David J. Malan <malan@harvard.edu> - 1.0-1
- Initial build
