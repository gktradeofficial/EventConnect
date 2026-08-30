from django.db import migrations


def create_services(apps, schema_editor):
    Category = apps.get_model("marketplace", "Category")
    Service = apps.get_model("marketplace", "Service")

    data = {
        "Photography": [
            "Wedding Photography",
            "Pre-Wedding Photography",
            "Event Photography",
        ],
        "Videography": [
            "Wedding Videography",
            "Cinematic Videography",
            "Event Videography",
        ],
        "Video Editing": [
            "Wedding Video Editing",
            "Cinematic Video Editing",
            "Reels Editing",
        ],
    }

    for category_name, services in data.items():

        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={
                "is_active": True,
            },
        )

        for service_name in services:
            Service.objects.get_or_create(
                category=category,
                name=service_name,
                defaults={
                    "is_active": True,
                },
            )


def remove_services(apps, schema_editor):
    Category = apps.get_model("marketplace", "Category")
    Service = apps.get_model("marketplace", "Service")

    service_names = [
        "Wedding Photography",
        "Pre-Wedding Photography",
        "Event Photography",
        "Wedding Videography",
        "Cinematic Videography",
        "Event Videography",
        "Wedding Video Editing",
        "Cinematic Video Editing",
        "Reels Editing",
    ]

    Service.objects.filter(name__in=service_names).delete()

    Category.objects.filter(
        name__in=[
            "Photography",
            "Videography",
            "Video Editing",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0003_providerprofile_profile_image"),
    ]

    operations = [
        migrations.RunPython(
            create_services,
            remove_services,
        ),
    ]