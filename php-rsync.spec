%define modname rsync
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B21_%{modname}.ini

Summary:	Wrapper for librsync library
Name:		php-%{modname}
Version:	0.1.0
Release:	%mkrel 5
Group:		Development/PHP
License:	Modified BSD License
URL:		http://pecl.php.net/package/rsync/
Source0:	http://pecl.php.net/get/rsync-%{version}.tgz
Source1:	B21_rsync.ini
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	librsync-devel >= 0.9.7
BuildRequires:	popt-devel
BuildRequires:	bzip2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE rsync_extension.php examples/*.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

