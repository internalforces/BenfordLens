# Qt 6.11.1 third-party attributions

Generated from official `qt_attribution.json` records in the sources listed in `QT_SOURCES.json`.

## Adobe Glyph List For New Fonts

- **Description**: Provides standardized names for glyphs.
- **QtUsage**: Used by PDF generator to make it easier for reader applications to resolve  the original contents of rendered text.
- **Homepage**: https://github.com/adobe-type-tools/agl-aglfn
- **Version**: 1.7
- **License**: BSD 3-Clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: LICENSE.AGLFN.txt
- **Copyright**: Copyright 2002, 2003, 2005, 2006, 2008, 2010, 2015 Adobe Systems
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/text/qt_attribution.json`

## Anti-aliasing rasterizer from FreeType 2

- **Description**: FreeType is a freely available software library to render fonts.
- **QtUsage**: Used in Qt GUI.
- **Homepage**: http://www.freetype.org
- **License**: Freetype Project License or GNU General Public License v2.0 only
- **LicenseId**: FTL OR GPL-2.0-only
- **LicenseFile**: ../../3rdparty/freetype/LICENSE.txt
- **Copyright**: Copyright 2000-2016 by David Turner, Robert Wilhelm, and Werner Lemberg.
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/painting/qt_attribution.json`

## Apache Tika MimeType Definitions

- **Description**: The Apache Tika MimeTypes list many known MIME types and how to match files (using globs and/or 'magic' rules for the file contents)
- **QtUsage**: Qt Core uses a copy of the Apache Tika MimeType Definitions if shared-mime-info isn't installed on the system.
- **Homepage**: https://github.com/apache/tika/tree/main/tika-core/src/main/resources/org/apache/tika/mime
- **Version**: 408c26e1e03e018a623e732dff6fb047a2fb8e19
- **License**: Apache License 2.0
- **LicenseId**: Apache-2.0
- **Copyright**: Copyright 2026 The Apache Software Foundation
- **Qt source record**: `qt/qtbase@v6.11.1:src/corelib/mimetypes/3rdparty/qt_attribution.json`

## BLAKE2 (reference implementation)

- **Description**: BLAKE2 is a cryptographic hash function faster than MD5, SHA-1, SHA-2, and SHA-3, yet is at least as secure as the latest standard SHA-3.
- **QtUsage**: Used in Qt Core (QCryptographicHash).
- **Homepage**: https://blake2.net/
- **Version**: ed1974ea83433eba7b2d95c5dcd9ac33cb847913
- **License**: Creative Commons Zero v1.0 Universal or Apache License 2.0
- **LicenseId**: CC0-1.0 OR Apache-2.0
- **LicenseFile**: COPYING
- **Copyright**: Copyright 2012, Samuel Neves <sneves@dei.uc.pt>
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/blake2/qt_attribution.json`

## Catch2

- **Description**: Catch2 is a multi-paradigm test framework for C++.
- **QtUsage**: Used for testing of the Qt Test module.
- **Homepage**: https://github.com/catchorg/Catch2
- **Version**: 2.13.10
- **License**: Boost Software License 1.0
- **LicenseId**: BSL-1.0
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (c) 2022 Two Blue Cubes Ltd. All rights reserved.
- **Qt source record**: `qt/qtbase@v6.11.1:src/testlib/3rdparty/catch2/qt_attribution.json`

## cmake-runcmake-test-modules

- **Description**: CMake helpers for running CMake tests.
- **QtUsage**: Used as part of the build system.
- **Homepage**: https://cmake.org/
- **Version**: 3.31.5
- **License**: BSD 3-Clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: Copyright.txt
- **Copyright**: Copyright © 2000-2024 Kitware, Inc. and Contributors
- **Qt source record**: `qt/qtbase@v6.11.1:src/testinternal/3rdparty/cmake/qt_attribution.json`

## Cocoa Platform Plugin

- **Description**: Allows Qt to integrate into Apple's Cocoa API.
- **QtUsage**: Code used in the Qt Platform Abstraction (QPA) for macOS.
- **License**: BSD 3-clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: LICENSE.COCOA.txt
- **Copyright**: Copyright (c) 2007-2008, Apple, Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/plugins/platforms/cocoa/qt_attribution.json`

## Cycle

- **Description**: Enables access to the CPU's cycle counters.
- **QtUsage**: Used in the Qt Test module.
- **Homepage**: http://fftw.org/
- **Version**: 3.3.10
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (c) 2003, 2007-14 Matteo Frigo; Copyright (c) 2003, 2007-14 Massachusetts Institute of Technology
- **Qt source record**: `qt/qtbase@v6.11.1:src/testlib/3rdparty/cycle/qt_attribution.json`

## D3D12 Memory Allocator

- **Description**: D3D12 Memory Allocator
- **QtUsage**: Memory management for the D3D12 backend of QRhi.
- **Homepage**: https://github.com/GPUOpen-LibrariesAndSDKs/D3D12MemoryAllocator
- **Version**: f128d39b7a95b4235bd228d231646278dc6c24b2
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (c) 2019-2022 Advanced Micro Devices, Inc. All rights reserved.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/D3D12MemoryAllocator/qt_attribution.json`

## Data Compression Library (zlib)

- **Description**: zlib is a general purpose data compression library.
- **QtUsage**: Optionally used in Qt Core and development tools. Configure with -system-zlib to avoid.
- **Homepage**: https://zlib.net/
- **Version**: 1.3.2
- **License**: zlib License
- **LicenseId**: Zlib
- **LicenseFile**: LICENSE
- **Copyright**: (C) 1995-2026 Jean-loup Gailly and Mark Adler
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/zlib/qt_attribution.json`

## DejaVu Fonts

- **Description**: The DejaVu fonts are a font family based on the Vera Fonts.
- **QtUsage**: Used for WebAssembly platform.
- **Homepage**: https://dejavu-fonts.github.io/
- **Version**: 2.37
- **License**: Bitstream Vera Font License
- **LicenseId**: Bitstream-Vera
- **LicenseFile**: DEJAVU-LICENSE
- **Copyright**: Copyright (c) 2003 by Bitstream, Inc; Copyright (c) 2006 by Tavmjong Bah; (c) American Mathematical Society
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wasm/qt_attribution.json`

## Easing Equations by Robert Penner

- **QtUsage**: Used in Qt Core (QEasingCurve).
- **Homepage**: http://robertpenner.com/easing/
- **License**: BSD 3-clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: LICENSE
- **Copyright**: Copyright (c) 2001 Robert Penner
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/easing/qt_attribution.json`

## Efficient Binary-Decimal and Decimal-Binary Conversion Routines for IEEE Doubles

- **QtUsage**: Used in Qt Core. Configure with -system-doubleconversion or -no-doubleconversion to avoid.
- **Homepage**: https://github.com/google/double-conversion
- **Version**: 3.4.0
- **License**: BSD 3-clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: LICENSE
- **Copyright**: Copyright 2006-2012, the V8 project authors
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/double-conversion/qt_attribution.json`

## Emoji Segmenter

- **Description**: A parser for emoji sequences.
- **QtUsage**: Used in QtGui for parsing complex emoji sequences. Can be configured using the -emojisegmenter option.
- **Homepage**: https://github.com/google/emoji-segmenter
- **Version**: 0.4.0
- **License**: Apache License 2.0
- **LicenseId**: Apache-2.0
- **Copyright**: Copyright 2019 Google LLC
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/emoji-segmenter/qt_attribution.json`

## extra-cmake-modules

- **Description**: Additional CMake modules.
- **QtUsage**: Used as part of the build system.
- **QtParts**: tools
- **Homepage**: https://api.kde.org/ecm/
- **Version**: 5.84.0
- **License**: BSD-3-Clause
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: COPYING-CMAKE-SCRIPTS
- **Copyright**: Copyright © 2011-2018 The KDE community
- **Qt source record**: `qt/qtbase@v6.11.1:cmake/3rdparty/extra-cmake-modules/qt_attribution.json`

## Freetype 2

- **Description**: FreeType is a freely available software library to render fonts.
- **QtUsage**: Optionally used in Qt GUI and platform plugins. Configure with -no-freetype, or -system-freetype to avoid.
- **Homepage**: http://www.freetype.org
- **Version**: 2.14.3
- **License**: Freetype Project License or GNU General Public License v2.0 only
- **LicenseId**: FTL OR GPL-2.0-only
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (c) 2007-2014 Adobe Systems Incorporated; Copyright (c) 2004-2026 Albert Chin-A-Young; Copyright (c) 2018-2026 Armin Hasitzka, David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2000 Computing Research Labs, New Mexico State University; Copyright (c) 1996-2026 David Turner, Robert Wilhelm, Dominik Röttsches, and Werner Lemberg; Copyright (c) 2004-2026 David Turner, Robert Wilhelm, Werner Lemberg and George Williams; Copyright (c) 2022-2026 David Turner, Robert Wilhelm, Werner Lemberg, and Moazin Khatti; Copyright (c) 2008-2026 David Turner, Robert Wilhelm, Werner Lemberg, and suzuki toshiya; Copyright (c) 2003-2026 David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2005-2026 David Turner; Copyright (c) 2007-2026 Derek Clegg and Michael Toftdal; Copyright (c) 2007 Dmitry Timoshkov for Codeweavers; Copyright (c) 2001-2015 Francesco Zappa Nardelli; Copyright (c) 2005, 2007, 2008, 2013 George Williams; Copyright (c) 2013-2026 Google, Inc. Google Author(s) Behdad Esfahbod and Stuart Gill; Copyright (c) 2013-2022 Google, Inc.; Copyright (c) 2003 Huw D M Davies for Codeweavers; Copyright (c) 2010-2026 Joel Klinghed; Copyright (c) 1996-2026 Just van Rossum, David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2003-2026 Masatake YAMATO and Redhat K.K.; Copyright (c) 2004-2026 Masatake YAMATO, Redhat K.K, David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2019-2026 Nikhil Ramakrishnan, David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2009-2026 Oran Agra and Mickey Gabel; Copyright (c) 2007-2026 Rahul Bhalerao <rahul.bhalerao@redhat.com>; Copyright (c) 2002-2026 Roberto Alameda; Copyright (c) 2015-2026 Werner Lemberg; Copyright (c) 2004-2026 suzuki toshiya, Masatake YAMATO, Red Hat K.K., David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2019 nyorain; Copyright (c) 2022-2026 David Turner, Robert Wilhelm, Werner Lemberg, George Williams, and Dominik Röttsches; Copyright (C) 2009, 2023  Red Hat, Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/freetype/qt_attribution.json`

## Freetype 2 - Bitmap Distribution Format (BDF) support

- **Description**: FreeType is a freely available software library to render fonts.
- **QtUsage**: Optionally used in Qt GUI and platform plugins. Configure with -no-freetype, or -system-freetype to avoid.
- **Homepage**: http://www.freetype.org
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: BDF-LICENSE.txt
- **Copyright**: Copyright (c) 2000 Computing Research Labs, New Mexico State University; Copyright (c) 2001-2014 Francesco Zappa Nardelli
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/freetype/qt_attribution.json`

## Freetype 2 - Portable Compiled Format (PCF) support

- **Description**: FreeType is a freely available software library to render fonts.
- **QtUsage**: Optionally used in Qt GUI and platform plugins. Configure with -no-freetype, or -system-freetype to avoid.
- **Homepage**: http://www.freetype.org
- **License**: MIT License and MIT Open Group variant
- **LicenseId**: MIT AND MIT-open-group
- **LicenseFile**: PCF-LICENSE.txt
- **Copyright**: Copyright (c) 2001, 2012 David Turner, Robert Wilhelm, and Werner Lemberg; Copyright (c) 2000-2014 Francesco Zappa Nardelli; Copyright (c) 1990, 1994, 1998 The Open Group
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/freetype/qt_attribution.json`

## Freetype 2 - zlib

- **Description**: FreeType is a freely available software library to render fonts.
- **QtUsage**: Optionally used in Qt GUI and platform plugins. Configure with -no-freetype, or -system-freetype to avoid.
- **Homepage**: http://www.freetype.org
- **License**: zlib License
- **LicenseId**: Zlib
- **LicenseFile**: ZLIB-LICENSE.txt
- **Copyright**: Copyright (C) 1995-2024 Jean-loup Gailly and Mark Adler
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/freetype/qt_attribution.json`

## Gradle wrapper

- **QtUsage**: Needed to create Android packages
- **QtParts**: tools
- **Homepage**: https://gradle.org
- **Version**: 9.3.1
- **License**: Apache License 2.0
- **LicenseId**: Apache-2.0
- **LicenseFile**: LICENSE
- **Copyright**: Copyright (C) 2025 Gradle Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/gradle/qt_attribution.json`

## HarfBuzz-NG

- **Description**: HarfBuzz is an OpenType text shaping engine.
- **QtUsage**: Optionally used in Qt GUI. Configure with -system-harfbuzz to force the use of the system library, or -qt-harfbuzz to link statically to the library that is bundled with your Qt version.
- **Homepage**: http://harfbuzz.org
- **Version**: 14.2.0
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: COPYING
- **Copyright**: Copyright © 2010-2022  Google, Inc.; Copyright © 2015-2020  Ebrahim Byagowi; Copyright © 2019,2020  Facebook, Inc.; Copyright © 2012,2015  Mozilla Foundation; Copyright © 2011  Codethink Limited; Copyright © 2008,2010  Nokia Corporation and/or its subsidiary(-ies); Copyright © 2009  Keith Stribley; Copyright © 2011  Martin Hosken and SIL International; Copyright © 2007  Chris Wilson; Copyright © 2005,2006,2020,2021,2022,2023  Behdad Esfahbod; Copyright © 2004,2007,2008,2009,2010,2013,2021,2022,2023  Red Hat, Inc.; Copyright © 1998-2005  David Turner and Werner Lemberg; Copyright © 2016  Igalia S.L.; Copyright © 2022  Matthias Clasen; Copyright © 2018,2021  Khaled Hosny; Copyright © 2018,2019,2020  Adobe, Inc; Copyright © 2013-2015  Alexei Podtelezhnikov
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/harfbuzz-ng/qt_attribution.json`

## KWin

- **Description**: Additional CMake modules for graphics system dependencies.
- **QtUsage**: Used as part of the build system.
- **QtParts**: tools
- **Homepage**: https://www.kde.org/
- **Version**: 5.13.4
- **License**: BSD 3-Clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: COPYING-CMAKE-SCRIPTS
- **Copyright**: Copyright 2014 Alex Merry <alex.merry@kde.org>; Copyright 2014 Martin Gräßlin <mgraesslin@kde.org>; Copyright (c) 2006,2007 Laurent Montel, <montel@kde.org>
- **Qt source record**: `qt/qtbase@v6.11.1:cmake/3rdparty/kwin/qt_attribution.json`

## libdbus-1 headers

- **Description**: D-Bus is a message bus system, a simple way for applications to talk to one another.
- **QtUsage**: Qt D-Bus uses constants and typedefs from libdbus-1 headers.
- **Homepage**: https://www.freedesktop.org/wiki/Software/dbus/
- **Version**: 1.13.12
- **License**: Academic Free License v2.1, or GNU General Public License v2.0 or later
- **LicenseId**: AFL-2.1 OR GPL-2.0-or-later
- **LicenseFile**: LICENSE.LIBDBUS-1.txt
- **Copyright**: Copyright (C) 2002, 2003 CodeFactory AB; Copyright (C) 2004, 2005 Red Hat, Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/dbus/qt_attribution.json`

## LibJPEG-turbo

- **Description**: The Independent JPEG Group's JPEG software
- **QtUsage**: Used in the qjpeg image plugin. Configure with -system-libjpeg or -no-libjpeg to avoid.
- **Homepage**: http://libjpeg-turbo.virtualgl.org/
- **Version**: 3.1.4
- **License**: Independent JPEG Group License and BSD 3-Clause "New" or "Revised" License
- **LicenseId**: IJG AND BSD-3-Clause
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/libjpeg/qt_attribution.json`

## LibPNG

- **Description**: libpng is the official PNG reference library.
- **QtUsage**: Used in the qpng image plugin. Configure with -system-libpng or -no-libpng to avoid.
- **Homepage**: http://www.libpng.org/pub/png/libpng.html
- **Version**: 1.6.58
- **License**: libpng License and PNG Reference Library version 2
- **LicenseId**: Libpng AND libpng-2.0
- **LicenseFile**: LICENSE
- **Copyright**: Copyright (c) 1995-2026 The PNG Reference Library Authors; Copyright (c) 2000-2026 Cosmin Truta; Copyright (c) 1998-2018 Glenn Randers-Pehrson; Copyright (c) 1996-1997 Andreas Dilger; Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc.; Copyright (c) 2000-2017 Simon-Pierre Cadieux; Copyright (c) 2000-2017 Eric S. Raymond; Copyright (c) 2000-2017 Mans Rullgard; Copyright (c) 2000-2017 Gilles Vollant; Copyright (c) 2000-2017 James Yu; Copyright (c) 2000-2017 Mandar Sahastrabuddhe; Copyright (c) 1998-2000 Tom Lane; Copyright (c) 1998-2000 Willem van Schaik; Copyright (c) 1996-1997 John Bowler; Copyright (c) 1996-1997 Kevin Bracey; Copyright (c) 1996-1997 Sam Bushell; Copyright (c) 1996-1997 Magnus Holmgren; Copyright (c) 1996-1997 Greg Roelofs; Copyright (c) 1996-1997 Tom Tanner; Copyright (c) 1995-1996 Dave Martindale; Copyright (c) 1995-1996 Paul Schmidt; Copyright (c) 1995-1996 Tim Wegner
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/libpng/qt_attribution.json`

## Linux Performance Events

- **Description**: Allows access to the Linux kernel's performance events.
- **QtUsage**: Used on Linux and Android in the Qt Test module.
- **Homepage**: https://www.kernel.org
- **Version**: 6.13
- **License**: GNU General Public License v2.0 only with Linux Syscall Note
- **LicenseId**: GPL-2.0-only WITH Linux-syscall-note
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (C) 2008-2009, Thomas Gleixner <tglx@linutronix.de>; Copyright (C) 2008-2011, Red Hat, Inc., Ingo Molnar; Copyright (C) 2008-2011, Red Hat, Inc., Peter Zijlstra
- **Qt source record**: `qt/qtbase@v6.11.1:src/testlib/3rdparty/linux/qt_attribution.json`

## MD4

- **Description**: An OpenSSL-compatible implementation of the RSA Data Security, Inc. MD4 Message-Digest Algorithm.
- **QtUsage**: Used in Qt Core (QCryptographicHash).
- **License**: Public Domain
- **LicenseId**: CC0-1.0
- **Copyright**: Written by Alexander Peslyak - better known as Solar Designer <solar@openwall.com> - in 2001, and placed in the public domain. There's absolutely no warranty.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/md4/qt_attribution.json`

## MD4C

- **Description**: A CommonMark-compliant Markdown parser.
- **QtUsage**: Optionally used in QTextDocument if configured with textmarkdownreader.
- **Homepage**: https://github.com/mity/md4c
- **Version**: 0.5.2
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.md
- **Copyright**: Copyright © 2016-2024 Martin Mitáš
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/md4c/qt_attribution.json`

## MD5

- **Description**: MD5 message-digest algorithm.
- **QtUsage**: Used in Qt Core (QCryptographicHash).
- **License**: Public Domain
- **LicenseId**: CC0-1.0
- **Copyright**: Written by Colin Plumb in 1993, no copyright is claimed. Ian Jackson <ian@chiark.greenend.org.uk>.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/md5/qt_attribution.json`

## Mipmap generator for D3D12

- **Description**: Compute shader for mipmap generation from MiniEngine in DirectX-Graphics-Samples
- **QtUsage**: Compute shader for mipmap generation with Direct 3D 12
- **Homepage**: https://github.com/microsoft/DirectX-Graphics-Samples
- **Version**: 0aa79bad78992da0b6a8279ddb9002c1753cb849
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.MiniEngine.txt
- **Copyright**: Copyright (c) 2015 Microsoft
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/rhi/qt_attribution.json`

## Native Style for Android

- **QtUsage**: Used in Android platform plugin.
- **License**: Apache License 2.0
- **LicenseId**: Apache-2.0
- **LicenseFile**: LICENSE
- **Copyright**: Copyright (C) 2005 The Android Open Source Project
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/android/qt_attribution.json`

## OpenGL ES 2 Headers

- **Description**: OpenGL ES 2 header generated from the Khronos OpenGL / OpenGL ES XML API Registry.
- **QtUsage**: Used on Windows and Linux in the OpenGL related headers of Qt GUI.
- **Homepage**: https://www.khronos.org/
- **Version**: Revision 27673
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.KHRONOS.txt
- **Copyright**: Copyright (c) 2013-2014 The Khronos Group Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/opengl/qt_attribution.json`

## OpenGL Headers

- **Description**: OpenGL header generated from the Khronos OpenGL / OpenGL ES XML API Registry.
- **QtUsage**: Used on Windows and Linux in the OpenGL related headers of Qt GUI.
- **Homepage**: https://www.khronos.org/
- **Version**: Revision 27684
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.KHRONOS.txt
- **Copyright**: Copyright (c) 2013-2014 The Khronos Group Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/opengl/qt_attribution.json`

## PCRE2

- **Description**: The PCRE library is a set of functions that implement regular expression pattern matching using the same syntax and semantics as Perl 5.
- **QtUsage**: Used in Qt Core (QRegularExpression).
- **Homepage**: http://www.pcre.org/
- **Version**: 10.47
- **License**: BSD 3-clause "New" or "Revised" License with PCRE2 binary-like Packages Exception
- **LicenseId**: LicenseRef-BSD-3-Clause-with-PCRE2-Binary-Like-Packages-Exception
- **LicenseFile**: LICENCE.md
- **Copyright**: Copyright (c) 1997-2007 University of Cambridge; Copyright (c) 2007-2024 Philip Hazel; Copyright (c) 2010-2024 Zoltan Herczeg
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/pcre2/qt_attribution.json`

## PCRE2 - Stack-less Just-In-Time Compiler

- **Description**: The PCRE library is a set of functions that implement regular expression pattern matching using the same syntax and semantics as Perl 5.
- **QtUsage**: Used in Qt Core (QRegularExpression).
- **Homepage**: http://www.pcre.org/
- **Version**: 10.47
- **License**: BSD 2-clause "Simplified" License
- **LicenseId**: BSD-2-Clause
- **LicenseFile**: LICENSE-SLJIT
- **Copyright**: Copyright Zoltan Herczeg
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/pcre2/qt_attribution.json`

## Pixman

- **Description**: pixman is a library that provides low-level pixel manipulation features such as image compositing and trapezoid rasterization.
- **QtUsage**: Used in Qt GUI on ARM NEON.
- **Homepage**: http://www.pixman.org/
- **Version**: 0.17.12
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE
- **Copyright**: Copyright © 2009 Nokia Corporation
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/pixman/qt_attribution.json`

## Presentation Time Protocol

- **Description**: The presentaton time protocol is a way to get presentation timing feedback.
- **QtUsage**: Used in the Qt Wayland Compositor
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2013, 2014 Collabora, Ltd.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/presentation-time/qt_attribution.json`

## Python

- **Description**: Qt for Python is an add-on for Python. The libshiboken packages of PySide uses certain parts of the source files (bufferprocs_py37.cpp, bufferprocs_py37.h). See the folder sources/shiboken6/libshiboken .
- **QtUsage**: Used for Qt for Python in the signature extension.
- **Homepage**: http://www.python.org/
- **Version**: 3.7.0
- **License**: PSF LICENSE AGREEMENT FOR PYTHON 3.7.0
- **LicenseFile**: bufferprocs_py37.h
- **Copyright**: © Copyright 2001-2018, Python Software Foundation.
- **Qt source record**: `QtForPython/pyside-setup@6.11.1:sources/shiboken6/libshiboken/qt_attribution.json`

## Python

- **Description**: Qt for Python is an add-on for Python. The signature packages of PySide uses certain copied and adapted source files. See the folder sources/shiboken6/files.dir/shibokensupport .
- **QtUsage**: Used for Qt for Python in the signature extension.
- **Homepage**: http://www.python.org/
- **Version**: 3.7.0
- **License**: Python License 2.0
- **LicenseId**: Python-2.0
- **LicenseFile**: PSF-3.7.0.txt
- **Copyright**: © Copyright 2001-2018, Python Software Foundation.
- **Qt source record**: `QtForPython/pyside-setup@6.11.1:sources/shiboken6/shibokenmodule/files.dir/shibokensupport/signature/qt_attribution.json`

## QEventDispatcher on macOS

- **Description**: Implementation of QAbstractEventDispatcher for macOS.
- **QtUsage**: Used in Qt Core on macOS.
- **License**: BSD 3-clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: LICENSE.QEVENTDISPATCHER_CF.txt
- **Copyright**: Copyright (c) 2007-2008, Apple, Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/corelib/kernel/qt_attribution.json`

## Secure Hash Algorithm SHA-1

- **Description**: Implements the Secure Hash Algorithms SHA 1
- **QtUsage**: Used in Qt Core (QCryptographicHash).
- **Homepage**: http://www.dominik-reichl.de/projects/csha1/
- **License**: Public Domain
- **LicenseId**: LicenseRef-SHA1-Public-Domain
- **Copyright**: Copyright (C) Dominik Reichl <dominik.reichl@t-online.de>; Copyright (C) 2016 The Qt Company Ltd
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/sha1/qt_attribution.json`

## Secure Hash Algorithms SHA-384 and SHA-512

- **Description**: Implements the Secure Hash Algorithms SHA 384 and SHA-521
- **QtUsage**: Used in Qt Core (QCryptographicHash and QMessageAuthenticationCode)
- **License**: BSD 3-clause "New" or "Revised" License
- **LicenseId**: BSD-3-Clause
- **LicenseFile**: LICENSE
- **Copyright**: Copyright (c) 2011 IETF Trust and the persons identified as authors of the code.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/rfc6234/qt_attribution.json`

## Selected Material Icons

- **QtUsage**: Used in Color Palette Client example in QtDoc
- **QtParts**: examples
- **Homepage**: https://fonts.google.com/icons
- **License**: Apache License Version 2.0
- **LicenseId**: Apache-2.0
- **Copyright**: Copyright 2018 Google, Inc. All Rights Reserved.
- **Qt source record**: `QtForPython/pyside-setup@6.11.1:examples/demos/colorpaletteclient/icons/qt_attribution.json`

## SipHash Algorithm

- **Description**: Implements the SipHash algorithm.
- **QtUsage**: Used in Qt Core (QHash)
- **Homepage**: https://131002.net/siphash/
- **License**: Creative Commons Zero v1.0 Universal
- **LicenseId**: CC0-1.0
- **Copyright**: Copyright (C) 2012-2014 Jean-Philippe Aumasson; Copyright (C) 2012-2014 Daniel J. Bernstein <djb@cr.yp.to>; Copyright (C) 2016 Intel Corporation
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/siphash/qt_attribution.json`

## Smooth Scaling Algorithm

- **Description**: Normal smoothscale method, based on Imlib2's smoothscale.
- **QtUsage**: Used in Qt Gui (QImage::transformed() functions).
- **License**: BSD 2-clause "Simplified" License and Imlib2 License
- **LicenseId**: BSD-2-Clause AND Imlib2
- **LicenseFile**: LICENSE.QIMAGETRANSFORM.txt
- **Copyright**: Copyright (C) 2004, 2005 Daniel M. Duley.; (C) Carsten Haitzler and various contributors.; (C) Willem Monsuwe <willem@stack.nl>
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/painting/qt_attribution.json`

## SQLite

- **Description**: SQLite is a small C library that implements a self-contained, embeddable, zero-configuration SQL database engine.
- **QtUsage**: Used in Qt SQL Lite plugin. Configure Qt with -system-sqlite or -no-sqlite to avoid.
- **Homepage**: https://www.sqlite.org/
- **Version**: 3.53.0
- **License**: SQLite Blessing
- **LicenseId**: blessing
- **Copyright**: The authors disclaim copyright to the source code. However, a license can be obtained if needed.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/sqlite/qt_attribution.json`

## sRGB color profile icc file

- **Description**: An ICC color profile for PDF/A-1b compatible PDF files.
- **QtUsage**: Used in Qt Gui (Embedded into PDF/A-1b files generated by QPrinter/QPdfWriter).
- **Homepage**: http://www.color.org/
- **License**: International Color Consortium License
- **LicenseId**: LicenseRef-ICC-License
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright International Color Consortium, 2015
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/icc/qt_attribution.json`

## TinyCBOR

- **Description**: Concise Binary Object Representation (CBOR) Library
- **QtUsage**: Used for QCborStreamReader and QCborStreamWriter.
- **Homepage**: https://github.com/intel/tinycbor
- **Version**: 7.0
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE
- **Copyright**: Copyright (C) 2015-2025 Intel Corporation
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/tinycbor/qt_attribution.json`

## tl::expected

- **Description**: Single header implementation of std::expected with functional-style extensions.
- **QtUsage**: Available as a private type in all Qt modules
- **Homepage**: https://github.com/TartanLlama/expected/
- **Version**: 41d3e1f48d682992a2230b2a715bca38b848b269
- **License**: Creative Commons Zero v1.0 Universal
- **LicenseId**: CC0-1.0
- **Copyright**: To the extent possible under law, Sy Brand has waived all copyright and related or neighboring rights to the expected library. This work is published from: United Kingdom.
- **Qt source record**: `qt/qtbase@v6.11.1:src/corelib/global/qt_attribution.json`

## Valgrind

- **Description**: An instrumentation framework for building dynamic analysis tools.
- **QtUsage**: Used on Linux ond MacOS in the Qt Test module.
- **Homepage**: http://valgrind.org/
- **Version**: 3.25.1
- **License**: BSD 4-clause "Original" or "Old" License
- **LicenseId**: BSD-4-Clause
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (C) 2000-2017 Julian Seward; Copyright (C) 2003-2017 Josef Weidendorfer.
- **Qt source record**: `qt/qtbase@v6.11.1:src/testlib/3rdparty/valgrind/qt_attribution.json`

## Vulkan API Registry

- **Description**: Vulkan XML API Registry.
- **QtUsage**: Used to dynamically generate the sources for the QVulkan(Device)Functions classes.
- **Homepage**: https://www.khronos.org/
- **Version**: 1.4.308
- **License**: Apache License 2.0 or MIT License
- **LicenseId**: Apache-2.0 OR MIT
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (c) 2015-2025 The Khronos Group Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/vulkan/qt_attribution.json`

## Vulkan Memory Allocator

- **Description**: Vulkan Memory Allocator
- **QtUsage**: Memory management for the Vulkan backend of QRhi.
- **Homepage**: https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator
- **Version**: 3.2.1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.txt
- **Copyright**: Copyright (c) 2017-2025 Advanced Micro Devices, Inc. All rights reserved.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/VulkanMemoryAllocator/qt_attribution.json`

## Wayland Color Management Protocol

- **Description**: An extension to use different colorspaces from sRGB
- **QtUsage**: Used in the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright 2019 Sebastian Wick
Copyright 2019 Erwin Burema
Copyright 2020 AMD
Copyright 2020-2024 Collabora, Ltd.
Copyright 2024 Xaver Hugl
Copyright 2022-2025 Red Hat, Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/color-management/qt_attribution.json`

## Wayland Dialog Protocol

- **Description**: Register toplevel as dialogs
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2023 Carlos Garnacho
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-dialog/qt_attribution.json`

## Wayland EGLStream Controller Protocol

- **Description**: Allows clients to request that the compositor creates its EGLStream.
- **QtUsage**: Used in the Qt Wayland Compositor
- **Homepage**: https://github.com/NVIDIA/egl-wayland
- **Version**: 1.1.1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright (c) 2017, NVIDIA CORPORATION. All rights reserved.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/wl-eglstream/qt_attribution.json`

## Wayland Fractional Scale Protocol

- **Description**: Send a preferred scale to different clients
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2022 Kenny Levinsen
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/fractional-scale/qt_attribution.json`

## Wayland Fullscreen Shell Protocol

- **Description**: A Wayland shell for displaying a single surface per output
- **QtUsage**: Used in the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2016 Yong Bakos
Copyright © 2015 Jason Ekstrand
Copyright © 2015 Jonas Ådahl
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/fullscreen-shell/qt_attribution.json`

## Wayland KDE DBus Menu Protocol

- **Description**: Attach a dbus menu to a window
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://kde.org
- **Version**: 1
- **License**: GNU Lesser General Public License 2.1 or later
- **LicenseId**: LGPL-2.1-or-later
- **LicenseFile**: LGPL-2.1-or-later.txt
- **Copyright**: Copyright 2017 David Edmundson
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/appmenu/qt_attribution.json`

## Wayland Linux Dmabuf Unstable V1 Protocol

- **Description**: The linux dmabuf protocol is a way to create dmabuf-based wl_buffers
- **QtUsage**: Used in the Qt Wayland Compositor
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1, version 3
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2014, 2015 Collabora, Ltd.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/linux-dmabuf/qt_attribution.json`

## Wayland Pointer Gestures Protocol

- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1, version 2
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2015, 2016 Red Hat
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/pointer-gestures/qt_attribution.json`

## Wayland Pointer Warp Protocol

- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: version 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2024 Neal Gompa
Copyright © 2024 Xaver Hugl
Copyright © 2024 Matthias Klumpp
Copyright © 2024 Vlad Zahorodnii
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/pointer-warp/qt_attribution.json`

## Wayland Primary Selection Protocol

- **Description**: The primary selection extension allows copying text by selecting it and pasting it with the middle mouse button.
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2015, 2016 Red Hat
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/wp-primary-selection/qt_attribution.json`

## Wayland Protocol

- **Description**: Wayland is a protocol for a compositor to talk to its clients.
- **QtUsage**: Used in the Qt Wayland Compositor, and the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1.24.0
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2008-2011 Kristian Høgsberg
Copyright © 2010-2011 Intel Corporation
Copyright © 2012-2013 Collabora, Ltd.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/wayland/qt_attribution.json`

## Wayland Scaler Protocol

- **Description**: The Wayland scaler extension allows a client to scale or crop a surface without modifying the buffer
- **QtUsage**: Used in the Qt Wayland Compositor API
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 2
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2013-2014 Collabora, Ltd.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/scaler/qt_attribution.json`

## Wayland Session Management Protocol

- **Description**: An extension to restore window positions
- **QtUsage**: Used in the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: experimental V1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright 2018 Mike Blumenkrantz
Copyright 2018 Samsung Electronics Co., Ltd
Copyright 2018 Red Hat Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/session-management/qt_attribution.json`

## Wayland Tablet Protocol

- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v2, version 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright 2014 © Stephen "Lyude" Chandler Paul
Copyright 2015-2016 © Red Hat, Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/tablet/qt_attribution.json`

## Wayland Text Input Protocol

- **Description**: Adds support for compositors to act as input methods and send text to applications.
- **QtUsage**: Used in the Qt Wayland Compositor, and the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v3
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../../MIT_LICENSE.txt
- **Copyright**: Copyright © 2012, 2013 Intel Corporation
Copyright © 2015, 2016 Jan Arne Petersen
Copyright © 2017, 2018 Red Hat, Inc.
Copyright © 2018       Purism SPC
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/text-input/v3/qt_attribution.json`

## Wayland Text Input Protocol v1

- **Description**: Adds support for text input and input methods to applications running on Wayland servers that only support text-input-unstable-v1.
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../../MIT_LICENSE.txt
- **Copyright**: Copyright © 2012, 2013 Intel Corporation
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/text-input/v1/qt_attribution.json`

## Wayland Text Input Protocol v2

- **Description**: Adds support for text input and input methods to applications.
- **QtUsage**: Used in the Qt Wayland Compositor, and the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v2
- **License**: HPND License
- **LicenseId**: HPND
- **LicenseFile**: HPND_LICENSE.txt
- **Copyright**: Copyright © 2012, 2013 Intel Corporation
Copyright © 2015, 2016 Jan Arne Petersen
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/text-input/v2/qt_attribution.json`

## Wayland Viewporter Protocol

- **Description**: The Wayland viewporter extension allows a client to scale or crop a surface without modifying the buffer
- **QtUsage**: Used in the Qt Wayland Compositor API
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2013-2016 Collabora, Ltd.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/viewporter/qt_attribution.json`

## Wayland XDG Foreign Protocol

- **Description**: Allows referencing surfaces of different clients
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2015-2016 Red Hat Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-foreign/qt_attribution.json`

## Wayland XDG Output Protocol

- **Description**: The XDG Output protocol is an extended way to describe output regions under Wayland
- **QtUsage**: Used in the Qt Wayland Compositor API, and the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1, version 3
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2017 Red Hat Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-output/qt_attribution.json`

## Wayland XDG Shell Protocol

- **Description**: The XDG-Shell protocol is an extended way to manage surfaces under Wayland compositors.
- **QtUsage**: Used in the Qt Wayland Compositor, and the Qt Wayland platform plugin.
- **Homepage**: https://gitlab.freedesktop.org/wayland/wayland-protocols/
- **Version**: 1.18
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2008-2013 Kristian Høgsberg
Copyright © 2013      Rafael Antognolli
Copyright © 2013      Jasper St. Pierre
Copyright © 2010-2013 Intel Corporation
Copyright © 2015-2017 Samsung Electronics Co., Ltd
Copyright © 2015-2017 Red Hat Inc.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-shell/qt_attribution.json`

## Wayland XDG System Bell Protocol

- **Description**: The XDG-System-Bell protocol provides a mechanism for apps to provide visual notification feedback through the compositor.
- **QtUsage**: Used in the Qt Wayland Compositor, and the Qt Wayland platform plugin.
- **Homepage**: https://gitlab.freedesktop.org/wayland/wayland-protocols/
- **Version**: 1.18
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2016, 2023 Red Hat
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-system-bell/qt_attribution.json`

## Wayland xdg-activation Protocol

- **Description**: The xdg-activation protocol provides a way for one client to pass focus to another.
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1, version 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2020 Aleix Pol Gonzalez &lt;aleixpol@kde.org&gt;
Copyright © 2020 Carlos Garnacho &lt;carlosg@gnome.org&gt;
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-activation/qt_attribution.json`

## Wayland xdg-decoration Protocol

- **Description**: The xdg-decoration protocol allows a compositor to announce support for server-side decorations.
- **QtUsage**: Used in the Qt Wayland Compositor API, and the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: unstable v1, version 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2018 Simon Ser
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-decoration/qt_attribution.json`

## Wayland xdg-toplevel-icon Protocol

- **Description**: The xdg-toplevel-icon protocol allows a compositor to announce support for window icons.
- **QtUsage**: Used in the Qt Wayland Compositor API, and the Qt Wayland platform plugin.
- **Homepage**: https://wayland.freedesktop.org
- **Version**: version 1
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2024 Matthias Klumpp 2024 David Edmundson
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/xdg-toplevel-icon/qt_attribution.json`

## WebGradients

- **Description**: WebGradients is a free collection of 180 linear gradients.
- **QtUsage**: Used in Qt GUI to provide presets for QGradient.
- **Homepage**: https://webgradients.com/
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: LICENSE.WEBGRADIENTS.txt
- **Copyright**: Copyright (c) 2017 itmeo
- **Qt source record**: `qt/qtbase@v6.11.1:util/gradientgen/qt_attribution.json`

## Wintab API

- **Description**: Wintab is a de facto API for pointing devices on Windows.
- **QtUsage**: Used in the Qt platform plugin for Windows. Configure with -no-feature-tabletevent to avoid.
- **License**: LCS-Telegraphics License
- **LicenseId**: LicenseRef-Lcs-Telegraphics
- **Copyright**: Copyright 1991-1998 by LCS/Telegraphics.
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wintab/qt_attribution.json`

## Wlr Data Control Unstable V1 Protocol

- **Description**: This protocol allows a privileged client to control data devices.
- **QtUsage**: Used in the Qt Wayland platform plugin
- **Homepage**: https://gitlab.freedesktop.org/wlroots/wlr-protocols/
- **Version**: 2
- **License**: MIT License
- **LicenseId**: MIT
- **LicenseFile**: ../MIT_LICENSE.txt
- **Copyright**: Copyright © 2018 Simon Ser
Copyright © 2019 Ivan Molodetskikht
- **Qt source record**: `qt/qtbase@v6.11.1:src/3rdparty/wayland/protocols/wlr-data-control/qt_attribution.json`

## X Server helper

- **Description**: Code from X11's region.h, Region.c, poly.h, and PolyReg.c
- **QtUsage**: Used in Qt GUI (QRegion).
- **Homepage**: https://www.x.org/
- **License**: X11 License and Historical Permission Notice and Disclaimer
- **LicenseId**: X11 AND HPND
- **LicenseFile**: LICENSE.XCONSORTIUM.txt
- **Copyright**: Copyright (c) 1987, 1988 X Consortium; Copyright 1987, 1988 by Digital Equipment Corporation, Maynard, Massachusetts.
- **Qt source record**: `qt/qtbase@v6.11.1:src/gui/painting/qt_attribution.json`

## XSVG

- **Description**: Some code for arc handling is derived from code from the XSVG project.
- **QtUsage**: Used in the Qt SVG library.
- **License**: Historical Permission Notice and Disclaimer - sell variant
- **LicenseId**: HPND-sell-variant
- **LicenseFile**: LICENSE.XSVG.txt
- **Copyright**: Copyright 2002 USC/Information Sciences Institute
- **Qt source record**: `qt/qtsvg@v6.11.1:src/svg/qt_attribution.json`
