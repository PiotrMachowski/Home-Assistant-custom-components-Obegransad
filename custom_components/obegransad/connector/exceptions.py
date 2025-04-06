from abc import ABC

from typing import Self


class ObegransadException(Exception, ABC):
    pass


class ObegransadMissingDataException(ObegransadException):
    def __init__(self, *missing_fields: str) -> None:
        super().__init__(
            f'Missing data for required fields: {", ".join(missing_fields)}'
        )


class ObegransadApiException(ObegransadException):
    def __init__(self: Self, status_code: int, response: str) -> None:
        super().__init__(f"Api error: {status_code}")
        self.status_code = status_code
        self.response = response
