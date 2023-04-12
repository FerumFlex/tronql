from enum import StrEnum

import strawberry


@strawberry.enum
class StatsGroup(StrEnum):
    hour = "hour"
    day = "day"
