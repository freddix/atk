Summary:	Accessibility Toolkit
Name:		atk
Version:	2.10.0
Release:	1
Epoch:		1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/atk/2.10/%{name}-%{version}.tar.xz
# Source0-md5:	e77833d4445ebe6842e9f9a0667b0be7
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	diffutils
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
as tools such as screen readers and magnifiers, and alternative input
devices.

%package devel
Summary:	ATK - header and development documentation
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
ATK - header and development documentation.

%package apidocs
Summary:	ATK API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
ATK API documentation.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static	\
	--disable-silent-rules	\
	--enable-introspection	\
	--enable-shared		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/{as,be@latin,tk,ug,ps,ca@valencia,en@shaw}

%find_lang atk10

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f atk10.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/girepository-1.0/Atk-1.0.typelib

%files devel
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/atk*
%{_datadir}/gir-1.0/Atk-1.0.gir
%{_pkgconfigdir}/atk*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/atk

