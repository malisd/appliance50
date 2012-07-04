############################################################################
Summary: CS50 Spring 2012
Name: cs51-2012-spring
Version: 0
Release: 1
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Source: %{name}-%{version}-%{release}
Vendor: CS50
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Provides: cs51
Requires: ocaml
Requires: emacs-tuareg
Requires: emacs-tuareg-el
Requires(pre): coreutils
Requires(pre): shadow-utils
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
Configures CS50 Appliance for CS51.


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

# /etc/group
/usr/sbin/groupadd -r courses > /dev/null 2>&1

# /etc/passwd
/usr/sbin/adduser --comment "CS51" --create-home --gid courses --shell /sbin/nologin --skel /dev/null --system cs51 > /dev/null 2>&1

# return 0
/bin/true


############################################################################
%postun

# http://www.redhat.com/archives/rpm-list/2003-August/msg00077.html
# http://www.redhat.com/archives/rpm-list/2005-February/msg00017.html
[ $1 != 0 ] && exit 0

# /etc/passwd
/usr/sbin/userdel --remove cs51 > /dev/null 2>&1

# /etc/group
/usr/sbin/groupdel courses > /dev/null 2>&1

# return 0
/bin/true


############################################################################
%files
%defattr(-,root,root,-)
/usr/share/emacs/site-lisp/site-start.d/cs51-init.el


############################################################################
%changelog
