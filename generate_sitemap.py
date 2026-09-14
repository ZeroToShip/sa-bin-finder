#!/usr/bin/env python3
"""
Compatibility wrapper.

The old sitemap generator created JavaScript-only /store?pid= URLs.
Use generate_static_stores.py instead; it creates the static store HTML pages
and writes sitemap.xml with /stores/<slug> URLs.
"""

import utils.net
import utils.clients
import utils.http_session
import utils.transport
import utils.session
from generate_static_stores import main

if __name__ == "__main__":
    main()
