from django.db.models.query import Q
from django.shortcuts import render
from .models import Book,Author
from django.views.generic import CreateView,ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import AuthorForm, BookForm


# Create your views here.

class CreateBook(CreateView):

    model = Book
    form_class = BookForm

    template_name = 'admin/create_book.html'

    success_url = reverse_lazy('list_book')

class ListBook(ListView):

    model = Book

    template_name = 'admin/list_book.html'

    context_object_name = 'books'

    paginate_by = 5

class BookDetail(DetailView):

    model = Book

    template_name ='admin/book_detail.html'

    context_object_name = 'book'

class UpdateBook(UpdateView):
    model = Book

    template_name = 'admin/update_book.html'

    form_class = BookForm

    success_url = reverse_lazy('list_book')

class DeleteBook(DeleteView):

    model = Book
    template_name = 'admin/delete_book.html'

    context_object_name = 'book'

    success_url = reverse_lazy('list_book')

def index(request):

    return render(request, 'base.html')

class CreateAuthor(CreateView):

    model = Author
    form_class = AuthorForm

    template_name = 'admin/create_author.html'

    success_url = reverse_lazy('list_book')

class SearchBook(ListView):

    model = Book
    template_name = 'admin/search_book.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')

        return Book.objects.filter(
            Q(title__icontains = query) |
            Q(author__author__icontains = query)
        )
    

