from math import ceil
from backend.models import Attendance


def compute_attendance_insights(att_record: Attendance):
    """
    Given an Attendance ORM object, compute:
    - current percentage
    - approximate number of extra continuous classes needed to reach threshold

    Formula:
      find smallest x such that (attended + x) / (total + x) >= threshold%
    """
    attended = att_record.attended
    total = att_record.total_classes
    threshold = att_record.threshold

    if total <= 0:
        return 0.0, 0

    current_pct = (attended / total) * 100

    t = threshold / 100  # convert to fraction
    if t >= 1:
        needed = 0
    else:
        # (attended + x) / (total + x) >= t
        # => x >= (t*total - attended) / (1 - t)
        numerator = (t * total) - attended
        denominator = 1 - t
        needed = ceil(max(0, numerator / denominator))

    return current_pct, needed
