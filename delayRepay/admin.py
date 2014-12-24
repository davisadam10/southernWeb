from django.contrib import admin
from delayRepay.models import UserData, Journey

class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email",
        "title", "forename", "surname",
        "phoneNum", "address1", "address2",
        "city", "county", "postcode", "photocard_id"
    )

class JourneyAdmin(admin.ModelAdmin):
    list_display = (
        "journeyName", "departingStation", "arrivingStation",
        "date", "startTime",
        "endTime", "delayRepayUser"
    )

admin.site.register(UserData, UserDataAdmin)
admin.site.register(Journey, JourneyAdmin)
