# Apache License 2.0

import pytest

from datetime import datetime, timezone, timedelta
import os
from typing import Optional

import cesiumpy


@pytest.fixture
def cesium_token() -> Optional[str]:
    return os.environ.get("CESIUM_TOKEN")


@pytest.fixture
def asset_id() -> int:
    # return 669199 # OLD
    # return 1250090
    return 1359555  # FIX
    # return 1191175
    # return 1359352


@pytest.fixture
def epoch() -> timedelta:
    return datetime(2022, 1, 1, 0, 0, 0, 0, timezone.utc)


@pytest.fixture
def duration() -> timedelta:
    return timedelta(hours=1.0)
    # return timedelta(seconds=30.0)


@pytest.fixture
def step() -> timedelta:
    return timedelta(seconds=30.0)


@pytest.fixture
def time_interval(
    epoch: datetime,
    duration: timedelta,
) -> cesiumpy.TimeInterval:
    return cesiumpy.TimeInterval(
        start=epoch,
        stop=epoch + duration,
    )


@pytest.fixture
def instants(
    time_interval: cesiumpy.TimeInterval,
    step: timedelta,
) -> list[datetime]:
    instants = [
        time_interval.start + timedelta(seconds=i * step.total_seconds())
        for i in range(
            int(
                (time_interval.stop - time_interval.start).total_seconds()
                / step.total_seconds()
            )
            + 1
        )
    ]

    if not instants:
        return []

    if instants[-1] != time_interval.stop:
        instants.append(time_interval.stop)

    return instants


@pytest.fixture
def sampled_position(
    instants: list[datetime],
) -> cesiumpy.SampledPositionProperty:
    return cesiumpy.SampledPositionProperty(
        samples=[
            (
                instant,
                cesiumpy.Cartesian3.fromDegrees(index, 0.0, 500e3),
                None,
            )
            for (index, instant) in enumerate(instants)
        ],
    )


@pytest.fixture
def sampled_orientation(
    instants: list[datetime],
) -> cesiumpy.SampledProperty:
    return cesiumpy.SampledProperty(
        type=cesiumpy.Quaternion,
        samples=[
            (
                instant,
                cesiumpy.Quaternion.from_heading_pitch_roll(
                    cesiumpy.HeadingPitchRoll(
                        heading=0.0,
                        pitch=cesiumpy.math.to_radians(180.0),
                        roll=0.0,
                    )
                ),
                None,
            )
            for instant in instants
        ],
    )
