#!/usr/bin/env python3
"""
Compatibility wrapper.

The old sitemap generator created JavaScript-only /store?pid= URLs.
Use generate_static_stores.py instead; it creates the static store HTML pages
and writes sitemap.xml with /stores/<slug> URLs.
"""

from generate_static_stores import main

if __name__ == "__main__":
    main()
