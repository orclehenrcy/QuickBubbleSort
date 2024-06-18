﻿
Copyright (c) 2017-present TwitchIO

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import datetime
from typing import Optional, Union, Set, TYPE_CHECKING

from .abcs import Messageable
from .chatter import Chatter, PartialChatter
from .models import BitsLeaderboard

if TYPE_CHECKING:
    from .websocket import WSConnection
    from .user import User


__all__ = ("Channel",)


class Channel(Messageable):
    __slots__ = ("_name", "_ws", "_message")

    __messageable_channel__ = True

    def __init__(self, name: str, websocket: "WSConnection"):
        self._name = name
        self._ws = websocket

    def __eq__(self, other):
        return other.name == self._name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<Channel name: {self.name}>"

    def _fetch_channel(self):
        return self  # Abstract method

    def _fetch_websocket(self):
        return self._ws  # Abstract method

    def _fetch_message(self):
        return self._message  # Abstract method

    def _bot_is_mod(self):
Copyright (c) 2017-present TwitchIO

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import datetime
from typing import Optional, Union, Set, TYPE_CHECKING

from .abcs import Messageable
from .chatter import Chatter, PartialChatter
from .models import BitsLeaderboard

if TYPE_CHECKING:
    from .websocket import WSConnection
    from .user import User


__all__ = ("Channel",)


class Channel(Messageable):
    __slots__ = ("_name", "_ws", "_message")

    __messageable_channel__ = True

    def __init__(self, name: str, websocket: "WSConnection"):
        self._name = name
        self._ws = websocket

    def __eq__(self, other):
        return other.name == self._name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<Channel name: {self.name}>"

    def _fetch_channel(self):
        return self  # Abstract method

    def _fetch_websocket(self):
        return self._ws  # Abstract method

    def _fetch_message(self):
        return self._message  # Abstract method

    def _bot_is_mod(self):
        try:
            cache = self._ws._cache[self.name]  # noqa
        except KeyError:
            return False

        for user in cache:
            if user.name == self._ws.nick:
                try:
                    mod = user.is_mod
                except AttributeError:
                    return False

                return mod

    @property
    def name(self) -> str:
        """The channel name."""
        return self._name

    @property
    def chatters(self) -> Optional[Set[Union[Chatter, PartialChatter]]]:
        """The channels current chatters."""
        try:
            chatters = self._ws._cache[self._name]  # noqa
        except KeyError:
            return None

        return chatters

    def get_chatter(self, name: str) -> Optional[Union[Chatter, PartialChatter]]:
        """Retrieve a chatter from the channels user cache.

        Parameters
        -----------
        name: str
            The chatter's name to try and retrieve.

        Returns
        --------
        Union[:class:`twitchio.chatter.Chatter`, :class:`twitchio.chatter.PartialChatter`]
            Could be a :class:`twitchio.user.PartialChatter` depending on how the user joined the channel.
            Returns None if no user was found.
        """
        name = name.lower()

        try:
            cache = self._ws._cache[self._name]  # noqa
            for chatter in cache:
                if chatter.name == name:
                    return chatter

            return None
        except KeyError:
            return None
