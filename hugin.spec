Summary:	Panorama Tools GUI
Name:		hugin
Version:	2011.4.0
Release:	3
License:	GPLv2+
Group:		Graphics
URL:		http://hugin.sourceforge.net
Source0:	http://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		hugin-2011.4.0-l10n-ru.patch
Requires:	libpano13-tools >= 2.9.18
Requires:	enblend >= 3.2
Requires:	perl-Image-ExifTool
Requires:	make
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	desktop-file-utils
BuildRequires:	tclap
BuildRequires:	zip
BuildRequires:	fftw2-devel
BuildRequires:	jpeg-devel
# pkgconfig(libtiff-4) is not provided by libtiff in 2011 so we use old format
BuildRequires:	tiff-devel
BuildRequires:	wxgtku-devel
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libpano13) >= 2.9.18
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)

%description
Hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. 

%prep
%setup -q
%patch0 -p1 -b .po-file
# Fix error: non-readable in debug package, we get 1000+ errors from rpmlint
find . -type f -exec chmod 644 {} \;

%build
%define Werror_cflags %{nil}
%cmake -DCMAKE_SKIP_RPATH:BOOL=OFF
%make

%install
%makeinstall_std -C build

# Menu icons
%__install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
%__install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
%__install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

# menu entry
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-CrossDesktop;" \
  --add-category="Photography" \
  --add-category="Graphics" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*

%find_lang %{name} %{name} nona_gui

%if %{mdvver} <= 201100
%find_lang %{name} %{name} nona_gui
%else
%find_lang %{name} nona_gui %{name}.lang
%endif

%files -f %{name}.lang
%doc AUTHORS COPYING INSTALL_cmake README README_JP TODO LICENCE_VIGRA doc/nona.txt doc/fulla.html src/hugin1/hugin/xrc/data/help_en_EN/LICENCE.manual
%{_bindir}/*
%{_libdir}/%{name}/lib*.so.*
%{_datadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man?/*
%{_datadir}/applications/hugin.desktop
%{_datadir}/applications/PTBatcher*.desktop
%{_datadir}/applications/calibrate_lens_gui.desktop
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-ptoptimizer-script.png
%{_datadir}/mime/packages/hugin.xml
%{_datadir}/pixmaps/hugin.png
%{_datadir}/pixmaps/ptbatcher.png
