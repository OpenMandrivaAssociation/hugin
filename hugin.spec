Summary:	Panorama Tools GUI
Name: 		hugin
Version:	2009.2.0
Release:	%mkrel 5
License:	GPLv2+
Group:		Graphics
URL:		http://hugin.sourceforge.net
Source0:	http://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.gz
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Requires:	libpano13-tools >= 2.9.14
Requires:	enblend >= 3.1
Requires:	perl-Image-ExifTool
Requires:	make
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:  cmake
BuildRequires:  OpenEXR-devel
BuildRequires:  libexiv-devel
BuildRequires:  libboost-devel
BuildRequires:  pano13-devel >= 2.9.14
BuildRequires:  fftw2-devel
BuildRequires:  libwxgtku-devel > 2.7
BuildRequires:  zlib-devel 
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:	libglew-devel
BuildRequires:	mesaglut-devel
BuildRequires:  zip
BuildRequires:  desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. 

%prep 
%setup -q -n %{name}-%{version}

%define Werror_cflags %nil
%build
%cmake
%make

%install
rm -rf %buildroot
%makeinstall_std -C build
%find_lang %name %name nona_gui

perl -pi -e "s|\r\n|\n|" %buildroot%{_datadir}/%name/xrc/data/*.xpm

# unused symlinks, prevents devel dependancies
rm %{buildroot}/%{_libdir}/libhuginbase.so
rm %{buildroot}/%{_libdir}/libhuginANN.so
rm %{buildroot}/%{_libdir}/libhuginvigraimpex.so
rm %{buildroot}/%{_libdir}/libceleste.so

# Menu icons
install -m644 %{SOURCE11} -D %buildroot%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %buildroot%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %buildroot%{_liconsdir}/%{name}.png

# menu entry
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-CrossDesktop;" \
  --add-category="Photography" \
  --add-category="Graphics" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*

%if %mdkversion > 200900
%post
%update_menus
%update_desktop_database

%postun 
%clean_menus
%clean_desktop_database
%endif

%clean 
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL_cmake README README_JP TODO LICENCE_VIGRA doc/nona.txt doc/fulla.html src/hugin1/hugin/xrc/data/help_en_EN/LICENCE.manual doc/batch-processing/README.batch
%{_bindir}/*
%{_libdir}/libhugin*
%{_libdir}/libceleste*
%{_datadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man?/*
%{_datadir}/applications/hugin.desktop
%{_datadir}/applications/PTBatcher*.desktop
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-ptoptimizer-script.png
%{_datadir}/mime/packages/hugin.xml
%{_datadir}/pixmaps/hugin.png
