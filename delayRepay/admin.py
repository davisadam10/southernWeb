from django.contrib import admin
from delayRepay.models import UserData

class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email",
        "title", "forename", "surname",
        "phoneNum", "address1", "address2",
        "city", "county", "postcode", "photocard_id"
    )

admin.site.register(UserData, UserDataAdmin)
