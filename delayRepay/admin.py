from django.contrib import admin
from delayRepay.models import UserData, Journey, Ticket, Delay

class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email",
        "title", "forename", "surname",
        "phoneNum", "address1", "address2",
        "city", "county", "postcode", "photocard_id"
    )

class JourneyAdmin(admin.ModelAdmin):
    list_display = (
        "journeyName", "departingStation", "arrivingStation", "delayRepayUser"
    )

class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_type', 'cost', 'ticket_start_date', 'ticket_expiry_date', 'ticket_photo', 'delayRepayUser'
    )

class DelayAdmin(admin.ModelAdmin):
    list_display = (
        "delay", "delay_reason", "date", "startTime", "endTime", 'delayRepayUser'
    )


admin.site.register(UserData, UserDataAdmin)
admin.site.register(Journey, JourneyAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Delay, DelayAdmin)
