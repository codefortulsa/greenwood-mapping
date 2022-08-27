import ast
import logging
from datetime import timedelta

from configurations import values


def cast_timedelta(self, value, **params):
    return timedelta(**value)


class TimeDeltaValue(values.CastingMixin, values.Value):
    """Use dict kwargs to get timedelta value"""

    # TODO: assert timedeta type
    caster = cast_timedelta

    def to_python(self, value):
        try:
            evaled_value = ast.literal_eval(value)
        except ValueError:
            raise ValueError(self.message.format(value))
        if not isinstance(evaled_value, dict):
            raise ValueError(self.message.format(value))
        return super().to_python(evaled_value)


def cast_log_level(self, value, **params):
    if value is None:
        return None
    try:
        keys = logging._levelToName.values()
        assert value in keys
        level = getattr(logging, value)
        assert type(level) == int
    except AttributeError as e:
        raise Exception(f"Unable to find logging level: {value}.")
    except AssertionError as e:
        raise Exception(f"Logging level {value} not found.")


class LogLevelValue(values.CastingMixin, values.Value):
    caster = cast_log_level
