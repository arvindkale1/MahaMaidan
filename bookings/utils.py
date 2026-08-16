import datetime


def generate_slots_for_date(turf):
    """
    Build the list of (start_time, end_time) tuples for one operating day,
    based on the turf's opening_time/closing_time/slot_duration_minutes.
    Purely computed — no DB rows are created until a Booking is made.
    """
    slots = []
    duration = datetime.timedelta(minutes=turf.slot_duration_minutes)

    current = datetime.datetime.combine(datetime.date.today(), turf.opening_time)
    closing = datetime.datetime.combine(datetime.date.today(), turf.closing_time)

    while current + duration <= closing:
        start = current.time()
        end = (current + duration).time()
        slots.append((start, end))
        current += duration

    return slots
