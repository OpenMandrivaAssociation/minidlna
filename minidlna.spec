%if "%{_unitdir}" == "%%{unitdir}"
%define %{_unitdir} /lib/systemd/system
%endif

Summary:	A DLNA/UPnP-AV compliant media server
Name:		minidlna
Version:	1.0.23
Release:	%mkrel 2
URL:		http://sourceforge.net/projects/minidlna/
Group:		Networking/Other
License:	GPL
Source0:	minidlna_%{version}_src.tar.gz
Source1:	initscript
Source2:	minidlna.conf
Source3:	minidlna.1
Source4:	minidlna.conf.5
Source5:	%{name}.service
# Local patches
# Selected patches from development tree
#Patch100:
# Selected patches from upstream patch tracker
#Patch200:
BuildRequires:	libflac-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	sqlite3-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	systemd-units
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
%serverbuild
%setup_compile_flags

#(tpg) obey %optflags
sed -i 's/CFLAGS = -Wall -g -O3/CFLAGS +=/' Makefile

#(tpg) verbose make
sed -i 's/@$(CC)/$(CC)/' Makefile

%make

%install
rm -rf %{buildroot}
%if %mdkver >= 201100
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}.service
%else
install -m 755 -D %{SOURCE1} %{buildroot}%{_initrddir}/minidlna
%endif
install -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/minidlna.conf
install -m 755 -D minidlna %{buildroot}%{_sbindir}/minidlna
install -m 644 -D %{SOURCE3} %{buildroot}%{_mandir}/man1/minidlna.1
install -m 644 -D %{SOURCE4} %{buildroot}%{_mandir}/man5/minidlna.conf.5

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
%if %mdkver >= 201100
%{_unitdir}/%{name}.service
%else
%attr(755,-,-) %{_initrddir}/minidlna
%endif
%config(noreplace) %{_sysconfdir}/minidlna.conf
%{_mandir}/man1/minidlna.1*
%{_mandir}/man5/minidlna.conf.5*
