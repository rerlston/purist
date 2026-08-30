from abc import ABC, abstractmethod

from purist.models.lexer_models import LexerResult, LexerState


class BaseMatcher(ABC):
    @abstractmethod
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        pass
