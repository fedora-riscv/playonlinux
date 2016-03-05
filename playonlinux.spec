Name: playonlinux
Version: 4.2.10
Summary: Graphical front-end for Wine
License: GPLv3
URL: https://www.playonlinux.com
Release: 6%{?dist}
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
BuildRequires: gzip
BuildRequires: mesa-libGL-devel
BuildRequires: python2 > 2.4
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libappstream-glib
Source0: https://github.com/PlayOnLinux/POL-POM-4/archive/%{version}.tar.gz

# Add documentation to playonlinux
# Add Makefile to build and install playonlinux
# https://github.com/PlayOnLinux/POL-POM-4/pull/33
Patch0: 0001-Add-Makefile-to-build-and-install-playonlinux.patch
# Change check_gl to use compiled version of check dd
# https://github.com/PlayOnLinux/POL-POM-4/pull/33
Patch1: 0002-Change-check_gl-to-use-compiled-version-of-check_dd.patch
# Updated desktop file for the new format
# https://github.com/PlayOnLinux/POL-POM-4/pull/35
Patch2: 0003-Updated-desktop-file-for-the-new-format.patch
# Move build check_dd to /usr/libexec as says FHS
# https://github.com/PlayOnLinux/POL-POM-4/pull/33
Patch3: 0004-Move-build-check_dd-to-usr-libexec-as-says-FHS.patch
# Add appdata.xml which is used for software center
# https://github.com/PlayOnLinux/POL-POM-4/pull/36
Patch4: 0005-Add-appdata.xml.patch
# Change Makefile to use appdata.xml
# https://github.com/PlayOnLinux/POL-POM-4/pull/36
Patch5: 0006-Change-Makefile-to-install-appdata.xml-file.patch
# Install lang files correctly to the system
# https://github.com/PlayOnLinux/POL-POM-4/pull/37
Patch6: 0007-Install-lang-files-correctly.patch

%global BUILD_DIR %{buildroot}/%{_datadir}/%{name}

%description
New users can often find Wine to be intimidating and difficult to use.
PlayOnLinux simplifies much of this and makes installing and using
Windows programs easier.
PlayOnLinux has the database of Windows applications from which the user
can install desired application with a few clicks. It will automatically
setup your Wine prefix and download any required Windows libraries.

%prep
%autosetup -n POL-POM-4-%{version} -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %make_build

%install
%make_install
%find_lang pol

sed -i '1{/^#!\//d}' %{BUILD_DIR}/python/gui_server.py \
          %{BUILD_DIR}/tests/python/test_versionlower.py \
          %{BUILD_DIR}/tests/bash/test-versionlower

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

