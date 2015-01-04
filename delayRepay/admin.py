from django.contrib import admin
from delayRepay.models import UserData, Journey, Ticket

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

admin.site.register(UserData, UserDataAdmin)
admin.site.register(Journey, JourneyAdmin)
admin.site.register(Ticket, TicketAdmin)
