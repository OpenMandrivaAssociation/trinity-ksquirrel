%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg ksquirrel

%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.8.0
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Powerful Trinity image viewer
Group:		Amusements/Games
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/graphics/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH=%{tde_prefix}/%{_lib}
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DCONFIG_INSTALL_DIR=%{_sysconfdir}/trinity
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	trinity-libkipi-devel
BuildRequires:	trinity-libksquirrel-devel

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

# MESA support
BuildRequires:  pkgconfig(glu)

BuildRequires:  pkgconfig(xrender)


%description
KSquirrel is an image viewer for TDE with disk navigator, file tree,
multiple directory view, thumbnails, extended thumbnails, dynamic
format support, DCOP interface, KEXIF and KIPI plugins support.

KSquirrel is a fast and convenient image viewer for TDE featuring
OpenGL and dynamic format support.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE LICENSE.GFDL LICENSE.LGPL README
%{tde_prefix}/bin/ksquirrel
%{tde_prefix}/bin/ksquirrel-libs-configurator
%{tde_prefix}/bin/ksquirrel-libs-configurator-real
%{tde_prefix}/%{_lib}/trinity/libksquirrelpart.la
%{tde_prefix}/%{_lib}/trinity/libksquirrelpart.so
%{tde_prefix}/share/applications/tde/ksquirrel.desktop
%dir %{tde_prefix}/share/apps/dolphin
%dir %{tde_prefix}/share/apps/dolphin/servicemenus
%{tde_prefix}/share/apps/dolphin/servicemenus/dolphksquirrel-dir.desktop
%{tde_prefix}/share/apps/konqueror/servicemenus/konqksquirrel-dir.desktop
%{tde_prefix}/share/apps/ksquirrel/
%{tde_prefix}/share/apps/ksquirrelpart/
%{tde_prefix}/share/doc/tde/HTML/*/ksquirrel
%{tde_prefix}/share/icons/hicolor/*/apps/ksquirrel.png
%{tde_prefix}/share/mimelnk/image/*.desktop
%{tde_prefix}/share/services/ksquirrelpart.desktop
%{tde_prefix}/share/man/man1/ksquirrel.1
%{tde_prefix}/share/man/man1/ksquirrel-libs-configurator.1*

