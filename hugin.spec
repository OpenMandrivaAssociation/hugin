%define beta beta4

Summary:	Panorama Tools GUI
Name: 		hugin
Version:	0.7
Release:	%mkrel 0.%{beta}.2
License:	GPL
Group:		Graphics
URL:		http://hugin.sourceforge.net
Source0:	http://downloads.sourceforge.net/hugin/%{name}-%{version}_%{beta}.tar.bz2
Patch0:		hugin-gcc43.diff
Patch1:		hugin-linkage_fix.diff
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Requires:	pano12
Requires:	enblend
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:	libboost-devel
BuildRequires:	pano12-devel >= 2.8.1
BuildRequires:	pano13-devel >= 2.8.1
BuildRequires:	fftw2-devel
BuildRequires:	libwxgtku-devel > 2.5
BuildRequires:	zlib-devel 
BuildRequires:	libtiff-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	zip
BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. 

%prep 

%setup -q -n %{name}-%{version}_%{beta}
%patch0 -p1

%build
touch m4/Makefile.in

# work-around broken wxGTK2.6 package
#ln -s %{_bindir}/wxrc-2.6-unicode ./wxrc
#export PATH=`pwd`:$PATH
export CFLAGS="%{optflags} -fpermissive"
export CXXFLAGS="%{optflags} -fpermissive"

%configure2_5x \
    --disable-rpath \
    --disable-static \
    --with-wx-config=wx-config-unicode \
    --with-unicode=yes

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

# menu entry
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-CrossDesktop;" \
  --add-category="Photography" \
  --add-category="Graphics" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*

%post
%update_menus
%update_desktop_database

%postun 
%clean_menus
%clean_desktop_database

%clean 
rm -rf %buildroot

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
