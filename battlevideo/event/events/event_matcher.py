import abc
from typing import Union, Tuple

from battlevideo.event.events.event import Event
from battlevideo.event.locale import Locale


class EventMatcher(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def matches(self, text: str, locale: Locale) -> Tuple[bool, Union[int, None], Union[Event, None]]:
        pass
