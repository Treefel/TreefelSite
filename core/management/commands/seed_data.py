from django.core.management.base import BaseCommand
from core.models import BlogCategory, SiteSetting


class Command(BaseCommand):
    help = "Seed initial data for Treefel site"

    def handle(self, *args, **options):
        categories = ["Dev Log", "Personal", "Interesting Finds"]
        for name in categories:
            BlogCategory.objects.get_or_create(name=name)
            self.stdout.write(f"  Category: {name}")

        SiteSetting.objects.get_or_create(
            key="feedback_welcome",
            defaults={"value": "Have something to share? Drop a message below!"},
        )
        self.stdout.write(self.style.SUCCESS("Seed data created."))
