# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

Name: playonlinux
Version: 4.3.4
Summary: Graphical front-end for Wine
License: GPLv3
URL: https://www.playonlinux.com
Release: 1%{?dist}
Source0: https://github.com/PlayOnLinux/POL-POM-4/archive/%{version}.tar.gz

# Wine supported on these arches
ExclusiveArch: %{arm} aarch64 %{ix86} x86_64

Requires: unzip
Requires: wine
Requires: wget
Requires: xterm
Requires: python2 > 2.4
Requires: wxPython
Requires: ImageMagick
Requires: cabextract
Requires: icoutils
Requires: p7zip-plugins
Requires: jq
BuildRequires:  gcc
BuildRequires: gzip
BuildRequires: mesa-libGL-devel
BuildRequires: python2 > 2.4
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libappstream-glib

%global BUILD_DIR %{buildroot}/%{_datadir}/%{name}

%description
New users can often find Wine to be intimidating and difficult to use.
PlayOnLinux simplifies much of this and makes installing and using
Windows programs easier.
PlayOnLinux has the database of Windows applications from which the user
can install desired application with a few clicks. It will automatically
setup your Wine prefix and download any required Windows libraries.

%prep
%autosetup -n POL-POM-4-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %make_build

%install
%make_install
%find_lang pol

sed -i '1{/^#!\//d}' %{BUILD_DIR}/python/setupwindow/gui_server.py \
                     %{BUILD_DIR}/tests/python/test_versionlower.py \
                     %{BUILD_DIR}/tests/bash/test-versionlower

grep -lZsr "#!/usr/bin/env python" %{BUILD_DIR}/python/ | xargs -0 -l sed -i -e "s%#\!/usr/bin/env python%#\!/usr/bin/env python2%"
grep -lZsr "#!/usr/bin/python" %{BUILD_DIR}/python/ | xargs -0 -l sed -i -e "s%#\!/usr/bin/python%#\!/usr/bin/python2%"

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/PlayOnLinux.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/PlayOnLinux.appdata.xml

%files -f pol.lang
%doc README.md
%license LICENCE doc/copyright
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}/
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/appdata/*
%{_libexecdir}/playonlinux-check_dd

%changelog
* Sun Jan 06 2019 Jiri Konecny <jkonecny@redhat.com> - 4.3.4-1
- Update to 4.3.4
- Update position of gui_server source code for sed

* Mon Dec 17 2018 Jiri Konecny <jkonecny@redhat.com> - 4.3.3-1
- Update to 4.3.3
- Fix python shebangs to python2
- Add new runtime dependency jq

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 4.2.12-1
- Update to 4.2.12 (#1463027)

* Wed May 31 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 4.2.11-1
- Update to 4.2.11 (#1457013)
- Remove patches contained in the new release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.10-10
- Define ExclusiveArch with arches wine supports

* Mon Oct 10 2016 Jiri Konecny <jkonecny@redhat.com> - 4.2.10-9
- Add patch to fix GUI layout issues on Wayland

* Sat Sep  3 2016 Jiri Konecny <jkonecny@redhat.com> - 4.2.10-8
- Add new patch for the updated appdata.xml file
- Improve old Patch2 for desktop file
- Rebase Patch6 and Patch7 on top of Patch2

* Wed Mar  9 2016 Jiri Konecny <jkonecny@redhat.com> - 4.2.10-7
- Apply patch which fixing bad icon path in a desktop file

* Sat Mar  5 2016 Ville Skyttä <ville.skytta@iki.fi> - 4.2.10-6
- Build with $RPM_OPT_FLAGS

* Fri Jan 22 2016 Jiri Konecny <jkonecny@redhat.com> 4.2.10-5
- Add patch which will fix installation of locales to the system

* Wed Jan 20 2016 Jiri Konecny <jkonecny@redhat.com> 4.2.10-4
- Change sed command to simpler and safer version
- Change appdata patches
- Fix installation of appdata
- Better description

* Wed Jan 13 2016 Jiri Konecny <jkonecny@redhat.com> 4.2.10-3
- Removed shebang and executable bit from scripts in /usr/share
- Change of summary and description
- Add 2 new patches which adding appdata.xml file
- Add new build requires for appstream-util check

* Thu Jan 7 2016 Jiri Konecny <jkonecny@redhat.com> 4.2.10-2
- Reworked patches for Makefile (Patch0, Patch1, Patch3 changed)
- Using make_install and make_build macros

* Mon Jan 4 2016 Jiri Konecny <jkonecny@redhat.com> 4.2.10-1
- New version 4.2.10
- Use more macros
- Add missing dependencies

* Thu Dec 10 2015 Jiri Konecny <jkonecny@redhat.com> 4.2.9-2
- Fixed missing lang files
- Remove exclude

* Wed Nov 11 2015 Jiri Konecny <jkonecny@redhat.com> 4.2.9-1
- Package creation

