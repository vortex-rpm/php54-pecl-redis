%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?pecl_phpdir: %{expand: %%global pecl_phpdir  %(%{__pecl} config-get php_dir  2> /dev/null || echo undefined)}}

%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%global php_base php54
%global pecl_name redis
%global real_name redis

Summary: Extension for working with redis
Name: %{php_base}-pecl-redis

Version: 2.2.2
Release: 1.vortex%{?dist}
License: PHP
Group: Development/Languages
Vendor: Vortex RPM
URL: https://github.com/nicolasff/%{pecl_name}

Source0: %{pecl_name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{php_base}-devel, %{php_base}-cli, %{php_base}-pear
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if %{?php_zend_api}0
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: %{php_base}-api = %{php_apiver}
%endif

%description
The phpredis extension provides an API for communicating with the Redis
key-value store. It is released under the PHP License, version 3.01.
This code has been developed and maintained by Owlient from November 2009
to March 2011.

%prep 
%setup -q -n %{pecl_name}-%{version}


%build
phpize
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

EOF


%clean
%{__rm} -rf %{buildroot}



%postun
if [ $1 -eq 0 ]; then
%{__pecl} uninstall --nodeps --ignore-errors --register-only %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/redis.so


%changelog
* Mon Oct 08 2012 Ilya A. Otyutskiy <sharp@thesharp.ru> - 2.2.2-1.vortex
- Initial packaging.
