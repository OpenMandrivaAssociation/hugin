Summary:	Panorama Tools GUI
Name:		hugin
Version: 2012.0.0
Release: 1.auto
License:	GPLv2+
Group:		Graphics
URL:		http://hugin.sourceforge.net
Source0:	http://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		hugin-2011.4.0-l10n-ru.patch
Patch1:		hugin-2011.4.0-gcc4.7.patch
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
%patch1 -p1 -b .gcc4.7
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


%changelog
* Tue Feb 07 2012 Andrey Bondrov <abondrov@mandriva.org> 2011.4.0-1
+ Revision: 771623
- pkgconfig(libtiff-4) is not provided by libtiff in 2011 so we revert to tiff-devel
- Update russian translation patch, more spec cleanups, fix file permissions in debug package

  + Matthew Dawkins <mattydaw@mandriva.org>
    - cleaned up spec
    - converted BRs to pkgconfig provides

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 2011.4.0

* Fri Oct 28 2011 vsinitsyn <vsinitsyn> 2011.2.0-3
+ Revision: 707709
- Fixed BuildRequires section, added tclap
- Removed stale patch file
- Fixed \SPECSiles section in the spec
- Added the patch file missed from previous commit
- Fixed patch file naming
- Updated Russian translation

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 2011.2.0

  + Funda Wang <fwang@mandriva.org>
    - br xmu

* Thu Jun 23 2011 Funda Wang <fwang@mandriva.org> 2011.0.0-2
+ Revision: 686754
- enable rpath

* Sun Jun 19 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2011.0.0-1
+ Revision: 686056
- update file list
- drop patch 0, fixed by upstream
- update to new version 2011.0.0
- update to new version 2010.4.0
- spec file clean

* Tue Mar 15 2011 Funda Wang <fwang@mandriva.org> 2010.2.0-3
+ Revision: 644911
- rebuild for new boost

* Wed Dec 01 2010 Funda Wang <fwang@mandriva.org> 2010.2.0-2mdv2011.0
+ Revision: 604452
- rebuild for new exiv2

* Sat Oct 16 2010 Eugeni Dodonov <eugeni@mandriva.com> 2010.2.0-1mdv2011.0
+ Revision: 585891
- Updated to 2010.2.0 final.

* Thu Sep 16 2010 Eugeni Dodonov <eugeni@mandriva.com> 2010.2.0-0.rc1.1mdv2011.0
+ Revision: 579115
- Updated to 2010.2rc1.

* Mon Aug 23 2010 Funda Wang <fwang@mandriva.org> 2010.2.0-0.beta1.5mdv2011.0
+ Revision: 572268
- rebuild for new boost

* Thu Aug 05 2010 Funda Wang <fwang@mandriva.org> 2010.2.0-0.beta1.4mdv2011.0
+ Revision: 566096
- rebuild for new boost

* Tue Aug 03 2010 Funda Wang <fwang@mandriva.org> 2010.2.0-0.beta1.3mdv2011.0
+ Revision: 565565
- rebuild for new exiv2

  + Nicholas Brown <nickbrown@mandriva.org>
    - bump release
    - Make installable

* Thu Jul 22 2010 Nicholas Brown <nickbrown@mandriva.org> 2010.2.0-0.beta1.1mdv2011.0
+ Revision: 556922
- New Version

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - fix conditional for %%post scripts

* Sat Feb 13 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2009.4.0-1mdv2010.1
+ Revision: 505490
- new release 2009.4.0

* Mon Feb 08 2010 Anssi Hannula <anssi@mandriva.org> 2009.2.0-5mdv2010.1
+ Revision: 501882
- rebuild for new boost

* Wed Feb 03 2010 Funda Wang <fwang@mandriva.org> 2009.2.0-4mdv2010.1
+ Revision: 500328
- rebuild for new boost

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 2009.2.0-3mdv2010.1
+ Revision: 492239
- rebuild for new libjpeg v8

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 2009.2.0-2mdv2010.1
+ Revision: 484207
- Rebuild for new libexiv2

* Wed Sep 30 2009 Nicholas Brown <nickbrown@mandriva.org> 2009.2.0-1mdv2010.0
+ Revision: 451790
- new version

* Fri Aug 21 2009 Funda Wang <fwang@mandriva.org> 0.8.0-3mdv2010.0
+ Revision: 418880
- rebuild for new libboost

* Sat Jul 18 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.8.0-2mdv2010.0
+ Revision: 397069
- Update to 0.8.0 final
- Update to 0.8.0 final

* Sun Jun 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.0-0.rc4.1mdv2010.0
+ Revision: 387692
- new version
- rediff patch

* Tue Mar 10 2009 Nicholas Brown <nickbrown@mandriva.org> 0.8.0-0.beta2.1mdv2009.1
+ Revision: 353413
- new version

* Wed Feb 25 2009 Nicholas Brown <nickbrown@mandriva.org> 0.8.0-0.beta1.1mdv2009.1
+ Revision: 344700
- fix build dependancies
- new version

* Mon Dec 22 2008 Funda Wang <fwang@mandriva.org> 0.7.0-4mdv2009.1
+ Revision: 317401
- rebuild against new boost

* Fri Oct 24 2008 Nicholas Brown <nickbrown@mandriva.org> 0.7.0-3mdv2009.1
+ Revision: 296923
- rebuild
- fix requires

* Wed Oct 22 2008 Nicholas Brown <nickbrown@mandriva.org> 0.7.0-1mdv2009.1
+ Revision: 296523
- final release version.
  depend on make. #44648
  remove unused .so files, to remove (devel) dependancies.

* Mon Sep 15 2008 Nicholas Brown <nickbrown@mandriva.org> 0.7.0-0.rc6.1mdv2009.0
+ Revision: 284888
- new rc6

* Thu Sep 04 2008 Nicholas Brown <nickbrown@mandriva.org> 0.7.0-0.rc5.1mdv2009.0
+ Revision: 280482
- rc5
- forgot patch file
- rc4
  now using cmake
  patch for proper linking
  tidyup

  + Oden Eriksson <oeriksson@mandriva.com>
    - added a gcc43 patch (P0, from gentoo)
    - fix linkage (P1, from gentoo)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun Jan 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.7-0.beta4.1mdv2008.1
+ Revision: 158623
- pano13 support
- new version

* Sat Jan 12 2008 Austin Acton <austin@mandriva.org> 0.6.1-4mdv2008.1
+ Revision: 149791
- rebuild for boost

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Sep 24 2007 Anne Nicolas <ennael@mandriva.org> 0.6.1-3mdv2008.0
+ Revision: 92452
- Fix BuilRequire
- increase release
- Fix menu
- import hugin


* Sat Sep 02 2006 Anssi Hannula <anssi@mandriva.org> 0.6.1-2mdv2007.0
- fix buildrequires

* Mon Aug 21 2006 Frederic Crozat <fcrozat@mandriva.com> 0.6.1-1mdv2007.0
- Release 0.6.1

* Sat Jul 29 2006 Couriousous <couriousous@mandriva.org> 0.6-1mdv2007.0
- mkrel
- XDG menu
- 0.6

* Sun Jan 14 2006 Sebastien Savarin <plouf@mandriva.org> 0.5.3mdk
- Fix Requires on enblend

* Sat Jan  7 2006 Couriousous <couriousous@mandriva.org> 0.5-2mdk
- Fix buildrequires ( danny at mailmij,org )

* Sat Dec 17 2005 Couriousous <couriousous@mandriva.org> 0.5-1mdk
- 0.5 final

* Sun Sep 25 2005 Couriousous <couriousous@mandriva.org> 0.5-0.rc2.1mdk
- rc2
- Requires pano12 ( for PTOptimizer )
- Requires enblend ( hugin use it to blend pictures )
- Remove old sift-related stuff

* Thu Sep  1 2005 Couriousous <couriousous@mandriva.org> 0.5-0.rc1.5mdk
- rebuild without glitz deps

* Sat Aug 20 2005 Couriousous <couriousous@mandriva.org> 0.5-0.rc1.4mdk
- Fix hugin on x86_64

* Fri Jul 08 2005 Couriousous <couriousous@mandriva.org> 0.5-0.rc1.3mdk
- Rebuild with wxGTK2.6 
- Build with unicode 
- Do not use -z with enblend

* Mon Jun 27 2005 Couriousous <couriousous@mandriva.org> 0.5-0.rc1.2mdk
- Rebuild with wxGTK2.5

* Sun Jun 12 2005 Frederic Crozat <fcrozat@mandriva.com> 0.5-0.rc1.1mdk 
- Release 0.5rc1

* Sat May 21 2005 Couriousous <couriousous@mandriva.org> 0.5-0.beta6.2mdk
- Work-around some wxGTK2.6 bug

* Sat May 21 2005 Couriousous <couriousous@mandriva.org> 0.5-0.beta6.1mdk
- Beta6
- Rebuild with wxGTK 2.6 

* Sun May 15 2005 Couriousous <couriousous@mandriva.org> 0.5-0.beta4.2mdk
- Rebuild with WxWidget 2.5

* Sun Mar 27 2005 Couriousous <couriousous@mandrake.org> 0.5-0.beta4.1mdk
- 0.5 beta4

* Wed Jan 26 2005 Couriousous <couriousous@mandrake.org> 0.4-0.20050126.1mdk
- Cvs sync
- Disable french locale since it doesn't build

* Tue Jan 04 2005 Couriousous <couriousous@mandrake.org> 0.4-0.20050104.1mdk
- Cvs sync
- Some spec clean
- Use automatic install
- Add locales
- Disable "de" locale, as it doesn't build

* Wed Dec 08 2004 Couriousous <couriousous@mandrake.org> 0.4-0.20041208.1mdk
- Cvs sync

* Sat Aug 28 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.4-0.20040725.2mdk
- fixed directory ownership (distlint)

* Thu Aug 05 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.4-0.20040725.1mdk
- update from Couriousous <couriousous@zarb.org>:
 - sync with CVS
 - drop patch0
 - split the patented and non-patented part in two package
- disabled parallel build
- fixed buildrequires

* Fri Jul 02 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.3-1mdk 
- contributed by Couriousous <couriousous@sceen.net>

