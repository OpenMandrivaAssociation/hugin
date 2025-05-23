%define _disable_ld_no_undefined 1

Summary:	Panorama Tools GUI
Name:		hugin
Version:	2024.0.1
Release:	5
License:	GPLv2+
Group:		Graphics
Url:		https://hugin.sourceforge.net
Source0:	https://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.bz2

BuildRequires:	gettext
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
BuildRequires:	wxwidgets-devel
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
# fix from suse
# Doesn't define the ZLIB::ZLIB target needed by OpenEXR 3
rm CMakeModules/FindZLIB.cmake

%define Werror_cflags %{nil}
%cmake \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-DBUILD_HSI=1 \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# menu entry
desktop-file-install \
	--vendor="" \
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
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/hugin.xml
%{_datadir}/metainfo/*
#{_iconsdir}/gnome/48x48/mimetypes/application-x-ptoptimizer-script.png
%{_iconsdir}/hicolor/*
%{py_platsitedir}/*
%{_mandir}/man?/*
