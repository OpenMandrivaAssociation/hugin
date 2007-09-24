%define name 	 hugin
%define version  0.6.1
%define release  %mkrel 2
%define summary  Hugin - Panorama Tools GUI


Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:        %{summary}
Source0: 	%{name}-%version.tar.bz2
Patch0:		hugin-0.5-defconfig.patch.bz2
Source11: 	%{name}.16.png
Source12: 	%{name}.32.png
Source13: 	%{name}.48.png
License: 	GPL
Group: 		Graphics
Url: 		http://hugin.sourceforge.net
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	libboost-devel
BuildRequires: 	pano12-devel >= 2.8.1
BuildRequires: 	fftw2-devel
BuildRequires: 	libwxgtku-devel > 2.5
BuildRequires:	zlib-devel 
BuildRequires:	libtiff-devel
BuildRequires:	libjpeg-devel
BuildRequires: 	libpng-devel
BuildRequires:	zip

Requires:	pano12
Requires:       enblend
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils



%description
Hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. 

%prep 
%setup -q -n %{name}-%version
%patch0 

%build
touch m4/Makefile.in

#ln -s %{_libdir}/wx/config/multiarch-%_arch-linux/gtk2-ansi-release-2.6 ./wx-config

# work-around broken wxGTK2.6 package
ln -s %{_bindir}/wxrc-2.6-unicode ./wxrc
export PATH=`pwd`:$PATH

%configure2_5x --disable-rpath --disable-static --with-wx-config=wx-config-unicode --with-unicode=yes

%make

%install
rm -rf %buildroot

%makeinstall_std
%find_lang %name
%find_lang nona_gui
cat nona_gui.lang >> %name.lang

perl -pi -e "s|\r\n|\n|" %buildroot%{_datadir}/%name/xrc/data/*.xpm

# Menu icons
install -m644 %{SOURCE11} -D %buildroot%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %buildroot%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %buildroot%{_liconsdir}/%{name}.png

# menu entries
mkdir -p  %buildroot%{_menudir}
cat << EOF > %buildroot%{_menudir}/%{name}
?package(hugin):command="/usr/bin/hugin" \
icon="hugin.png" needs="X11" \
section="Multimedia/Graphics" startup_notify="false" \
title="Hugin" longtitle="A panorama tools GUI " \
mimetypes="" accept_url="false" \
multiple_files="false" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Graphics" \
  --add-category="Photography" \
  --add-category="Graphics" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%clean 
rm -rf %buildroot

%post
%{update_menus} 
%{update_desktop_database}

%postun 
%{clean_menus} 
%{clean_desktop_database}

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS BUGS LICENCE README TODO
%{_bindir}/*
%{_datadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
%{_mandir}/man?/*
%{_datadir}/applications/hugin.desktop
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-ptoptimizer-script.png
%{_datadir}/mime/packages/hugin.xml
%{_datadir}/pixmaps/hugin.png

