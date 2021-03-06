from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from contacts.models import Contact
from contacts.forms import ContactForm
from contacts.serializers import ContactSerializer


def contacts(request):
    user = request.user

    contacts = Contact.objects.filter(user=user)

    return render_to_response('contacts/index.html', {
        'user': user,
        'contacts': contacts,
    }, RequestContext(request))


def contacts_add(request):
    if request.method == 'POST':
        form = ContactForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_contact = form.save()
            return HttpResponseRedirect("/contacts")
    else:
        form = ContactForm(user=request.user)

    return render_to_response("contacts/new.html", {
        'form': form
    }, RequestContext(request))


class ContactList(generics.ListCreateAPIView):
    model = Contact
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
