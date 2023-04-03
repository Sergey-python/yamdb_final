from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Category, Genre, Title, Comment, Review


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
            "slug",
        )


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]


class CommentResource(resources.ModelResource):
    review_id = Field(attribute="review_id", column_name="review_id")
    csv_pub_date = Field(attribute="pub_date", column_name="pub_date")

    class Meta:
        model = Comment
        fields = (
            "id",
            "review_id",
            "text",
            "author",
            "csv_pub_date",
        )


class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]


class ReviewResource(resources.ModelResource):
    title_id = Field(attribute="title_id", column_name="title_id")
    text = Field(attribute="text", column_name="text")
    author = Field(attribute="author", column_name="author")
    score = Field(attribute="score", column_name="score")
    csv_pub_date = Field(attribute="pub_date", column_name="pub_date")

    class Meta:
        model = Title
        fields = (
            "id",
            "title_id",
            "text",
            "author",
            "score",
            "csv_pub_date",
        )


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
