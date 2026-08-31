from dataclasses import dataclass, replace
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Logger:
    _division_length: int = 125
    _indentation_level: int = 0
    _tab_size: int = 4

    @property
    def division_length(self) -> int:
        return self._division_length

    @property
    def indentation_level(self) -> int:
        return self._indentation_level

    @property
    def tab_size(self) -> int:
        return self._tab_size

    def with_division_length(self, division_length: int) -> "Logger":
        return replace(self, _division_length=division_length)

    def with_indentation_level(self, indentation_level: int) -> "Logger":
        return replace(self, _indentation_level=indentation_level)

    def with_tab_size(self, tab_size: int) -> "Logger":
        return replace(self, _tab_size=tab_size)

    def increment_indentation_level(self, inc: int = 1) -> "Logger":
        return replace(self, _indentation_level=self.indentation_level + inc)
    
    def log(self, message: str) -> "Logger":
        indent = ' ' * (self.indentation_level * self.tab_size)
        print(f"{indent}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {message}")
        return replace(self)

    def log_division(self) -> "Logger":
        indent = ' ' * (self.indentation_level * self.tab_size)
        print(f"{indent}{'-'*self.division_length}")
        return replace(self)

    class _SectionContext:
        def __init__(self, logger, entry_msg: str | None = None, exit_msg: str | None = None, error_msg: str | None = None):
            self.logger = logger
            self.entry_msg = entry_msg
            self.exit_msg = exit_msg
            self.error_msg = error_msg

        def __enter__(self):
            self.logger.log_division()
            self.logger.log(self.entry_msg)
            return self.logger

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self.logger.log(self.exit_msg)
                self.logger.log_division()
            else:
                self.logger.log(self.error_msg)
                self.logger.log_division()
            return False  # propagate exception

    def section(
        self,
        entry_msg: str | None = None,
        exit_msg: str | None = None,
        error_msg: str | None = None
    ) -> "_SectionContext":
        return Logger._SectionContext(self, entry_msg, exit_msg, error_msg)