#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Call audio routing daemon
Summary(pl.UTF-8):	Demon przekierowujący dźwięk w trakcie połączeń
Name:		callaudiod
Version:	0.1.0
Release:	1
License:	GPL v3+ (daemon), LGPL v2.1+ (library)
Group:		Daemons
#Source0Download: https://gitlab.com/mobian1/callaudiod/-/tags
Source0:	https://gitlab.com/mobian1/callaudiod/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	cf45959ced1812e4e837ecd74fd93f08
URL:		https://gitlab.com/mobian1/callaudiod
BuildRequires:	alsa-lib-devel
BuildRequires:	glib2-devel >= 2.0
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	pulseaudio-devel
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
Requires:	libcallaudio = %{version}-%{release}
Requires:	pulseaudio
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
callaudiod is a daemon for dealing with audio routing during phone
calls.

It provides a D-Bus interface allowing other programs to:
- switch audio profiles
- output audio to the speaker or back to its original port
- mute the microphone

%description -l pl.UTF-8
callaudiod to demon przekierowujący dźwięk w trakcie połączeń
telefonicznych.

Udostępnia interfejs D-Bus, pozwalający innym programom:
- przełączać profile dźwiękowe
- kierować wyjście dźwięku na głośnik lub z powrotem na oryginalny
  port
- wyciszać mikrofon

%package -n libcallaudio
Summary:	CallAudio library
Summary(pl.UTF-8):	Biblioteka CallAudio
Group:		Libraries
Suggests:	%{name} = %{version}-%{release}

%description -n libcallaudio
CallAudio library.

%description -n libcallaudio -l pl.UTF-8
Biblioteka CallAudio.

%package -n libcallaudio-devel
Summary:	Header files for CallAudio library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CallAudio
Group:		Development/Libraries
Requires:	libcallaudio = %{version}-%{release}
Requires:	glib2-devel >= 2.0

%description -n libcallaudio-devel
Header files for CallAudio library.

%description -n libcallaudio-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CallAudio.

%package -n libcallaudio-apidocs
Summary:	API documentation for CallAudio library
Summary(pl.UTF-8):	Dokumentacja API biblioteki CallAudio
Group:		Documentation
BuildArch:	noarch

%description -n libcallaudio-apidocs
API documentation for CallAudio library.

%description -n libcallaudio-apidocs -l pl.UTF-8
Dokumentacja API biblioteki CallAudio.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libcallaudio -p /sbin/ldconfig
%postun	-n libcallaudio -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/callaudiocli
%attr(755,root,root) %{_bindir}/callaudiod
%{_datadir}/dbus-1/services/org.mobian_project.CallAudio.service

%files -n libcallaudio
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcallaudio-0.1.so.0
%{_datadir}/dbus-1/interfaces/org.mobian_project.CallAudio.xml

%files -n libcallaudio-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcallaudio-0.1.so
%{_includedir}/libcallaudio-0.1
%{_pkgconfigdir}/libcallaudio-0.1.pc

%if %{with apidocs}
%files -n libcallaudio-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libcallaudio
%endif
