import abc

from battlevideo.event.locale import Locale


class EventMatcher(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def matches(self, text: str, locale: Locale) -> bool:
        pass