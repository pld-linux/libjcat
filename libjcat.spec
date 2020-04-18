#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library for reading and writing Jcat files
Summary(pl.UTF-8):	Biblioteka do odczytu i zapisu plików Jcat
Name:		libjcat
Version:	0.1.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	22295ec8d6ac55afacd14f54b82dc8d8
URL:		https://github.com/hughsie/libjcat
BuildRequires:	glib2-devel >= 1:2.45.8
BuildRequires:	gnutls-devel >= 3.6.0
BuildRequires:	gpgme-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	json-glib-devel >= 1.1.1
BuildRequires:	libgpg-error-devel
BuildRequires:	meson >= 0.52.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.45.8
Requires:	gnutls >= 3.6.0
Requires:	json-glib >= 1.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows reading and writing gzip-compressed JSON catalog
files, which can be used to store GPG, PKCS-7 and SHA-256 checksums
for each file.

This provides equivalent functionality to the catalog files supported
in Microsoft Windows.

%description -l pl.UTF-8
Ta biblioteka pozwala na odczyt i zapis skompresowanych gzipem plików
katalogów JSON, które mogą służyć do zapisu sum kontrolnych GPG, PKCS-7
i SHA-256 dla każdego pliku.

Daje do funkcjonalność odpowiadającą plikom catalog, obsługiwanym w
Microsoft Windows.

%package devel
Summary:	Header files for Jcat library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Jcat
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.45.8
Requires:	gnutls-devel >= 3.6.0
Requires:	gpgme-devel
Requires:	json-glib-devel >= 1.1.1
Requires:	libgpg-error-devel

%description devel
Header files for Jcat library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Jcat.

%package static
Summary:	Static Jcat library
Summary(pl.UTF-8):	Statyczna biblioteka Jcat
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Jcat library.

%description static -l pl.UTF-8
Statyczna biblioteka Jcat.

%package -n vala-libjcat
Summary:	Vala API for Jcat library
Summary(pl.UTF-8):	API języka Vala do biblioteki Jcat
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-libjcat
Vala API for Jcat library.

%description -n vala-libjcat -l pl.UTF-8
API języka Vala do biblioteki Jcat.

%package apidocs
Summary:	API documentation for Jcat library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Jcat
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Jcat library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Jcat.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Dgtkdoc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/installed-tests \
	$RPM_BUILD_ROOT%{_datadir}/installed-tests

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/jcat-tool
%attr(755,root,root) %{_libdir}/libjcat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjcat.so.1
%{_libdir}/girepository-1.0/Jcat-1.0.typelib
%{_mandir}/man1/jcat-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjcat.so
%{_includedir}/libjcat-1
%{_datadir}/gir-1.0/Jcat-1.0.gir
%{_pkgconfigdir}/jcat.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjcat.a
%endif

%files -n vala-libjcat
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/jcat.deps
%{_datadir}/vala/vapi/jcat.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libjcat
%endif
