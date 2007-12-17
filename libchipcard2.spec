#
# Conditional build:
%bcond_without	sysfs	# don't use sysfs to scan for ttyUSB
#
Summary:	A library for easy access to smart cards (chipcards)
Summary(pl.UTF-8):	Biblioteka do łatwego dostępu do kart procesorowych
Name:		libchipcard2
Version:	2.1.10
Release:	0.1
License:	GPL v2 with OpenSSL linking exception
Group:		Libraries
Source0:	http://dl.sourceforge.net/libchipcard/%{name}-%{version}.tar.gz
# Source0-md5:	0a8669ed2c996eb2816b8e125a9c68f2
Patch0:		%{name}-reader.patch
URL:		http://www.libchipcard.de/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gwenhywfar-devel >= 2.3.0
BuildRequires:	gwenhywfar-devel < 3.0.0
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	opensc-devel >= 0.9.4
BuildRequires:	pkgconfig
%{?with_sysfs:BuildRequires:	sysfsutils-devel >= 1.3.0-3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libchipcard allows easy access to smart cards. It provides basic
access to memory and processor cards and has special support for
German medical cards, German "GeldKarte" and HBCI (homebanking) cards
(both type 0 and type 1). It accesses the readers via CTAPI or IFD
interfaces and has successfully been tested with Towitoko, Kobil, SCM,
Orga, Omnikey and Reiner-SCT readers. This package contains the
chipcard2 daemon needed to access card readers.

%description -l pl.UTF-8
libchipcard pozwala na łatwy dostęp do kart procesorowych. Daje
podstawowy dostęp do kart pamięciowych i procesorowych, ma także
specjalną obsługę niemieckich kart medycznych, niemieckich kart
"GeldKarte" oraz kart HBCI (do homebankingu, zarówno typu 0 jak i 1).
Z czytnikami komunikuje się poprzez interfejs CTAPI lub IFD, była
testowana z czytnikami Towitoko, Kobil, SCM, Orga, Omnikey i
Reiner-SCT. Ten pakiet zawiera demona chipcard2 potrzebnego do dostępu
do czytników kart.

%package devel
Summary:	libchipcard server development kit
Summary(pl.UTF-8):	Pliki programistyczne serwera libchipcard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gwenhywfar-devel >= 2.0.0
Requires:	libusb-devel
%{?with_sysfs:Requires:	sysfsutils-devel >= 1.3.0-3}

%description devel
This package contains chipcard2-server-config and header files for
writing drivers, services or even your own chipcard daemon for
libchipcard.

%description devel -l pl.UTF-8
Ten pakiet zawiera skrypt chipcard2-server-config oraz pliki
nagłówkowe do pisania sterowników, usług, a nawet własnych demonów
kart dla libchipcard.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# pcmcia code needs fix to use userspace headers
%configure \
	%{!?with_sysfs:ac_cv_header_sysfs_libsysfs_h=no} \
	--with-kernel-sources=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/reader-lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/crypttoken/*.la
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard2-client/chipcardc2.conf{.example,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard2-client/chipcardc2.conf.minimal
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard2-server/chipcardd2.conf{.example,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard2-server/chipcardd2.conf.minimal
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard2-server/chipcardrd.conf{.example,}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{CERTIFICATES,IPCCOMMANDS,*.conf.*}
%attr(755,root,root) %{_bindir}/cardcommander2
%attr(755,root,root) %{_bindir}/chipcard-tool
%attr(755,root,root) %{_bindir}/geldkarte2
%attr(755,root,root) %{_bindir}/kvkcard2
%attr(755,root,root) %{_bindir}/memcard2
%attr(755,root,root) %{_bindir}/rsacard2
%attr(755,root,root) %{_sbindir}/chipcardd2
%attr(755,root,root) %{_sbindir}/chipcardrd
%attr(755,root,root) %{_libdir}/libchipcard2_ctapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard2_ctapi.so.0
%attr(755,root,root) %{_libdir}/libchipcard2c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard2c.so.0
%attr(755,root,root) %{_libdir}/libchipcard2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard2d.so.0
%attr(755,root,root) %{_libdir}/libchipcard2i.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard2i.so.0
%attr(755,root,root) %{_libdir}/libchipcard2sv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard2sv.so.0
%attr(755,root,root) %{_libdir}/reader-libchipcard2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/reader-libchipcard2.so.0
%attr(755,root,root) %{_libdir}/reader-libchipcard2.so
%dir %{_libdir}/chipcard2-server
%dir %{_libdir}/chipcard2-server/drivers
%{_libdir}/chipcard2-server/drivers/*.xml
%attr(755,root,root) %{_libdir}/chipcard2-server/drivers/ccid
%attr(755,root,root) %{_libdir}/chipcard2-server/drivers/ctapi
%attr(755,root,root) %{_libdir}/chipcard2-server/drivers/ifd
%attr(755,root,root) %{_libdir}/chipcard2-server/drivers/ifdold
%attr(755,root,root) %{_libdir}/chipcard2-server/drivers/pcsc
%dir %{_libdir}/chipcard2-server/lowlevel
%dir %{_libdir}/chipcard2-server/services
%{_libdir}/chipcard2-server/services/*.xml
%attr(755,root,root) %{_libdir}/chipcard2-server/services/cardfs
%attr(755,root,root) %{_libdir}/chipcard2-server/services/kvks
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/crypttoken/*.so*
%{_libdir}/gwenhywfar/plugins/*/crypttoken/*.xml
%dir %{_sysconfdir}/chipcard2-client
%{_sysconfdir}/chipcard2-client/apps
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard2-client/chipcardc2.conf
%dir %{_sysconfdir}/chipcard2-server
%{_sysconfdir}/chipcard2-server/cards
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard2-server/chipcardd2.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard2-server/chipcardrd.conf
%{_sysconfdir}/chipcard2-server/drivers

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chipcard2-server-config
%attr(755,root,root) %{_bindir}/chipcard2-client-config
%attr(755,root,root) %{_libdir}/libchipcard2_ctapi.so
%attr(755,root,root) %{_libdir}/libchipcard2c.so
%attr(755,root,root) %{_libdir}/libchipcard2d.so
%attr(755,root,root) %{_libdir}/libchipcard2i.so
%attr(755,root,root) %{_libdir}/libchipcard2sv.so
%{_libdir}/libchipcard2_ctapi.la
%{_libdir}/libchipcard2c.la
%{_libdir}/libchipcard2d.la
%{_libdir}/libchipcard2i.la
%{_libdir}/libchipcard2sv.la
%{_includedir}/chipcard2
%{_includedir}/chipcard2-client
%{_includedir}/chipcard2-server
%{_includedir}/chipcard2-service
%{_aclocaldir}/chipcard2-server.m4
%{_aclocaldir}/chipcard2-client.m4
