%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%endif

%if 0%{?rhel} > 7
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-netaddr
Version:        0.7.19
Release:        8%{?dist}
Summary:        A pure Python network address representation and manipulation library

License:        BSD
URL:            http://github.com/drkjam/netaddr
Source0:        https://pypi.python.org/packages/source/n/netaddr/netaddr-%{version}.tar.gz

BuildArch:      noarch

Patch0: 0001-fixed-broken-tests-in-issue-149-python-3-regression-.patch
Patch1: 0001-Do-not-override-executable-path.patch

%global desc A network address manipulation library for Python\
\
Provides support for:\
\
Layer 3 addresses\
\
 * IPv4 and IPv6 addresses, subnets, masks, prefixes\
 * iterating, slicing, sorting, summarizing and classifying IP networks\
 * dealing with various ranges formats (CIDR, arbitrary ranges and globs, nmap)\
 * set based operations (unions, intersections etc) over IP addresses and subnets\
 * parsing a large variety of different formats and notations\
 * looking up IANA IP block information\
 * generating DNS reverse lookups\
 * supernetting and subnetting\
\
Layer 2 addresses\
\
 * representation and manipulation MAC addresses and EUI-64 identifiers\
 * looking up IEEE organisational information (OUI, IAB)\
 * generating derived IPv6 addresses


%global _description\
%{desc}

%description %_description

%if %{with python2}
%package -n python2-netaddr
Summary: %summary
%{?python_provide:%python_provide python2-netaddr}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-pytest

%description -n python2-netaddr %_description
%endif #{with python2}

%if 0%{?with_python3}
%package -n python3-netaddr
Summary: A pure Python network address representation and manipulation library
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-pytest

%description -n python3-netaddr
%{desc}
%endif

%prep
%setup -q -n netaddr-%{version}
%patch0 -p1
%patch1 -p1

# Make rpmlint happy, get rid of DOS line endings
sed -i 's/\r//' netaddr/*.py netaddr/ip/*.py netaddr/eui/*.idx

# Make rpmlint happy, rip out python shebang lines from most python
# modules
find netaddr -name "*.py" | \
  xargs sed -i -e '1 {/^#!\//d}'
# Fix python executable
%if %{with python2}
sed -i -e '1s,/usr/bin/env python,%{__python2} %{?py_shbang_opts},' netaddr/tools/netaddr
%else
sed -i -e '1s,/usr/bin/env python,%{__python3} %{?py_shbang_opts},' netaddr/tools/netaddr
%endif #{with python2}

# Make rpmlint happy, fix permissions on documentation files
chmod 0644 README.md AUTHORS CHANGELOG COPYRIGHT LICENSE PKG-INFO

%build
%if %{with python2}
%py2_build
%endif #{with python2}

%if 0%{?with_python3}
%py3_build
%endif

#docs
pushd docs
%if %{with python2}
PYTHONPATH='../' sphinx-build -b html -d build/doctrees source html
%endif #{with python2}
%if 0%{?with_python3}
PYTHONPATH='../' sphinx-build-%{python3_version} -b html -d build/doctrees source python3/html
%endif
popd


%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/netaddr %{buildroot}%{_bindir}/netaddr3
%endif

%if %{with python2}
%py2_install
%endif #{with python2}


%check
%if %{with python2}
py.test-%{python2_version}
%endif #{with python2}
%if 0%{?with_python3}
LANG=en_US.UTF-8 py.test-%{python3_version}
%endif

%if %{with python2}
%files -n python2-netaddr
%license COPYRIGHT LICENSE
%doc AUTHORS CHANGELOG
%doc README.md docs/html
%{python2_sitelib}/*
%{_bindir}/netaddr
%endif #{with python2}

%if 0%{?with_python3}
%files -n python3-netaddr
%license COPYRIGHT
%doc AUTHORS CHANGELOG
%doc README.md docs/python3/html
%{python3_sitelib}/*
%{_bindir}/netaddr3
%endif

%changelog
* Mon Jul 09 2018 Petr Viktorin <pviktori@redhat.com> - 0.7.19-8
- Don't build python2 subpackage on rhel>7
  https://bugzilla.redhat.com/show_bug.cgi?id=1567153

* Mon Feb 19 2018 John Eckersberg <eck@redhat.com> - 0.7.19-7
- Fix shebang mangling for python3 (RHBZ#1546800)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.7.19-5
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.19-4
- Python 2 binary package renamed to python2-netaddr
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 John Eckersberg <eck@redhat.com> - 0.7.19-1
- New upstream release 0.7.19 (RHBZ#1413231)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.18-10
- Rebuild for Python 3.6

* Sun Nov 13 2016 Orion Poplawski <orion@cora.nwra.com> - 0.7.18-9
- Update description
- Fix netaddr shebang (bug #1394046)

* Thu Nov 10 2016 Orion Poplawski <orion@cora.nwra.com> - 0.7.18-8
- Use updated python macros
- Use %%license

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.18-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar  8 2016 John Eckersberg <eck@redhat.com> - 0.7.18-6
- Add provides for python2-netaddr (RHBZ#1282129)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Robert Kuska <rkuska@redhat.com> - 0.7.18-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
- Delete file which contains bundled pytest

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.18-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.18-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep  4 2015 John Eckersberg <eck@redhat.com> - 0.7.18-1
- New upstream release 0.7.18 (RHBZ#1259969)

* Tue Sep  1 2015 John Eckersberg <eck@redhat.com> - 0.7.17-1
- New upstream release 0.7.17

* Mon Jun 29 2015 John Eckersberg <eck@redhat.com> - 0.7.15-1
- New upstream release 0.7.15
- Add separate source for tests, see https://github.com/drkjam/netaddr/issues/102
- Add patch for broken assertion, see https://github.com/drkjam/netaddr/pull/103

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 John Eckersberg <eck@redhat.com> - 0.7.14-1
- New upstream release 0.7.14

* Wed Sep 17 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 0.7.12-1
- Upstream 0.7.12
- Conditionalize python3 subpackages build on Fedora
- Few spec cleanups

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.11-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 John Eckersberg <jeckersb@redhat.com> - 0.7.11-1
- New upstream release 0.7.11
- Enabled Python 3 support (bz1070357)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 30 2011 Jakub Hrozek <jhrozek@redhat.com> - 0.7.5-3
- Do not traceback on invalid IPNetwork input (upstream issues #2, #6, #5, #8)
- Remove executable bit from documentation files to make rpmlint happy

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 John Eckersberg <jeckersb@redhat.com> - 0.7.5-1
- New upstream release 0.7.5
- Updated summary and description to match upstream README
- Updated URL and source to reflect upstream move to github

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 17 2010 John Eckersberg <jeckersb@redhat.com> - 0.7.4-1
- New upstream release 0.7.4

* Wed Sep 30 2009 John Eckersberg <jeckersb@redhat.com> - 0.7.3-1
- New upstream release 0.7.3

* Fri Aug 21 2009 John Eckersberg <jeckersb@redhat.com> - 0.7.2-1
- New upstream release 0.7.2
- Updated Summary and Description with new values provided by upstream

* Mon Aug 17 2009 John Eckersberg <jeckersb@redhat.com> - 0.7.1-1
- New upstream release 0.7.1 fixes naming conflict with 'nash' by
  renaming the netaddr shell to 'netaddr'

* Wed Aug 12 2009 John Eckersberg <jeckersb@redhat.com> - 0.7-1
- Upstream release 0.7

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.3-2
- Minor tweaks to spec file aligning with latest Fedora packaging guidelines
- Enforce python 2.4 dependency as needed by netaddr >= 0.6.2
- Drop BR on python-setuptool as it is not imported in setup.py
- Drop BR on dos2unix use sed instead
- Align description with that of delivered PKG-INFO
- Rip out python shebangs
- Add %%check section to enable tests
- Thanks to Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Jun 23 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.3-1
- New upstream bugfix release

* Mon Apr 13 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.2-1
- New upstream bugfix release

* Tue Apr 7 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.1-1
- New upstream bugfix release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 0.6-2
- Add BuildDepends on dos2unix to clean up some upstream sources

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 0.6-1
- New upstream version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.2-2
- Rebuild for Python 2.6

* Fri Oct 10 2008 John Eckersberg <jeckersb@redhat.com> - 0.5.2-1
- New upstream version, bug fixes for 0.5.1

* Tue Sep 23 2008 John Eckersberg <jeckersb@redhat.com> - 0.5.1-1
- New upstream version, bug fixes for 0.5

* Sun Sep 21 2008 John Eckersberg <jeckersb@redhat.com> - 0.5-1
- New upstream version

* Mon Aug 11 2008 John Eckersberg <jeckersb@redhat.com> - 0.4-1
- Initial packaging for Fedora

