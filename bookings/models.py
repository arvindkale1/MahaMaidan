from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    """
    One reserved time-slot on a turf.

    Double-booking prevention has two layers:
      1. DB-level: unique_together on (turf, date, start_time) — the
         database itself refuses a second confirmed row for the same slot.
      2. App-level: clean() also rejects overlapping ranges in case a turf's
         slot_duration_minutes changes after older bookings were made.
    """

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings'
    )
    turf = models.ForeignKey(
        'turfs.Turf', on_delete=models.CASCADE, related_name='bookings'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CONFIRMED)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['turf', 'date', 'start_time'],
                condition=~models.Q(status='CANCELLED'),
                name='unique_active_slot_per_turf',
            )
        ]

    def __str__(self):
        return f"{self.turf.name} — {self.date} {self.start_time}–{self.end_time} ({self.user})"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.')

        overlapping = Booking.objects.filter(
            turf=self.turf,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(status=self.Status.CANCELLED)

        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError('This slot overlaps with an existing booking.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
