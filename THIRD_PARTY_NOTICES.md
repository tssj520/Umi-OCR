# Copyright and bundled runtime notices

Umi-OCR is originally developed by **hiroi-sora and contributors** and distributed under the MIT license in [LICENSE](LICENSE). The translation enhancement is maintained by [tssj520](https://github.com/tssj520/Umi-OCR); it is a community fork, not an official upstream release.

The Windows portable build reuses the runtime and RapidOCR plugin distributed with upstream `Umi-OCR_Rapid_v2.1.5.7z`. Their files and included license notices are preserved. These third-party components have their own licenses; Umi-OCR's MIT license does not replace them.

Source and project information for the bundled components:

- [Windows runtime and build instructions](https://github.com/hiroi-sora/Umi-OCR_runtime_windows)
- [Umi-OCR engine plugins](https://github.com/hiroi-sora/Umi-OCR_plugins)
- [Python](https://www.python.org/downloads/source/) — license included in `UmiOCR-data/runtime/LICENSE.txt`.
- [Qt for Python / PySide2](https://code.qt.io/cgit/pyside/pyside-setup.git/) and [Qt](https://code.qt.io/cgit/qt/) — use the applicable upstream LGPL/GPL/commercial licensing terms; bundled DLLs are not modified.
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) — its included `COPYING` and applicable AGPL/commercial terms remain in force.
- [Pillow](https://github.com/python-pillow/Pillow), [fontTools](https://github.com/fonttools/fonttools), [psutil](https://github.com/giampaolo/psutil), [pynput](https://github.com/moses-palmer/pynput), [six](https://github.com/benjaminp/six), and [zxing-cpp](https://github.com/zxing-cpp/zxing-cpp) — retain their original licenses and notices where bundled.

The OCR engine executables, model files, Python runtime, and third-party libraries are reused without modification. Translation integration uses Python's standard library and adds no new binary dependency. Source for this fork is available at <https://github.com/tssj520/Umi-OCR>; the original project is <https://github.com/hiroi-sora/Umi-OCR>.
