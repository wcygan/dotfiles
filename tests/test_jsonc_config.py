"""Regression cases for the parser installed in the config-checks Nix shell."""

import importlib.util
import tempfile
import unittest
from contextlib import chdir
from pathlib import Path

from scripts.config_checks import validate


@unittest.skipUnless(importlib.util.find_spec("rapidjson"), "requires the config-checks Nix shell")
class JsoncConfigTest(unittest.TestCase):
    def test_comments_and_trailing_commas_but_no_trailing_content(self):
        # check_kind matches repository-relative paths.
        with tempfile.TemporaryDirectory() as directory, chdir(directory):
            config = Path("config/zed/settings.json")
            config.parent.mkdir(parents=True)
            valid = '// User settings\n{"editor": true, /* enabled */ }'
            config.write_text(valid)
            validate(config)
            for extra in ("]", "{}", " null"):
                with self.subTest(extra=extra), self.assertRaises(ValueError):
                    config.write_text(valid + extra)
                    validate(config)
            config.write_text('{"size": NaN}')
            with self.assertRaises(ValueError):
                validate(config)
