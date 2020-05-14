%define _disable_ld_no_undefined 1

Summary:	Panorama Tools GUI
Name:		hugin
Version:	2019.2.0
Release:	3
License:	GPLv2+
Group:		Graphics
Url:		http://hugin.sourceforge.net
Source0:	http://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.bz2

BuildRequires:	cmake ninja
BuildRequires:	desktop-file-utils
BuildRequires:	swig >= 2.0
BuildRequires:	tclap
BuildRequires:	zip
BuildRequires:	boost-devel
BuildRequires:	fftw-devel
BuildRequires:	jpeg-devel
# pkgconfig(libtiff-4) is not provided by libtiff in 2011 so we use old format
BuildRequires:	tiff-devel
BuildRequires:  vigra-devel
BuildRequires:	wxgtku3.0-devel
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(lensfun)
BuildRequires:	pkgconfig(libpano13) >= 2.9.18
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(lapack)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	perl-Image-ExifTool
Requires:	enblend >= 3.2
Requires:	libpano13-tools >= 2.9.18
Requires:	perl-Image-ExifTool

%description
Hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. 

%prep
%autosetup -p1

# Fix error: non-readable in debug package, we get 1000+ errors from rpmlint
find . -type f -exec chmod 644 {} \;

%build
%define Werror_cflags %{nil}
%cmake -DCMAKE_SKIP_RPATH:BOOL=OFF -DBUILD_HSI=1 -DENABLE_LAPACK=ON -G Ninja
%ninja_build

%install
%ninja_install -C build

# menu entry
desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="X-MandrivaLinux-CrossDesktop;" \
	--add-category="Photography" \
	--add-category="Graphics" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name} nona_gui %{name}.lang

%files -f %{name}.lang
%doc AUTHORS INSTALL_cmake README TODO doc/nona.txt doc/fulla.html src/hugin1/hugin/xrc/data/help_en_EN/LICENCE.manual
%{_bindir}/*
%{_libdir}/%{name}/lib*.so.*
%{_datadir}/%{name}
%{_datadir}/appdata/*
%{_datadir}/applications/*.desktop
%{_iconsdir}/gnome/48x48/mimetypes/gnome-mime-application-x-ptoptimizer-script.png
%{_datadir}/mime/packages/hugin.xml
%{_iconsdir}/hicolor/*
%{py_platsitedir}/*
%{_mandir}/man?/*
