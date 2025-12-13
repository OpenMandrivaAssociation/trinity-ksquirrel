%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg ksquirrel
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

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

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/graphics/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH="%{tde_libdir}"
BuildOption:    -DCMAKE_NO_BUILTIN_CHRPATH=ON
BuildOption:    -DBIN_INSTALL_DIR=%{tde_bindir}
BuildOption:    -DCONFIG_INSTALL_DIR="%{tde_confdir}"
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir}
BuildOption:    -DLIB_INSTALL_DIR=%{tde_libdir}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_datadir}
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON

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
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"


%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE LICENSE.GFDL LICENSE.LGPL README
%{tde_bindir}/ksquirrel
%{tde_bindir}/ksquirrel-libs-configurator
%{tde_bindir}/ksquirrel-libs-configurator-real
%{tde_tdelibdir}/libksquirrelpart.la
%{tde_tdelibdir}/libksquirrelpart.so
%{tde_tdeappdir}/ksquirrel.desktop
%dir %{tde_datadir}/apps/dolphin
%dir %{tde_datadir}/apps/dolphin/servicemenus
%{tde_datadir}/apps/dolphin/servicemenus/dolphksquirrel-dir.desktop
%{tde_datadir}/apps/konqueror/servicemenus/konqksquirrel-dir.desktop
%{tde_datadir}/apps/ksquirrel/
%{tde_datadir}/apps/ksquirrelpart/
%{tde_tdedocdir}/HTML/*/ksquirrel
%{tde_datadir}/icons/hicolor/*/apps/ksquirrel.png
%{tde_datadir}/mimelnk/image/*.desktop
%{tde_datadir}/services/ksquirrelpart.desktop
%{tde_mandir}/man1/ksquirrel.1
%{tde_mandir}/man1/ksquirrel-libs-configurator.1*

