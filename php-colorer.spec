%define modname colorer
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A48_%{modname}.ini

Summary:	Syntax highlighting for PHP
Name:		php-%{modname}
Version:	0.7
Release:	%mkrel 21
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/colorer
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
Patch0:		colorer-0.7-no_rpath.diff
Patch1:		colorer-0.7-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libcolorer-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Colorer take5 is a syntax highlighting and text parsing library, that provides
services of text parsing in host editor systems in real-time and transforming
results into colored text. For details, see http://colorer.sourceforge.net/
   
While colorer is primarily designed for use with text editors, it can be also
used for non-interactive syntax highlighting, for example, in web
applications. This PHP extension provides basic functions for syntax
highlighting.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0
%patch1 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS EXPERIMENTAL README TODO package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
