from django.db import models


class FuzzyDateRangeMixin(models.Model):
    """Abstract: a date range whose endpoints can be fuzzy.

    Every range has two endpoints (`start` and `end`), and each endpoint
    has two fields — `earliest` (the earliest possible date the event
    could have occurred) and `latest` (the latest). For an exact date
    `earliest == latest`. For a fuzzy date the window between the two
    expresses uncertainty.

    Renderers use the window width to animate fade-in/out or hatch
    fuzzy regions; records stay clickable regardless. Open-ended
    endpoints (still ongoing / unknown) leave both fields null.
    """

    start_earliest = models.DateTimeField(null=True, blank=True)
    start_latest = models.DateTimeField(null=True, blank=True)
    end_earliest = models.DateTimeField(null=True, blank=True)
    end_latest = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def start_is_estimated(self) -> bool:
        if self.start_earliest is None and self.start_latest is None:
            return False
        return self.start_earliest != self.start_latest

    @property
    def end_is_estimated(self) -> bool:
        if self.end_earliest is None and self.end_latest is None:
            return False
        return self.end_earliest != self.end_latest
