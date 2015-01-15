Summary:	SBLIM CMPI NFSv4 instrumentation
Summary(pl.UTF-8):	Przyrządy pomiarowe NFSv4 dla SBLIM CMPI
Name:		sblim-cmpi-nfsv4
Version:	1.1.0
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	293b12060de9dc0470e645d14054d5a5
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI NFSv4 providers.

%description -l pl.UTF-8
Dostawcy informacji NFSv4 dla SBLIM CMPI.

%prep
%setup -q

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi \
	--disable-static

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.la
# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_NFSv4System{Configuration,Setting}.registration \
	-m %{_datadir}/%{name}/Linux_NFSv4System{Configuration,Setting}.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_NFSv4System{Configuration,Setting}.registration \
		-m %{_datadir}/%{name}/Linux_NFSv4System{Configuration,Setting}.mof >/dev/null
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README README.TEST
%attr(755,root,root) %{_libdir}/libLinux_NFSv4SystemConfigurationUtil.so
%attr(755,root,root) %{_libdir}/cmpi/libLinux_NFSv4SettingContext.so
%attr(755,root,root) %{_libdir}/cmpi/libLinux_NFSv4SystemConfiguration.so
%attr(755,root,root) %{_libdir}/cmpi/libLinux_NFSv4SystemSetting.so
%dir %{_datadir}/sblim-cmpi-nfsv4
%{_datadir}/sblim-cmpi-nfsv4/Linux_NFSv4SystemConfiguration.mof
%{_datadir}/sblim-cmpi-nfsv4/Linux_NFSv4SystemConfiguration.registration
%{_datadir}/sblim-cmpi-nfsv4/Linux_NFSv4SystemSetting.mof
%{_datadir}/sblim-cmpi-nfsv4/Linux_NFSv4SystemSetting.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-nfsv4/provider-register.sh
