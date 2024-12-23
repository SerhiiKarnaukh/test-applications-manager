import datetime
from .models import Order


def create_order_from_form(form, user_profile, grand_total, tax, request):
    """
    Creates an Order object based on a form and additional data.
    """
    order = Order(
        user=user_profile,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        phone=form.cleaned_data['phone'],
        email=form.cleaned_data['email'],
        address_line_1=form.cleaned_data['address_line_1'],
        address_line_2=form.cleaned_data['address_line_2'],
        country=form.cleaned_data['country'],
        state=form.cleaned_data['state'],
        city=form.cleaned_data['city'],
        order_note=form.cleaned_data['order_note'],
        order_total=grand_total,
        tax=tax,
        ip=request.META.get('REMOTE_ADDR'),
    )
    order.save()
    return order


def generate_order_number(order):
    """
    Generates a unique order number.
    """
    current_date = datetime.date.today().strftime("%Y%m%d")
    return f"{current_date}{order.id}"
