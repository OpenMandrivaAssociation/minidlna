%define _disable_rebuild_configure 1

Summary:	A DLNA/UPnP-AV compliant media server
Name:		minidlna
Version:	1.3.0
Release:	4
URL:		http://sourceforge.net/projects/minidlna/
Group:		Networking/Other
License:	GPLv2
Source0:	http://downloads.sourceforge.net/project/minidlna/minidlna/%{version}/minidlna-%{version}.tar.gz
Source1:	%{name}.sysusers
Source2:	%{name}.tmpfiles
Source3:	%{name}.service
Patch0:		minidlna-rundir.patch
Patch1:		https://gitweb.gentoo.org/repo/gentoo.git/plain/net-misc/minidlna/files/minidlna-1.3.0-fd-leak.patch
Patch2:		https://gitweb.gentoo.org/repo/gentoo.git/plain/net-misc/minidlna/files/minidlna-1.3.0-fno-common.patch
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	systemd-rpm-macros
%systemd_requires
Requires(pre):	systemd

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being fully
compliant with DLNA/UPnP-AV clients. MiniDLNA serves multimedia content
such as music, video and pictures to compatible clients on the network.

See http://www.upnp.org/ for more details on UPnP
and http://www.dlna.org/ for mode details on DLNA.

%prep
%autosetup -p1
sed -i 's|#user=.*|user=minidlna|g' minidlna.conf

%build
%serverbuild

export ac_cv_lib_id3tag__lz___id3_file_open=yes
%configure \
	--with-log-path=%{_logdir} \
	--with-db-path=%{_localstatedir}/cache \
	--with-os-name="%{distribution}"\
	--with-os-version="%{distro_release}" \
	--with-os-url="%{disturl}"

%make_build

%install
%make_install


install -D -p -m 0644 %{name}.conf %{buildroot}%{_sysconfdir}/minidlna.conf
install -D -p -m 0644 minidlna.conf.5 %{buildroot}%{_mandir}/man5/%{name}.conf.5
install -D -p -m 0644 minidlnad.8 %{buildroot}%{_mandir}/man8/%{name}d.8
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service

install -d -m 0755 %{buildroot}%{_localstatedir}/cache/%{name}/
touch %{buildroot}%{_localstatedir}/cache/%{name}/files.db

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-minidlna.preset << EOF
enable minidlna.service
EOF

%find_lang %{name}

%pre
%sysusers_create_package %{name} %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files -f %{name}.lang
%doc README
%dir %attr(-,minidlna,minidlna) %{_localstatedir}/cache/%{name}/
%ghost %attr(-,minidlna,minidlna) %{_localstatedir}/cache/%{name}/files.db
%attr(755,-,-) %{_sbindir}/minidlna*
%{_presetdir}/86-minidlna.preset
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/minidlna.conf
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%doc %{_mandir}/man?/%{name}*
