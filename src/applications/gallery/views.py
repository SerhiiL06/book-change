from typing import Any

from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import UploadImageForm
from .models import Gallery, ImageTag


class GalleryView(ListView):
    template_name = "gallery/gallery.html"
    model = Gallery

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = ImageTag.objects.all()
        return context

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset()

        profile = self.kwargs.get("profile_id", None)

        tag_name = self.kwargs.get("tag_name", None)

        if profile is not None:
            queryset = queryset.filter(owner=self.request.user)

        if tag_name is not None:
            queryset = queryset.filter(tags__tag_name=tag_name)

        return queryset


class UploadImageToGalleryView(CreateView):
    template_name = "gallery/upload_image.html"
    model = Gallery
    form_class = UploadImageForm
    success_url = reverse_lazy("users:options")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()

        return super().form_valid(form)
