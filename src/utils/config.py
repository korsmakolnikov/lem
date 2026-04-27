import os
from dataclasses import dataclass

from dotenv import load_dotenv

# LOAD ENV
load_dotenv(override=True)


@dataclass
class YouTrackConfig:
    url: str
    token: str
    sprint_prefix: str = "sprint-"
    story_points_field: str = "Story Points"


@dataclass
class SimulationConfig:
    default_sprints: int = 10
    n_simulations: int = 10000


@dataclass
class AppConfig:
    youtrack: YouTrackConfig
    simulations: SimulationConfig


# HELPERS
def _get_str(name: str, required: bool = True, default: str | None = None) -> str:
    value = os.getenv(name, default)
    value_is_none = value is None
    default_is_none = default is None

    if value_is_none:
        if required and default_is_none:
            raise ValueError(f"Missing required env variables: {name}")
        value = default

    assert value is not None
    return value.strip()


def _get_int(name: str, required: bool = True, default: int | None = None) -> int:
    value = os.getenv(name)

    if value is None:
        if required and default is None:
            raise ValueError(f"Missing required env variable: {name}")
        assert default is not None
        return default

    try:
        return int(value)
    except ValueError as err:
        raise ValueError(f"Invalid int for env variable {name}: {value}") from err


# FACTORY
YOUTRACK_URL = "YOUTRACK_URL"
YOUTRACK_TOKEN = "YOUTRACK_TOKEN"
SPRINT_PREFIX = "SPRINT_PREFIX"
STORY_POINTS_FIELD = "STORY_POINTS_FIELD"
DEFAULT_SPRINTS = "DEFAULT_SPRINTS"
N_SIMULATION = "N_SIMULATION"


def load_config() -> AppConfig:
    youtrack = YouTrackConfig(
        url=_get_str(YOUTRACK_URL),
        token=_get_str(YOUTRACK_TOKEN),
        sprint_prefix=_get_str(name=SPRINT_PREFIX, default="sprint-"),
        story_points_field=_get_str(name=STORY_POINTS_FIELD, default="Story Points"),
    )

    simulations = SimulationConfig(
        default_sprints=int(_get_int(name=DEFAULT_SPRINTS, default=10)),
        n_simulations=int(_get_int(name=N_SIMULATION, default=10000)),
    )

    return AppConfig(youtrack=youtrack, simulations=simulations)
