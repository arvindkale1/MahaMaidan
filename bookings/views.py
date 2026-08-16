import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from turfs.models import Turf
from .models import Booking


@login_required
def create_booking(request, turf_pk):
    """
    Book a single slot on a turf. Slot comes from the turf detail page as
    date/start_time/end_time in the query string or POST body.
    """
    turf = get_object_or_404(Turf, pk=turf_pk, is_active=True)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        start_str = request.POST.get('start_time')
        end_str = request.POST.get('end_time')

        try:
            date = datetime.date.fromisoformat(date_str)
            start_time = datetime.time.fromisoformat(start_str)
            end_time = datetime.time.fromisoformat(end_str)
        except (TypeError, ValueError):
            messages.error(request, 'Invalid slot selection.')
            return redirect('turfs:turf_detail', pk=turf.pk)

        duration_hours = (
            datetime.datetime.combine(date, end_time)
            - datetime.datetime.combine(date, start_time)
        ).seconds / 3600

        booking = Booking(
            user=request.user,
            turf=turf,
            date=date,
            start_time=start_time,
            end_time=end_time,
            status=Booking.Status.CONFIRMED,
            total_price=turf.price_per_hour * round(duration_hours, 2),
        )
        try:
            booking.save()
        except ValidationError as exc:
            messages.error(request, ' '.join(exc.messages))
            return redirect('turfs:turf_detail', pk=turf.pk)

        messages.success(request, f'Booked {turf.name} on {date} at {start_time}.')
        return redirect('bookings:my_bookings')

    return redirect('turfs:turf_detail', pk=turf.pk)


class MyBookingsView(LoginRequiredMixin, ListView):
    """Booking history and status for the logged-in customer."""
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('turf')


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST' and booking.status == Booking.Status.CONFIRMED:
        booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, 'Booking cancelled.')
    return redirect('bookings:my_bookings')


class TurfBookingsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """A turf owner's view of all bookings made on one of their turfs."""
    model = Booking
    template_name = 'bookings/turf_bookings.html'
    context_object_name = 'bookings'

    def test_func(self):
        self.turf = get_object_or_404(Turf, pk=self.kwargs['turf_pk'])
        return self.request.user == self.turf.owner

    def get_queryset(self):
        return Booking.objects.filter(turf=self.turf).select_related('user')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['turf'] = self.turf
        return ctx
