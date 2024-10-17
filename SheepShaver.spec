%define name		SheepShaver
%define version		2.3
%define release		%mkrel 0.%{cvsdate}.2
%define cvsdate		20051130
%define mon_active	1
%define mon_version	3.0
%define mon_snapshot	20030206

# Extract Mandriva Linux name
%if %{mdkversion} >= 1010
%define mdk_distro_file	/etc/release
%else
%define mdk_distro_file	/etc/mandrake-release
%endif
%define mdk_distro	%(perl -ne '/^([.\\w\\s]+) release/ and print $1' < %{mdk_distro_file})

Summary:	An Open Source PowerMac emulator
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}%{?cvsdate:-%{cvsdate}}.tar.bz2
Source1:	SheepShaver-icons.tar.bz2
Source2:	cxmon-%{mon_version}-%{mon_snapshot}.tar.bz2
Patch0:		SheepShaver-2.2-stats.patch.bz2
URL:		https://sheepshaver.gibix.net/
License:	GPL
Group:		Emulators
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libgtk+2.0-devel, esound-devel >= 0.2.8
# Other arches need an instruction skipper on well-known invalid
# memory references (e.g. illegal writes to ROM).
ExclusiveArch:	ppc %{ix86} amd64 x86_64

%description
SheepShaver is a MacOS run-time environment for BeOS and Linux that
allows you to run classic MacOS applications inside the Linux
multitasking environment. This means that both Linux and MacOS
applications can run at the same time (usually in a window on the
Linux desktop).

If you are using a PowerPC-based system, applications will run at
native speed (i.e. with no emulation involved). There is also a
built-in PowerPC G4 emulator, without MMU support, for non-PowerPC
systems.

Some features of SheepShaver:
  - SheepShaver runs MacOS 7.5.2 thru MacOS 9.0.4
  - Copy and paste text between MacOS and the host OS (X11 clipboard)
  - File exchange with the host OS via a "Unix" icon on the Mac desktop
  - Color video display with support for run-time resolution switching
  - Run-time depth switching from 1 bpp to current host depth settings
  - Native QuickDraw acceleration for BitBlt and FillRect operations
  - CD-quality stereo sound output
  - Networking: SheepShaver supports Internet and LAN networking via
    Ethernet and PPP with all Open Transport compatible MacOS
    applications (on 32-bit big endian systems at this time)

%prep
%setup -q -a 1 -a 2
%patch0 -p1 -b .stats
perl -pi -e 's/^The XFree86 Project, Inc$/%{mdk_distro}/' src/Unix/keycodes

%build
cd ./src/Unix
%if %{mon_active}
WithMon="--with-mon=../../cxmon-%{mon_version}/src"
%endif
# force the use of gcc, not the icecream wrapper which doesn't handle
# input from stdin (that caused JIT to not be enabled)
%configure2_5x $WithMon --with-dgcc=%{_bindir}/gcc
# FIXME: grrr, what's up?
perl -pi -e 's,-m(cpu|tune)=pentiumpro,,g' Makefile
make obj
%make SheepShaver

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
%makeinstall -C src/Unix

# install icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
install -m 644 icons/SheepShaver.png $RPM_BUILD_ROOT%{_iconsdir}/
install -m 644 icons/mini/SheepShaver.png $RPM_BUILD_ROOT%{_miconsdir}/
install -m 644 icons/large/SheepShaver.png $RPM_BUILD_ROOT%{_liconsdir}/

# MDK menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Name=SheepShaver
Categories=Emulator;
Icon=%{name}
Comment=A MacOS run-time environment
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING NEWS doc/Linux
%{_bindir}/SheepShaver
%{_mandir}/man1/SheepShaver.1*
%{_datadir}/applications/mandriva-SheepShaver.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/keycodes
%{_datadir}/%{name}/tunconfig
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

