Summary:	A library for easy access to smart cards (chipcards)
Summary(pl):	Biblioteka do �atwego dost�pu do kart procesorowych
Name:		libchipcard2
# "beta" is constant suffix added to all releases before stable version,
# no need to move it to release - there won't be 1.9.19 non-beta release
Version:	1.9.19beta
Release:	1
License:	GPL v2 with OpenSSL linking exception
Group:		Libraries
Source0:	http://dl.sourceforge.net/libchipcard/%{name}-%{version}.tar.gz
# Source0-md5:	c8f3e08474a893890c4d221288c9e7a6
URL:		http://www.libchipcard.de/
BuildRequires:	gwenhywfar-devel >= 1.99.1
BuildRequires:	libusb-devel
BuildRequires:	opensc-devel >= 0.9.4
BuildRequires:	pkgconfig
BuildRequires:	sysfsutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libchipcard allows easy access to smart cards. It provides basic
access to memory and processor cards and has special support for
German medical cards, German "GeldKarte" and HBCI (homebanking) cards
(both type 0 and type 1). It accesses the readers via CTAPI or IFD
interfaces and has successfully been tested with Towitoko, Kobil, SCM,
Orga, Omnikey and Reiner-SCT readers. This package contains the
chipcard2 daemon needed to access card readers.

%description -l pl
libchipcard pozwala na �atwy dost�p do kart procesorowych. Daje
podstawowy dost�p do kart pami�ciowych i procesorowych, ma tak�e
specjaln� obs�ug� niemieckich kart medycznych, niemieckich kart
"GeldKarte" oraz kart HBCI (do homebankingu, zar�wno typu 0 jak i 1).
Z czytnikami komunikuje si� poprzez interfejs CTAPI lub IFD, by�a
testowana z czytnikami Towitoko, Kobil, SCM, Orga, Omnikey i
Reiner-SCT. Ten pakiet zawiera demona chipcard2 potrzebnego do dost�pu
do czytnik�w kart.

%package devel
Summary:	libchipcard server development kit
Summary(pl):	Pliki programistyczne serwera libchipcard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gwenhywfar-devel >= 1.99.1
Requires:	libusb-devel
Requires:	sysfsutils-devel

%description devel
This package contains chipcard2-server-config and header files for
writing drivers, services or even your own chipcard daemon for
libchipcard.

%description devel
Ten pakiet zawiera skrypt chipcard2-server-config oraz pliki
nag��wkowe do pisania sterownik�w, us�ug, a nawet w�asnych demon�w
kart dla libchipcard.

%prep
%setup -q

%build
# pcmcia code needs fix to use userspace headers
%configure \
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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/reader-lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/reader-lib*.so
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
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/chipcard2
%{_includedir}/chipcard2-client
%{_includedir}/chipcard2-server
%{_includedir}/chipcard2-service
%{_aclocaldir}/chipcard2-server.m4
%{_aclocaldir}/chipcard2-client.m4
