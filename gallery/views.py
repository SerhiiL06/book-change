from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Gallery, ImageTag

from .forms import UploadImageForm


class GalleryView(ListView):
    template_name = "gallery/gallery.html"
    model = Gallery

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = ImageTag.objects.all()
        return context


class UploadImageToGalleryView(CreateView):
    template_name = "gallery/upload_image.html"
    model = Gallery
    form_class = UploadImageForm
    success_url = reverse_lazy("users:options")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()

        return super().form_valid(form)
