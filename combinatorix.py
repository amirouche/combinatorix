"""Combinatorix"""


class CombinatorixException(Exception):
    pass


class ParseFailure(CombinatorixException):

    def __init__(self, stream):
        self.stream = stream


class EndOfStream(ParseFailure):
    # Here we inherit ParseFailure to streamline the code
    # and avoid to check everywhere for EndOfStream (EOS).
    # Instead, if EOS is not expected it's considered an error.
    pass


END_OF_STREAM = object()


class Stream(object):

    def __init__(self, string, position=0):
        self.string = string
        self.position = position

    def next(self):
        return type(self)(self.string, self.position + 1)

    def peek(self):
        try:
            return self.string[self.position]
        except IndexError:
            raise EndOfStream(self)


# combinators

def sequence(*parsers):
    """Return a closure that takes as argument a ``Stream``
    that will be parsed one after the other in sequence
    by the ``parsers``."""
    def closure(stream):
        out = list()
        for parser in parsers:
            item, stream = parser(stream)
            out.append(item)
        return out, stream
    return closure


def either(*parsers):
    """Return a closure that takes as argument a ``Stream``
    that will be parsed by the first parser of ``parsers``
    that succeed."""
    def closure(stream):
        for parser in parsers:
            try:
                out, stream = parser(stream)
            except ParseFailure:
                continue
            else:
                break
        # if no parser succeed, the combinator fails
        else:
            raise ParseFailure(stream)
        return out, stream
    return closure


def zero_or_more(parser):
    """Return a closure that takes as argument a ``Stream``
    that will be parsed by ``parser`` *zero or more* times

    .. warning: this can run forever!
    """

    def closure(stream):
        out = list()
        while True:
            try:
                item, stream = parser(stream)
            except ParseFailure:
                return out, stream
            else:
                out.append(item)

    return closure


def one_or_more(parser):
    """Return a closure that takes as argument a ``Stream``
    that will be parsed by ``parser`` *one or more* times

    .. warning: this can run forever!
    """
    def closure(stream):
        combined = sequence(parser, zero_or_more(parser))
        out, stream = combined(stream)
        # linearize the output
        head, tail = out
        tail.insert(0, head)
        return tail, stream
    return closure


def when(predicate, parser):
    """Return a closure that takes as argument a ``Stream``
    that will be parsed using `parser` only if `predicate` succeed.

    `predicate` doesn't consume the stream.
    """
    def closure(stream):
        predicate(stream)
        return parser(stream)
    return closure


def unless(predicate, parser):
    """Return a closure that takes as argument a ``Stream``
    that will be parsed using `parser` only if `predicate` fails.

    `predicate` doesn't consume the stream.
    """
    def closure(stream):
        try:
            predicate(stream)
        except ParseFailure:
            return parser(stream)
        else:
            raise ParseFailure(stream)

    return closure

# parsers


def nop(stream):
    return '', stream.next()


def anything(stream):
    return stream.peek(), stream.next()


def space(stream):
    char = stream.peek()
    if char.isspace():
        return char, stream.next()
    else:
        raise ParseFailure(stream)


def end_of_stream(stream):
    """Parser that succeed if the stream is fully consumed"""
    try:
        stream.peek()
    except EndOfStream:
        return END_OF_STREAM, stream
    else:
        raise ParseFailure(stream)


def char(char):
    def parser(stream):
        other = stream.peek()
        if other == char:
            return char, stream.next()
        else:
            raise ParseFailure(stream)
    return parser

def apply(func):
    """Apply ``func`` on the output of ``parser``"""
    def parser(parser):
        def closure(stream):  # functor factory ftw!
            out, stream = parser(stream)
            return func(out), stream
        return closure
    return parser


def string(string):
    def parser(stream):
        parser = sequence(*map(char, list(string)))
        out, stream = parser(stream)
        return ''.join(out), stream
    return parser


def combinatorix(string, parser):
    stream = Stream(string)
    out, stream = parser(stream)
    # check that the input was fully consumed
    try:
        end_of_stream(stream)
    except ParseFailure:
        raise ParseFailure(stream)
    else:
        return out


# tweet parser

join = apply(lambda x: ''.join(x))

nonspace = one_or_more(unless(space, anything))
nonspace = join(nonspace)


def href(parser):
    def closure(stream):
        out, stream = parser(stream)
        out = '<a href="%s">%s</a>' % (out, out)
        return out, stream
    return closure


url = sequence(either(string('http://'), string('https://')), nonspace)
url = href(join(url))


hashtag = sequence(char('#'), nonspace)
hashtag = href(join(hashtag))

fragment = either(url, hashtag, nonspace, space)

tweet_parser = one_or_more(fragment)
tweet_parser = join(tweet_parser)


def tweet(string):
    return combinatorix(string, tweet_parser)
