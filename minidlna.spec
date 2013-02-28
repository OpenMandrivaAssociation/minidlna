Summary:	A DLNA/UPnP-AV compliant media server
Name:		minidlna
Version:	1.0.25
Release:	3
URL:		http://sourceforge.net/projects/minidlna/
Group:		Networking/Other
License:	GPLv2
Source0:	http://downloads.sourceforge.net/project/minidlna/minidlna/%{version}/minidlna_%{version}_src.tar.gz
Source2:	minidlna-tmpfiles.conf
Source3:	minidlna.1
Source4:	minidlna.conf.5
Source5:	%{name}.service
# Local patches
# Selected patches from development tree
#Patch100:
# Selected patches from upstream patch tracker
#Patch200:
Patch0:		minidlna-1.0.25-ffmpeg10.patch
BuildRequires:	pkgconfig(flac)
BuildRequires:	libid3tag-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	ffmpeg-devel >= 1.1
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	systemd-units
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being fully
compliant with DLNA/UPnP-AV clients. MiniDLNA serves multimedia content
such as music, video and pictures to compatible clients on the network.

See http://www.upnp.org/ for more details on UPnP
and http://www.dlna.org/ for mode details on DLNA.

%prep
%setup -q
%patch0 -p1

./genconfig.sh
sed -i -e 's!^\(#define OS_NAME\).*!\1 "%{product_vendor}"!
	s!^\(#define OS_VERSION\).*!\1 "%{product_version}"!
	s!^\(#define OS_URL\).*!\1 "http://www.mandriva.com/"!
	s!^\(#define DEFAULT_DB_PATH\).*!\1 "/var/cache/%{name}"!
	s!^\(#define DEFAULT_LOG_PATH\).*!\1 "/var/log"!' config.h


%build
%serverbuild
%setup_compile_flags

#(tpg) obey %optflags
sed -i 's/CFLAGS = -Wall -g -O3/CFLAGS +=/' Makefile

#(tpg) verbose make
sed -i 's/@$(CC)/$(CC)/' Makefile

%make

%install
%makeinstall_std

install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 -D minidlna.conf %{buildroot}%{_sysconfdir}/minidlna.conf
install -m 644 -D %{SOURCE3} %{buildroot}%{_mandir}/man1/minidlna.1
install -m 644 -D %{SOURCE4} %{buildroot}%{_mandir}/man5/minidlna.conf.5

mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

%post
%_post_service minidlna
systemd-tmpfiles --create minidlna.conf

%preun
%_preun_service minidlna

%files
%doc README
%attr(755,-,-) %{_sbindir}/minidlna
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/minidlna.conf
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_mandir}/man1/minidlna.1*
%{_mandir}/man5/minidlna.conf.5*
