# Pet Hotel

Django-based backend for managing pet hotels and embassy citizen records, with a group-scoped Django Admin.

---

## Group-based permissions

All non-superuser access in Django Admin is gated by the user's group membership. **Group names are not arbitrary** — they are hardcoded keys in two mapping constants that drive the entire permission system.

### Reserved group names

| Group name | Scope |
|---|---|
| `pet_hotel_group` | Pet hotel staff — access to hotel-related data and `auth.User` mail templates |
| `embassy_group` | Embassy staff — access to citizen/university data and both `auth.User` + `Citizen` mail templates |

A user can belong to both groups simultaneously and will receive the union of both scopes.

---

## How it works

### 1. Mail templates (`apps/mail`)

`GROUP_CONTENT_TYPE_MODELS` in `apps/mail/forms/send_email_form.py` maps each group to the recipient models its members can target:

```python
GROUP_CONTENT_TYPE_MODELS = {
    "pet_hotel_group": [User],
    "embassy_group":   [User, Citizen],
}
```

When a non-superuser opens *Mail Template → Add*, the `content_type` dropdown only shows the models allowed for their group(s). A user in neither group sees an empty dropdown.

### 2. Auth groups (`apps/auth/admin/group.py`)

`GROUP_PREFIX_MAP` in `apps/auth/admin/constants.py` maps each group to a name prefix:

```python
GROUP_PREFIX_MAP = {
    "pet_hotel_group": "pet_hotel",
    "embassy_group":   "embassy",
}
```

- **List view** — non-superusers see only `auth.Group` records whose name starts with their allowed prefix(es).
- **Create/edit** — a validator rejects any group name that does not start with an allowed prefix.

This means all groups belonging to the hotel domain must be named `pet_hotel_*`, and all embassy groups must be named `embassy_*`.

### 3. Users (`apps/auth/admin/user.py`)

Non-superusers see only `auth.User` records that belong to at least one of their own allowed groups (`pet_hotel_group` or `embassy_group`). A user in both groups sees the union.

---

## Adding a new scope

1. Create the Django group in the database with the correct prefix (e.g. `new_scope_group`).
2. Add an entry to `GROUP_PREFIX_MAP` in `apps/auth/admin/constants.py`.
3. Add an entry to `GROUP_CONTENT_TYPE_MODELS` in `apps/mail/forms/send_email_form.py`.
4. Assign users to the new group via the superuser admin.

No other code changes are needed.
