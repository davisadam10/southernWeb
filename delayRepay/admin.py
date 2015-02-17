from django.contrib import admin
import delayRepay.models as models


class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email",
        "title", "forename", "surname",
        "phoneNum", "address1", "address2",
        "city", "county", "postcode", "photocard_id"
    )


class JourneyAdmin(admin.ModelAdmin):
    list_display = (
        "journeyName", "departingStation", "arrivingStation", "delayRepayUser", 'id'
    )


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_type', 'cost', 'ticket_start_date', 'ticket_expiry_date', 'ticket_photo', 'delayRepayUser'
    )


class DelayAdmin(admin.ModelAdmin):
    list_display = (
        "delay", "delay_reason", "date", "startTime", "endTime", 'delayRepayUser', 'claimed', 'expired', 'journey'
    )


class StationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'short_name'
    )

admin.site.register(models.UserData, UserDataAdmin)
admin.site.register(models.Journey, JourneyAdmin)
admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.Delay, DelayAdmin)
admin.site.register(models.Station, StationAdmin)
