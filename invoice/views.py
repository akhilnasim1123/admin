from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from cart.models import OrderedItems


def order_details_user_side(request,id):
    order = OrderedItems.objects.get(id=id)
    payment=order.payment
    payment_id=order.payment_id
    
    context = {
        'order':order,
        'payment':payment,
        'payment_id':payment_id,
    }

    return render(request,'userprofile/order_details.html',context)
#     return HttpResponse(pdf,content_type="application/pdf")


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



class ViewPDF(View):
	def get(self, request,id, *args, **kwargs):
            order = OrderedItems.objects.get(id=id)

            context = {
            'order':order,
            }

            pdf = render_to_pdf('userprofile/order_details.html', context)
            return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request,id, *args, **kwargs):
            order = OrderedItems.objects.get(id=id)
            context = {
            'order':order,
 
            }
            
            pdf = render_to_pdf('userprofile/order_details.html', context)

            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("torque.in")
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response