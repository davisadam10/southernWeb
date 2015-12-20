import os
from datetime import datetime, time
import suds
from suds.sax.element import Element

token = os.getenv('NATIONAL_RAIL_TOKEN')
WSDL_URL = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx"
LDB = suds.client.Client(WSDL_URL, soapheaders=Element('AccessToken').insert(Element('TokenValue').setText(token)))

MAX_SERVICES = 15
MAX_RESULTS = 1


def get_service_details(service):
    return LDB.service.GetServiceDetails(service.serviceID)


def is_service_cancelled(service):
    cancelled = False
    details = get_service_details(service)
    try:
        if details.etd == 'Cancelled':
            cancelled = True
    except:
        pass

    return cancelled

def is_service_delayed(service):
    pass


def get_services_from_to(depart_station, arrival_station):
    """

    :param depart_station:
    :type depart_station:
    :param arrival_station:
    :type arrival_station:
    :return:
    :rtype:
    """
    train_services = []
    departure_board = LDB.service.GetDepartureBoard(MAX_SERVICES, depart_station)
    for count, service in enumerate(departure_board.trainServices.service):
        details = LDB.service.GetServiceDetails(service.serviceID)
        for calling_point in details.subsequentCallingPoints.callingPointList[0].callingPoint:
            station = calling_point
            if station.crs == arrival_station:
                train_services.append(service)
                break
    return train_services


def get_services_arriving_from(depart_station, arrival_station):
    """

    :param depart_station: station where the train left
    :type depart_station:
    :param arrival_station: station where train arrives
    :type arrival_station:
    :return:
    :rtype:
    """
    train_services = []
    departure_board = LDB.service.GetArrivalBoard(MAX_SERVICES, arrival_station)
    for count, service in enumerate(departure_board.trainServices.service):
        details = LDB.service.GetServiceDetails(service.serviceID)
        for calling_point in details.previousCallingPoints.callingPointList[0].callingPoint:
            station = calling_point
            if station.crs == depart_station:
                train_services.append(service)
                break
    return train_services

def get_arrival_services(arrival_station):
    return LDB.service.GetArrivalBoard(MAX_SERVICES, arrival_station)


def getCancelledArrivingServices(arrivingStation):
    cancelledServices = []
    departureBoard = LDB.service.GetDepartureBoard(MAX_SERVICES, arrivingStation)
    for service in departureBoard.trainServices.service:
        if service.etd == 'Cancelled':
            cancelledServices.append(service)
    return cancelledServices


def getServiceDepartDetails(serviceID):
    journeyInfo = {}
    details = LDB.service.GetServiceDetails(serviceID)
    journeyInfo['journeyDate'] = datetime.now().date()
    journeyInfo['departingStation'] = details.previousCallingPoints.callingPointList[0].callingPoint[0].crs

    hour, minute = details.previousCallingPoints.callingPointList[0].callingPoint[0].st.split(':')
    journeyInfo['startTime'] = time(int(hour), int(minute))

    if 'at' in details.previousCallingPoints.callingPointList[0].callingPoint[0]:
        if details.previousCallingPoints.callingPointList[0].callingPoint[0].at == "On time":
            journeyInfo['actualStartTime'] = journeyInfo['startTime']
        else:
            hour, minute = details.previousCallingPoints.callingPointList[0].callingPoint[0].at.split(':')
            journeyInfo['actualStartTime'] = journeyInfo['startTime'] = time(int(hour), int(minute))
    else:
        journeyInfo['actualStartTime'] = journeyInfo['startTime']

    return journeyInfo



def getServiceArrivalDetails(serviceID):
    journeyInfo = {}
    details = LDB.service.GetServiceDetails(serviceID)
    journeyInfo['journeyDate'] = datetime.now().date()
    journeyInfo['arrivingStation'] = details.crs
    journeyInfo['endTime'] = details.sta

    if details.eta == "On time":
        journeyInfo['actualEndTime'] = journeyInfo['endTime']
    else:
        journeyInfo['actualEndTime'] = journeyInfo['startTime'] = details.eta

    return journeyInfo


def getDepartingServices(departingStation):
    services = []
    departureBoard = LDB.service.GetDepartureBoard(MAX_SERVICES, departingStation)
    for service in departureBoard.trainServices.service:
        services.append(service)
    return services

#services = getDepartingServices('VIC')
#print getCancelledDepartingServices('VIC')
#details = getServiceArrivalDetails(services[0].serviceID)

#print get_services_from_to('VIC', 'ELD')
#print get_services_from_to('LBG', 'ELD')
#services_from_earls_to_bridge = get_services_from_to('VIC', 'ELD')
#services = get_services_arriving_from('VIC', 'ELD')
#print services
'''
for service in services:
    cancelled = is_service_cancelled(service)
    print cancelled
'''
#for services


def findServiceArrivalTime(station_name, serviceID):
    details = LDB.service.GetServiceDetails(serviceID)
    callingPoint = None
    for calling_point in details.previousCallingPoints.callingPointList[0].callingPoint:
        if calling_point.locationName == station_name:
            callingPoint = calling_point

    if not callingPoint:
        for calling_point in details.subsequentCallingPoints.callingPointList[0].callingPoint:
            if calling_point.locationName == station_name:
                callingPoint = calling_point

    if callingPoint:
        return callingPoint.st



'''
services = get_services_arriving_from(
                        'LBG',
                        'ELD'
                    )

services2 = get_services_from_to(
                        'LBG',
                        'ELD'
                    )
'''

