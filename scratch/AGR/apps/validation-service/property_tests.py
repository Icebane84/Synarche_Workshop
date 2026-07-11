from hypothesis import given
from hypothesis.strategies import text


@given(text())
def parser_should_never_crash(source):

    #
    # Placeholder.
    # Later this imports ParserEngine
    # and verifies robustness against
    # randomized input.
    #

    assert source is not None