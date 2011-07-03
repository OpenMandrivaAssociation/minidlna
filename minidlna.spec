Name: minidlna
Version: 1.0.20
Release: %mkrel 1
Summary: A DLNA/UPnP-AV compliant media server
URL: http://sourceforge.net/projects/minidlna/
Group: Networking/Other
License: GPL
Source: minidlna_%{version}_src.tar.gz
Source1: initscript
Source2: minidlna.conf
Source3: minidlna.1
Source4: minidlna.conf.5
# Local patches
# Selected patches from development tree
#Patch100:
# Selected patches from upstream patch tracker
#Patch200:
BuildRequires: libflac-devel libid3tag-devel libexif-devel libjpeg-devel
BuildRequires: libsqlite3-devel libffmpeg-devel libvorbis-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being fully
compliant with DLNA/UPnP-AV clients. MiniDLNA serves multimedia content
such as music, video and pictures to compatible clients on the network.

See http://www.upnp.org/ for more details on UPnP
and http://www.dlna.org/ for mode details on DLNA.

%prep
%setup -q

./genconfig.sh
sed -i -e 's!^\(#define OS_NAME\).*!\1 "%{product_vendor}"!
	s!^\(#define OS_VERSION\).*!\1 "%{product_version}"!
	s!^\(#define OS_URL\).*!\1 "http://www.mandriva.com/"!
	s!^\(#define DEFAULT_DB_PATH\).*!\1 "/var/cache/%{name}"!
	s!^\(#define DEFAULT_LOG_PATH\).*!\1 "/var/log"!' config.h

%build
%make

%install
rm -rf %{buildroot}
install -m 755 -D %{_sourcedir}/initscript %{buildroot}%{_initrddir}/minidlna
install -m 644 -D %{_sourcedir}/minidlna.conf \
  %{buildroot}%{_sysconfdir}/minidlna.conf
install -m 755 -D minidlna %{buildroot}%{_sbindir}/minidlna
install -m 644 -D %{_sourcedir}/minidlna.1 \
  %{buildroot}%{_mandir}/man1/minidlna.1
install -m 644 -D %{_sourcedir}/minidlna.conf.5 \
  %{buildroot}%{_mandir}/man5/minidlna.conf.5

%clean
rm -rf %{buildroot}

%post
%_post_service minidlna

%preun
%_preun_service minidlna

%files
%defattr(0644,root,root,0755)
%doc README
%attr(755,-,-) %{_sbindir}/minidlna
%attr(755,-,-) %{_initrddir}/minidlna
%config(noreplace) %{_sysconfdir}/minidlna.conf
%{_mandir}/man1/minidlna.1*
%{_mandir}/man5/minidlna.conf.5*
