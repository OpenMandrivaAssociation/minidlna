Name: minidlna
Version: 1.0.18.2
Release: %mkrel 2
Summary: A DLNA/UPnP-AV compliant media server
URL: http://sourceforge.net/projects/minidlna/
Group: Networking/Other
License: GPL
Source: minidlna_1.0.18_src.tar.gz
Source1: initscript
Source2: minidlna.conf
Source3: minidlna.1
Source4: minidlna.conf.5
# Local patches
Patch1: minidlna-fix-log-path.patch
# Selected patches from development tree
Patch101: 0008-Make-Xbox360-support-more-generic-for-use-with-other.patch
Patch102: 0009-Fix-a-few-typos.patch
Patch103: 0010-Remove-the-last-remnants-of-hard-coded-ObjectIDs.patch
Patch104: 0013-Fix-Xbox360-video-thumbnail-bug-introduced-in-the-la.patch
Patch106: 0015-Fall-back-to-regular-read-write-if-sendfile-fails.patch
Patch107: 0016-Fix-big-endian-issue-with-XING-header-parsing.patch
Patch108: 0017-Handle-libavformat-format-name-matroska-webm.patch
Patch109: 0020-Bump-to-v1.0.18.2.patch
Patch110: 0022-Fix-bug-in-zero-MAC-detection-so-UUIDs-are-actually-.patch
Patch111: 0026-Add-Sony-BDP-S370-MKV-support-by-pretending-they-re-.patch
Patch112: 0027-Sony-SMP-100-needs-the-same-treatment-as-their-BDP-S.patch
Patch113: 0029-Handle-the-mpegvideo-format-name.patch
Patch114: 0030-Current-model-Samsung-TVs-have-a-neat-little-bug-whe.patch
Patch115: 0036-Try-to-trick-Sony-Blu-ray-home-theater-systems-into-.patch
Patch116: 0038-Fall-back-to-regular-I-O-instead-of-using-sendfile-i.patch
Patch117: 0041-Cheat-to-make-Sony-Bravia-AVC-support-work.patch
# Selected patches from upstream patch tracker
#Patch200: minidlna.samsung-new.patch
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
%setup -q -n %{name}
%patch1 -p1 -b .fix-log-path
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
#%patch200 -p1

./genconfig.sh
sed -i -e 's!^\(#define OS_NAME\).*!\1 "%{product_vendor}"!
	s!^\(#define OS_VERSION\).*!\1 "%{product_version}"!
	s!^\(#define OS_URL\).*!\1 "http://www.mandriva.com/"!
	s!^\(#define DEFAULT_DB_PATH\).*!\1 "/var/cache/%{name}"!' config.h

%build
%make

%install
rm -rf %{buildroot}
install -m 755 -D %{_sourcedir}/initscript %{buildroot}%{_initrddir}/minidlna
install -m 644 -D %{_sourcedir}/minidlna.conf \
  %{buildroot}%{_sysconfdir}/minidlna.conf
install -m 755 -D minidlna %{buildroot}%{_sbindir}/minidlna
install -m 644 -D minidlna.1 %{buildroot}%{mandir}/man1/minidlna.1
install -m 644 -D minidlna.conf.5 %{buildroot}%{mandir}/man5/minidlna.conf.5

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
