%define name 	 hugin
%define version  0.7
%define beta     beta4
%define release  %mkrel 0.%{beta}.1


Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:    Panorama Tools GUI
License: 	GPL
Group: 		Graphics
Url: 		http://hugin.sourceforge.net
Source0: 	http://downloads.sourceforge.net/hugin/%{name}-%{version}_%{beta}.tar.bz2
Patch0:		hugin-0.5-defconfig.patch.bz2
Source11: 	%{name}.16.png
Source12: 	%{name}.32.png
Source13: 	%{name}.48.png
Requires:	pano12
Requires:       enblend
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires: 	libboost-devel
BuildRequires: 	pano12-devel >= 2.8.1
BuildRequires: 	fftw2-devel
BuildRequires: 	libwxgtku-devel > 2.5
BuildRequires:	zlib-devel 
BuildRequires:	libtiff-devel
BuildRequires:	libjpeg-devel
BuildRequires: 	libpng-devel
BuildRequires:	zip
BuildRequires: desktop-file-utils
BuildRoot: 	%{_tmppath}/%{name}-%{version}

%description
Hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. 

%prep 
%setup -q -n %{name}-%{version}_%{beta}
#%patch0 

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

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-CrossDesktop;" \
  --add-category="Photography" \
  --add-category="Graphics" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

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
%{_mandir}/man?/*
%{_datadir}/applications/hugin.desktop
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-ptoptimizer-script.png
%{_datadir}/mime/packages/hugin.xml
%{_datadir}/pixmaps/hugin.png

