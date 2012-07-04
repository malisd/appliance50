############################################################################
Summary: CS153 Fall 2011
Name: cs153-2011-fall
Version: 1.0
Release: 1
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Source: %{name}-%{version}-%{release}
Vendor: CS50
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(pre): cs50-appliance
Requires: coq
Requires: ghc
Requires: llvm
Requires: ocaml
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
Configures appliance for Fall 2011 of CS153.


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
%files
%defattr(0644,root,root,0755)
/


############################################################################
%changelog
* Sun Aug 21 2011 David J. Malan <malan@harvard.edu> - 1.0-1
- Initial build.
