#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
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

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.8.0
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Powerful Trinity image viewer
Group:		Amusements/Games
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/graphics/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	trinity-libkipi-devel
BuildRequires:	trinity-libksquirrel-devel

BuildRequires:	autoconf automake libtool m4
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# MESA support
BuildRequires:  pkgconfig(glu)

BuildRequires:  pkgconfig(xrender)


%description
KSquirrel is an image viewer for TDE with disk navigator, file tree,
multiple directory view, thumbnails, extended thumbnails, dynamic
format support, DCOP interface, KEXIF and KIPI plugins support.

KSquirrel is a fast and convenient image viewer for TDE featuring
OpenGL and dynamic format support.


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

# Warning: GCC visibility causes FTBFS [Bug #1285]
%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DCONFIG_INSTALL_DIR="%{tde_confdir}" \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

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

