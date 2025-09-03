from django.shortcuts import render, get_object_or_404
from .models import Client, Document

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'fillingsystem/client_list.html', {'clients': clients})

def document_list(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    documents = client.documents.all()
    return render(request, 'fillingsystem/document_list.html', {'client': client, 'documents': documents})
