%define modname rsync
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B21_%{modname}.ini

Summary:	Wrapper for librsync library
Name:		php-%{modname}
Version:	0.1.0
Release:	7
Group:		Development/PHP
License:	Modified BSD License
URL:		https://pecl.php.net/package/rsync/
Source0:	http://pecl.php.net/get/rsync-%{version}.tgz
Source1:	B21_rsync.ini
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	librsync-devel >= 0.9.7
BuildRequires:	popt-devel
BuildRequires:	bzip2-devel

%description
include the posibility to php to generate signatur files, patches and patch
files with the rsync functionality.

%prep

%setup -q -n %{modname}-%{version}

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

chmod 644 LICENSE rsync_extension.php examples/*.php

%build
%serverbuild

phpize
%configure2_5x --disable-static --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files
%defattr(-,root,root)
%doc LICENSE rsync_extension.php examples/*.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2012.0
+ Revision: 795495
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4
+ Revision: 761287
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3
+ Revision: 696464
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2
+ Revision: 695459
- rebuilt for php-5.3.7

* Tue Jun 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1
+ Revision: 683087
- fix deps
- silly typo
- fix build
- import php-rsync


* Tue Jun 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.2
- initial Mandriva package
