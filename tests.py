from unittest import TestCase

# utils
from combinatorix import Stream
from combinatorix import ParseFailure

# combinators
from combinatorix import when
from combinatorix import unless
from combinatorix import either
from combinatorix import sequence
from combinatorix import one_or_more
from combinatorix import zero_or_more
from combinatorix import end_of_stream

# main
from combinatorix import combinatorix

# parser
from combinatorix import char
from combinatorix import string
from combinatorix import tweet


class TestCombinatorix(TestCase):

    def test_char_ok(self):
        parser = char('c')
        stream = Stream('c')
        out, stream = parser(stream)
        self.assertEqual(out, 'c')
        self.assertEqual(stream.position, 1)

    def test_char_fail(self):
        parser = char('x')
        stream = Stream('c')
        with self.assertRaises(ParseFailure):
            parser(stream)

    def test_string_ok(self):
        OmbiNatori = 'Ombi Natori'
        parser = string(OmbiNatori)
        stream = Stream(OmbiNatori)
        out, stream = parser(stream)
        self.assertEqual(out, OmbiNatori)
        self.assertEqual(stream.position, len(OmbiNatori))

    def test_string_fails(self):
        OmbiNatori = 'Ombi Natori'
        parser = string(OmbiNatori)
        stream = Stream('Combinatorix')
        with self.assertRaises(ParseFailure):
            parser(stream)

    def test_sequence_ok_one(self):
        c = char('c')
        ccc = sequence(c, c, c)
        stream = Stream('ccc')
        out, stream = ccc(stream)
        self.assertEqual(out, list('ccc'))
        self.assertEqual(stream.position, 3)

    def test_sequence_ok_two(self):
        c = char('c')
        ccc = sequence(c, c, c)
        stream = Stream('cccc')
        out, stream = ccc(stream)
        self.assertEqual(out, list('ccc'))
        self.assertEqual(stream.position, 3)

    def test_sequence_fails_one(self):
        c = char('c')
        ccc = sequence(c, c, c)
        stream = Stream('xxx')
        with self.assertRaises(ParseFailure):
            ccc(stream)

    def test_sequence_fails_two(self):
        c = char('c')
        ccc = sequence(c, c, c)
        stream = Stream('ccx')
        with self.assertRaises(ParseFailure):
            ccc(stream)

    def test_zero_or_more_ok_one(self):
        c = char('c')
        parser = zero_or_more(c)
        stream = Stream('')
        out, stream = parser(stream)
        self.assertEqual(out, [])
        self.assertEqual(stream.position, 0)

    def test_zero_or_more_ok_two(self):
        c = char('c')
        parser = zero_or_more(c)
        stream = Stream('ccc')
        out, stream = parser(stream)
        self.assertEqual(out, ['c'] * 3)
        self.assertEqual(stream.position, 3)

    def test_zero_or_more_ok_three(self):
        c = char('c')
        parser = zero_or_more(c)
        stream = Stream('combinatorix')
        out, stream = parser(stream)
        self.assertEqual(out, ['c'])
        self.assertEqual(stream.position, 1)

    def test_one_or_more_ok_one(self):
        c = char('c')
        parser = one_or_more(c)
        stream = Stream('combinatorix')
        out, stream = parser(stream)
        self.assertEqual(out, ['c'])
        self.assertEqual(stream.position, 1)

    def test_one_or_more_ok_two(self):
        c = char('c')
        parser = one_or_more(c)
        stream = Stream('cccombinatorix')
        out, stream = parser(stream)
        self.assertEqual(out, ['c', 'c', 'c'])
        self.assertEqual(stream.position, 3)

    def test_one_or_more_fails(self):
        c = char('c')
        parser = one_or_more(c)
        stream = Stream('xxx')
        with self.assertRaises(ParseFailure):
            parser(stream)

    def test_either_ok_one(self):
        c = char('c')
        x = char('x')
        parser = either(c, x)
        stream = Stream('combinatorix')
        out, stream = parser(stream)
        self.assertEqual(out, 'c')
        self.assertEqual(stream.position, 1)

    def test_either_ok_two(self):
        c = char('c')
        x = char('x')
        parser = either(c, x)
        stream = Stream('xirotanibmoc')
        out, stream = parser(stream)
        self.assertEqual(out, 'x')
        self.assertEqual(stream.position, 1)

    def test_either_fails(self):
        c = char('c')
        x = char('x')
        parser = either(c, x)
        stream = Stream('i')
        with self.assertRaises(ParseFailure):
            parser(stream)

    def test_when_ok(self):
        c = char('c')
        parser = when(c, c)
        stream = Stream('c')
        out, stream = parser(stream)
        self.assertEqual(out, 'c')
        self.assertEqual(stream.position, 1)

    def test_unless_ok(self):
        c = char('c')
        parser = unless(end_of_stream, c)
        stream = Stream('c')
        out, stream = parser(stream)
        self.assertEqual(out, 'c')
        self.assertEqual(stream.position, 1)


class TestTweetParser(TestCase):

    def test_tweet_simple(self):
        input = 'Ombi Natori combine combinators using combinatorix'
        output = tweet(input)
        self.assertEqual(input, output)

    def test_tweet_hashtag(self):
        input = 'Ombi Natori combine combinators using combinatorix #Python'
        output = tweet(input)
        hashtag = '<a href="#Python">#Python</a>'
        expected = 'Ombi Natori combine combinators using combinatorix %s'
        expected = expected % hashtag
        self.assertEqual(output, expected)

    def test_tweet_link(self):
        input = 'Ombi Natori combine combinators using combinatorix #Python'
        input += ' Get it at https://github.com/amirouche/combinatorix#combinatorix'
        output = tweet(input)
        hashtag = '<a href="#Python">#Python</a>'
        expected = 'Ombi Natori combine combinators using combinatorix %s'
        expected = expected % hashtag
        url = 'https://github.com/amirouche/combinatorix#combinatorix'
        expected += ' Get it at <a href="%s">%s</a>' % (url, url)
        self.assertEqual(output, expected)
