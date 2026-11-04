import os
from pathlib import Path, PurePosixPath

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db.models.fields.files import FileField


class Command(BaseCommand):
    help = (
        "Copy database-referenced local uploads to their configured Cloudinary "
        "storage. Use --execute to perform uploads; local files are never deleted."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--execute",
            action="store_true",
            help="Upload local files and update their database paths.",
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT).resolve()
        entries = self._get_media_entries(media_root)
        missing = [entry for entry in entries if not entry[4].is_file()]

        if not options["execute"]:
            self.stdout.write(
                f"Dry run: {len(entries) - len(missing)} local media file(s) "
                f"ready to upload; {len(missing)} referenced file(s) missing."
            )
            self.stdout.write("Run with --execute to upload. Local files will be kept.")
            if missing:
                self.stderr.write(
                    "Missing local source(s): "
                    + ", ".join(entry[3] for entry in missing)
                )
            return

        already_remote = set()
        missing_sources = set()
        remote_status = {}
        for model, instance, field, old_name, source_path in missing:
            cache_key = (field.storage.__class__, old_name)
            if cache_key not in remote_status:
                remote_status[cache_key] = field.storage.exists(old_name)
            if remote_status[cache_key]:
                already_remote.add(cache_key)
            else:
                missing_sources.add(f"{model.__name__}.{field.name}: {old_name}")

        if missing_sources:
            raise CommandError(
                "Some local media files are missing. No uploads were started. "
                "Restore these files or confirm they already exist in Cloudinary: "
                + ", ".join(sorted(missing_sources))
            )

        uploaded_names = {}
        uploaded_count = 0
        already_remote_count = 0

        for model, instance, field, old_name, source_path in entries:
            cache_key = (field.storage.__class__, old_name)
            if cache_key in already_remote:
                already_remote_count += 1
                continue

            new_name = uploaded_names.get(cache_key)

            if new_name is None:
                with source_path.open("rb") as source:
                    new_name = field.storage.save(
                        old_name,
                        File(source, name=old_name),
                    )
                uploaded_names[cache_key] = new_name
                uploaded_count += 1

            setattr(instance, field.name, new_name)
            instance.save(update_fields=[field.name])

        self.stdout.write(
            self.style.SUCCESS(
                f"Uploaded {uploaded_count} file(s), found "
                f"{already_remote_count} already in Cloudinary. "
                "Local source files were kept."
            )
        )

    def _get_media_entries(self, media_root):
        entries = []
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if not isinstance(field, FileField) or not field.concrete:
                    continue

                instances = model.objects.exclude(**{field.name: ""})
                if field.null:
                    instances = instances.exclude(
                        **{f"{field.name}__isnull": True}
                    )

                for instance in instances.iterator():
                    old_name = getattr(instance, field.name).name
                    if not old_name or old_name == str(field.default):
                        continue

                    relative_name = PurePosixPath(old_name.replace("\\", "/"))
                    source_path = (media_root / Path(*relative_name.parts)).resolve()
                    if os.path.commonpath((media_root, source_path)) != str(media_root):
                        raise CommandError(
                            f"Media path escapes MEDIA_ROOT: {old_name}"
                        )
                    entries.append(
                        (model, instance, field, old_name, source_path)
                    )
        return entries
