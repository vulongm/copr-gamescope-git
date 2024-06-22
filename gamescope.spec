# Based on https://src.fedoraproject.org/rpms/gamescope

%global commit 3b69847e15c84c0a4f93e82c2eb16b623f9765b9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20240622
%global tag 3.14.22
%global ver_count 2
%global libliftoff_minver 0.4.1

Name:           gamescope
Version:        %{tag}
Release:        %{git_date}.%{ver_count}.%{shortcommit}%{?dist}
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ValveSoftware/gamescope

# Create stb.pc to satisfy dependency('stb')
Source0:        stb.pc

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXcursor-devel
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libavif)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  spirv-headers-devel
# Enforce the the minimum EVR to contain fixes for all of:
# CVE-2021-28021 CVE-2021-42715 CVE-2021-42716 CVE-2022-28041 CVE-2023-43898
# CVE-2023-45661 CVE-2023-45662 CVE-2023-45663 CVE-2023-45664 CVE-2023-45666
# CVE-2023-45667
BuildRequires:  stb_image-devel >= 2.28^20231011gitbeebb24-12
# Header-only library: -static is for tracking per guidelines
BuildRequires:  stb_image-static
BuildRequires:  stb_image_resize-devel
BuildRequires:  stb_image_resize-static
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_write-static
BuildRequires:  /usr/bin/glslangValidator

# libliftoff hasn't bumped soname, but API/ABI has changed for 0.2.0 release
Requires:       libliftoff%{?_isa} >= %{libliftoff_minver}
Requires:       xorg-x11-server-Xwayland
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

# gamescope copr added deps
BuildRequires:  git
BuildRequires:  libeis-devel
BuildRequires:  libdecor-devel

# submodule deps
BuildRequires:  pkgconfig(libinput) >= 1.21.0
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) >= 0.42.0
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xwayland)

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%prep
git clone %{URL}
cd gamescope
git checkout %{commit}
git submodule update --init --recursive

# Install stub pkgconfig file
mkdir -p pkgconfig	
cp %{SOURCE0} pkgconfig/stb.pc

# Replace spirv-headers include with the system directory
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

%autopatch -p1

%if 0%{?fedora} == 39
  %define avif_screenshots disabled
%else
  %define avif_screenshots enabled
%endif

%build
cd gamescope
export PKG_CONFIG_PATH=pkgconfig
%meson -Dpipewire=enabled -Davif_screenshots=%{avif_screenshots}
%meson_build

%install
cd gamescope
%meson_install --skip-subprojects

%files
%license gamescope/LICENSE
%doc gamescope/README.md
%caps(cap_sys_nice=eip) %{_bindir}/gamescope
%{_bindir}/gamescopestream
%{_bindir}/gamescopectl
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json

%changelog
%autochangelog
