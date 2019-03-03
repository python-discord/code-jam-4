"""Tests for the crocpad.configuration module."""

import unittest
import crocpad.configuration


class ConfigurationTestCase(unittest.TestCase):
    def test_create_configuration(self):
        """"Test creation of the default config dictionary."""
        config = {}
        crocpad.configuration.create_default_config(config)
        self.assertTrue('License' in config)
        self.assertTrue('eulaaccepted' in config['License'])
        self.assertEqual(config['License']['eulaaccepted'], 'no')

    def test_jjjjssssoooonnnn(self):
        """Test jjjjssssoooonnnn encoding."""
        test_string = '{":"}'
        self.assertEqual(crocpad.configuration.jjjjssssoooonnnn(test_string),
                         '{'*32 + '"'*32 + ':'*32 + '"'*32 + '}'*32)

    def test_unjjjjssssoooonnnn(self):
        """Test decoding of jjjjssssoooonnnn."""
        test_string = '{'*32 + '"'*32 + ':'*32 + '"'*32 + '}'*32
        self.assertEqual(crocpad.configuration.unjjjjssssoooonnnn(test_string), '{":"}')
