Summary:	A DLNA/UPnP-AV compliant media server
Name:		minidlna
Version:	1.1.1
Release:	2
URL:		http://sourceforge.net/projects/minidlna/
Group:		Networking/Other
License:	GPLv2
Source0:	http://downloads.sourceforge.net/project/minidlna/minidlna/%{version}/minidlna-%{version}.tar.gz
Source2:	minidlna-tmpfiles.conf
Source3:	minidlna.1
Source4:	minidlna.conf.5
Source5:	%{name}.service
BuildRequires:	pkgconfig(flac)
BuildRequires:	libid3tag-devel
BuildRequires:	libexif-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	ffmpeg-devel >= 1.1
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	systemd
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

%build
%serverbuild

%configure2_5x \
	--with-log-path=%{_logdir} \
	--with-db-path=%{_localstatedir}/cache \
	--with-os-name="%{distribution}"\
	--with-os-version="%{distro_release}" \
	--with-os-url="%{disturl}"

%make

%install
%makeinstall_std

install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 -D minidlna.conf %{buildroot}%{_sysconfdir}/minidlna.conf
install -m 644 -D %{SOURCE3} %{buildroot}%{_mandir}/man1/minidlna.1
install -m 644 -D %{SOURCE4} %{buildroot}%{_mandir}/man5/minidlna.conf.5

mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

%find_lang %{name}

%pre
%_pre_useradd minidlna %{_var}/run/%{name} /bin/false
%_pre_groupadd minidlna minidlna

%post
%_post_service minidlna
%tmpfiles_create %{name}.conf

%preun
%_preun_service minidlna

%postun
%_postun_userdel minidlna
%_postun_groupdel minidlna minidlna

%files -f %{name}.lang
%doc README
%attr(755,-,-) %{_sbindir}/minidlna*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/minidlna.conf
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_mandir}/man1/minidlna.1*
%{_mandir}/man5/minidlna.conf.5*
