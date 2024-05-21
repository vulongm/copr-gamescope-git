# Based on https://src.fedoraproject.org/rpms/libliftoff

%global debug_package %{nil}
%global commit c5f0ff73e452ab6297ad03d27c67949a0460abd9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20240516

Name:           libliftoff
Version:        0.5.0^%{git_date}.git%{shortcommit}
Release:        %autorelease
Summary:        Lightweight KMS plane library

License:        MIT
URL:            https://gitlab.freedesktop.org/emersion/libliftoff
Source0:        %{url}/-/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  meson >= 0.52.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(libdrm)

%description
libliftoff eases the use of KMS planes from userspace without
standing in your way. Users create "virtual planes" called
layers, set KMS properties on them, and libliftoff will
allocate planes for these layers if possible.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/*.so.0*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
%autochangelog
