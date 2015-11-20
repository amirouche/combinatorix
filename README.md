# Combinatorix

Very simple parser combinator library licensed under LGPLv2.1 or later.

Tested with Python 2.7 and Python 3.4.


## Example

There is a `tweet` parser included in `combinatorix` module.
Start microblogging with:

``` python
from combinatorix import tweet

messsage = 'Ombi Natori combine combinators using combinatorix #Python '
message += 'Get it at https://github.com/amirouche/combinatorix#combinatorix'
tweet(message)
```
