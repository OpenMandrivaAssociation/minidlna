Summary:	A DLNA/UPnP-AV compliant media server
Name:		minidlna
Version:	1.2.1
Release:	3
URL:		http://sourceforge.net/projects/minidlna/
Group:		Networking/Other
License:	GPLv2
Source0:	http://downloads.sourceforge.net/project/minidlna/minidlna/%{version}/minidlna-%{version}.tar.gz
Source2:	minidlna-tmpfiles.conf
Source3:	minidlna.1
Source4:	minidlna.conf.5
Source5:	%{name}.service
Patch0:		01-run-instead-of-var-run.patch
Patch2:		03-make-sure-the-database-is-closed-after-scanning.patch
Patch3:		10-db_dir-should-not-affect-log_dir.patch
Patch4:		07-fix-multi-artist-album-handling.patch
Patch5:		02-use-USER-instead-of-LOGNAME.patch
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
Requires(postun):	rpm-helper

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being fully
compliant with DLNA/UPnP-AV clients. MiniDLNA serves multimedia content
such as music, video and pictures to compatible clients on the network.

See http://www.upnp.org/ for more details on UPnP
and http://www.dlna.org/ for mode details on DLNA.

%prep
%setup -q
%apply_patches

%build
%serverbuild

%configure \
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

install -d -m 0755 %{buildroot}%{_localstatedir}/cache/%{name}/
touch %{buildroot}%{_localstatedir}/cache/%{name}/files.db

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-minidlna.preset << EOF
enable minidlna.service
EOF

%find_lang %{name}

%pre
%_pre_useradd %{name} /run/%{name} /sbin/nologin
%_pre_groupadd minidlna minidlna

%post
%create_ghostfile %{_localstatedir}/cache/%{name}/files.db %{name} %{name} 0644

%postun
%_postun_userdel minidlna
%_postun_groupdel minidlna minidlna

%files -f %{name}.lang
%doc README
%dir %attr(-,minidlna,minidlna) %{_localstatedir}/cache/%{name}/
%ghost %attr(-,minidlna,minidlna) %{_localstatedir}/cache/%{name}/files.db
%attr(755,-,-) %{_sbindir}/minidlna*
%{_presetdir}/86-minidlna.preset
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/minidlna.conf
%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_mandir}/man1/minidlna.1*
%{_mandir}/man5/minidlna.conf.5*
