import traceback
from datetime import date, datetime

import openpyxl
from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from apps.embassy.forms.citizen_upload_form import CitizenUploadForm
from apps.embassy.models import Citizen, CitizenUniversity
from apps.embassy.models.citizen_upload_log import CitizenUploadLog

CITIZEN_UPLOAD_FIELDS = [
    "id_number",
    "first_name",
    "second_name",
    "first_surname",
    "second_surname",
    "birthdate",
    "main_email",
    "secondary_email",
    "phone_exterior",
    "phone_home_country",
]
_UPDATE_FIELDS = [f for f in CITIZEN_UPLOAD_FIELDS if f != "main_email"]
_BATCH_SIZE = 500


@admin.action(description=_("Restore selected citizens"))
def restore_citizens(modeladmin, request, queryset):
    ids_to_restore = list(queryset.values_list("id", flat=True))
    count = len(ids_to_restore)
    if count > 0:
        with transaction.atomic():
            citizen_to_restore = Citizen.objects.filter(id__in=ids_to_restore)
            updated = citizen_to_restore.update(is_deleted=False)
            CitizenUniversity.objects.filter(citizen_id__in=ids_to_restore, is_deleted=True).update(is_deleted=False)
            modeladmin.message_user(request, _("%d citizens restored successfully.") % updated, messages.SUCCESS)
    else:
        modeladmin.message_user(request, _("No citizens selected for restore."), messages.WARNING)


@admin.action(description=_("Permanently delete selected citizens"))
def hard_delete_citizens(modeladmin, request, queryset):
    ids_to_delete = list(queryset.values_list("id", flat=True))
    count = len(ids_to_delete)
    if count > 0:
        with transaction.atomic():
            Citizen.hard_delete_bulk(ids=ids_to_delete)
            university_relations_to_delete = CitizenUniversity.objects.filter(
                citizen_id__in=ids_to_delete
            ).values_list("id", flat=True)
            CitizenUniversity.hard_delete_bulk(ids=university_relations_to_delete)
        modeladmin.message_user(request, _("%d citizens permanently deleted.") % count, messages.SUCCESS)
    else:
        modeladmin.message_user(request, _("No citizens selected for deletion."), messages.WARNING)


class CitizenUniversityInline(admin.TabularInline):
    model = CitizenUniversity
    extra = 1
    fields = ["university", "enrollment_date", "graduation_date", "stop_date", "is_active"]
    autocomplete_fields = ["university"]


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "id_number", "first_name", "first_surname", "main_email", "age", "is_deleted"]
    list_filter = ["birthdate", "is_deleted"]
    search_fields = ["first_name", "second_name", "first_surname", "second_surname", "main_email"]
    fieldsets = (
        (
            _("Personal Information"),
            {"fields": ("id_number", "first_name", "second_name", "first_surname", "second_surname", "birthdate")},
        ),
        (_("Contact Information"), {"fields": ("main_email", "secondary_email")}),
        (_("Phone Numbers"), {"fields": ("phone_exterior", "phone_home_country")}),
        (_("Status"), {"fields": ("is_deleted",)}),
    )
    inlines = [CitizenUniversityInline]
    actions = [restore_citizens, hard_delete_citizens]

    def get_queryset(self, request):
        return super().get_queryset(request)

    def get_list_display(self, request):
        return self.list_display

    def delete_model(self, request, obj):
        with transaction.atomic():
            obj.soft_delete()
            university_relations_to_delete = CitizenUniversity.objects.filter(citizen_id=obj.pk).values_list(
                "id", flat=True
            )
            CitizenUniversity.soft_delete_bulk(ids=university_relations_to_delete)
        self.message_user(request, _("%s was deleted successfully (soft delete).") % obj.full_name, messages.SUCCESS)

    def delete_queryset(self, request, queryset):
        with transaction.atomic():
            ids_to_delete = list(queryset.values_list("id", flat=True))
            Citizen.soft_delete_bulk(ids=ids_to_delete)
            university_relations_to_delete = CitizenUniversity.objects.filter(
                citizen_id__in=ids_to_delete
            ).values_list("id", flat=True)
            CitizenUniversity.soft_delete_bulk(ids=university_relations_to_delete)
        self.message_user(
            request, _("%d citizens were deleted successfully (soft delete).") % len(ids_to_delete), messages.SUCCESS
        )

    def get_urls(self):
        return [
            path(
                "upload/",
                self.admin_site.admin_view(self.upload_view),
                name="embassy_citizen_upload",
            ),
        ] + super().get_urls()

    def upload_view(self, request):
        if request.method == "POST":
            form = CitizenUploadForm(request.POST, request.FILES)
            if form.is_valid():
                results = self._process_excel_upload(form.cleaned_data["file"])
                CitizenUploadLog.objects.create(log=results)

                created = sum(1 for r in results if r["status"] == "created")
                updated = sum(1 for r in results if r["status"] == "updated")
                errors = sum(1 for r in results if r["status"] == "error")

                if created or updated:
                    self.message_user(
                        request,
                        _("Upload complete: %(c)d created, %(u)d updated, %(e)d errors.")
                        % {"c": created, "u": updated, "e": errors},
                        messages.SUCCESS if not errors else messages.WARNING,
                    )
                else:
                    self.message_user(
                        request,
                        _("Upload finished with %(e)d errors and no successful rows.") % {"e": errors},
                        messages.ERROR,
                    )
                return redirect(reverse("admin:embassy_citizen_changelist"))
        else:
            form = CitizenUploadForm()

        context = {
            **self.admin_site.each_context(request),
            "title": _("Upload Citizens"),
            "form": form,
            "opts": self.model._meta,
            "media": self.media + form.media,
            "expected_columns": CITIZEN_UPLOAD_FIELDS,
        }
        return render(request, "admin/embassy/citizen/upload.html", context)

    def _process_excel_upload(self, excel_file):
        results = []

        try:
            wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(values_only=True))
        except Exception:
            return [{"row": 0, "status": "error", "message": traceback.format_exc()}]

        if not rows:
            return []

        headers = [str(h).strip() if h is not None else "" for h in rows[0]]

        rows_to_process = []

        for row_idx, row in enumerate(rows[1:], start=2):
            try:
                row_data = {}
                for i, value in enumerate(row):
                    if i < len(headers) and headers[i] in CITIZEN_UPLOAD_FIELDS:
                        row_data[headers[i]] = value

                main_email = row_data.get("main_email")
                if not main_email or str(main_email).strip() == "":
                    results.append({"row": row_idx, "status": "error", "message": "no main_email"})
                    continue

                main_email = str(main_email).strip()
                row_data["main_email"] = main_email

                cleaned = {}
                for field, value in row_data.items():
                    if value is None:
                        continue
                    if field == "birthdate":
                        if isinstance(value, datetime):
                            cleaned[field] = value.date().isoformat()
                        elif isinstance(value, date):
                            cleaned[field] = value.isoformat()
                        else:
                            v = str(value).strip()
                            cleaned[field] = v if v else None
                    else:
                        v = str(value).strip()
                        cleaned[field] = v if v else None

                rows_to_process.append((row_idx, main_email, cleaned))

            except Exception:
                results.append({"row": row_idx, "status": "error", "message": traceback.format_exc()})

        if not rows_to_process:
            return results

        emails = [r[1] for r in rows_to_process]
        existing_citizens = {c.main_email: c for c in Citizen.objects.filter(main_email__in=emails)}

        to_create = []
        to_update = []
        row_meta = {}

        for row_idx, main_email, data in rows_to_process:
            if main_email in existing_citizens:
                citizen = existing_citizens[main_email]
                for field, value in data.items():
                    if field != "main_email":
                        setattr(citizen, field, value)
                to_update.append(citizen)
                row_meta[main_email] = (row_idx, "updated")
            else:
                citizen = Citizen(**data)
                to_create.append(citizen)
                row_meta[main_email] = (row_idx, "created")

        for i in range(0, len(to_create), _BATCH_SIZE):
            batch = to_create[i : i + _BATCH_SIZE]
            try:
                with transaction.atomic():
                    Citizen.objects.bulk_create(batch)
                for c in batch:
                    row_idx, status = row_meta[c.main_email]
                    results.append({"row": row_idx, "status": status, "email": c.main_email})
            except Exception:
                for c in batch:
                    try:
                        with transaction.atomic():
                            c.save()
                        row_idx, status = row_meta[c.main_email]
                        results.append({"row": row_idx, "status": "created", "email": c.main_email})
                    except Exception:
                        row_idx, _ = row_meta[c.main_email]
                        results.append(
                            {
                                "row": row_idx,
                                "status": "error",
                                "email": c.main_email,
                                "message": traceback.format_exc(),
                            }
                        )

        for i in range(0, len(to_update), _BATCH_SIZE):
            batch = to_update[i : i + _BATCH_SIZE]
            try:
                with transaction.atomic():
                    Citizen.objects.bulk_update(batch, _UPDATE_FIELDS)
                for c in batch:
                    row_idx, status = row_meta[c.main_email]
                    results.append({"row": row_idx, "status": status, "email": c.main_email})
            except Exception:
                for c in batch:
                    try:
                        with transaction.atomic():
                            c.save()
                        row_idx, status = row_meta[c.main_email]
                        results.append({"row": row_idx, "status": "updated", "email": c.main_email})
                    except Exception:
                        row_idx, _ = row_meta[c.main_email]
                        results.append(
                            {
                                "row": row_idx,
                                "status": "error",
                                "email": c.main_email,
                                "message": traceback.format_exc(),
                            }
                        )

        results.sort(key=lambda x: x["row"])
        return results
