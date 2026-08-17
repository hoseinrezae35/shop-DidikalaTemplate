from django.views.generic import TemplateView


class OrderView(TemplateView):
    template_name = 'order/checkout.html'


# def next_step(request):
#     if request.method == 'POST':
#         address_id = request.POST.get('address')
#         if not address_id:
#             messages.error(request, 'لطفاً یک آدرس را انتخاب کنید')
#             return redirect('current-step')
#
#         try:
#             address = request.user.addresses.get(id=address_id)
#             # ادامه فرآیند
#         except Address.DoesNotExist:
#             messages.error(request, 'آدرس معتبر نیست')
#             return redirect('current-step')
