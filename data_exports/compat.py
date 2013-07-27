# -*- coding: utf-8 -*-

import sys

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    python_2_unicode_compatible = lambda x: x


text_type = str
if sys.version < '3':
    text_type = unicode  # noqa
