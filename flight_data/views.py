from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from django.urls import reverse
from . models import Flight
from models import Airmedflights
from django.conf import settings
import csv
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import openpyxl
from tablib import Dataset
from . resource import FlightResource
import psycopg2
import csv
import pandas as pd
from .forms import AirmedflightsForm
from .filters import AirmedflightsFilter
from .filters import AirMedDashboardFilter
from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum


# Create your views here.


def upload_csv(request):
    if request.method == 'POST':
        new_flight_data = request.FILES["excel_file"]
        if not new_flight_data.name.endswith('.xlsx'):
            messages.error(request, "Not Valid File Type")
            return HttpResponseRedirect('flight_data/flight_numbers.html')

        conn = psycopg2.connect(database="airmed_db",
                                host="localhost",
                                user="postgres",
                                password="medic9367",
                                port="5433")

        print("Database Connected....")
        cur = conn.cursor()
        #cur.execute("DROP TABLE AirmedFlights ")
        # cur.execute(
        #     "CREATE TABLE AirmedFlights("
        #     "transport_date DATE, "
        #     "flight_num CHAR(50), "
        #     "base CHAR(100),"
        #     "hour INT,"
        #     "flight_date CHAR(50),"
        #     "flight_month CHAR(100),"
        #     "year CHAR(50),"
        #     "call_sign CHAR(250),"
        #     "vehicle CHAR(250),"
        #     "call_type CHAR(250),"
        #     "initial_priority CHAR(100),"
        #     "outcome CHAR(100),"
        #     "final_disposition CHAR(250),"
        #     "primary_cancel_reason_for_miss CHAR(250),"
        #     "secondary_cancel_reason_for_miss CHAR(250),"
        #     "referrer_name CHAR(350),"
        #     "requesting_agency CHAR(350),"
        #     "pickup_location CHAR(350),"
        #     "pickup_zip INT,"
        #     "pickup_county CHAR(350),"
        #     "pickup_state CHAR(100),"
        #     "pickup_lat NUMERIC,"
        #     "pickup_long NUMERIC,"
        #     "delorme_lat CHAR(100),"
        #     "delorme_long CHAR(100),"
        #     "mappoint_lat CHAR(100),"
        #     "mappoint_long CHAR(100),"
        #     "receiving_agency CHAR(250),"
        #     "dropoff_location CHAR(250),"
        #     "call_start_time CHAR(250),"
        #     "standby_time CHAR(250),"
        #     "end_standby_time CHAR(250),"
        #     "launch_page_time CHAR(250),"
        #     "dispatch_time CHAR(250),"
        #     "flight_accepted_time CHAR(250),"
        #     "depart_base CHAR(250),"
        #     "arrive_pt_location CHAR(250),"
        #     "depart_pt_on_board CHAR(250),"
        #     "at_receiving_facility CHAR(250),"
        #     "depart_receiving_facility CHAR(250),"
        #     "arrive_at_base CHAR(250),"
        #     "cancel_time CHAR(250),"
        #     "pilot CHAR(300),"
        #     "medical_1 CHAR(300),"
        #     "medical_2 CHAR(300),"
        #     "medical_3 CHAR(300),"
        #     "PRIMARY KEY (flight_num));")
        # print("Table Created....")
        # conn.commit()

        # Read the xls file
        df = pd.read_excel(new_flight_data)

        # Change the Column Headings
        df.columns = ["transport_date", "flight_num", "base", "hour", "flight_date", "flight_month", "year", "call_sign", "vehicle",
                      "call_type", "initial_priority", "outcome", "final_disposition", "primary_cancel_reason_for_miss",
                      "secondary_cancel_reason_for_miss", "patient_count", "referrer_name", "requesting_agency",
                      "pickup_location", "pickup_zip", "pickup_county", "pickup_state", "pickup_lat", "pickup_long", "delorme_lat",
                      "delorme_long", "mappoint_lat", "mappoint_long", "referring_doctor", "receiving_agency",
                      "dropoff_location", "receiving_doctor", "call_start_time", "standby_time", "end_standby_time", "launch_page_time",
                      "dispatch_time", "flight_accepted_time", "depart_base", "arrive_pt_location", "depart_pt_on_board", "at_receiving_facility",
                      "depart_receiving_facility", "arrive_at_base", "cancel_time", "pilot", "medical_1", "medical_2",
                      "medical_3", "requestor_unit", "requestor_room", "receiver_unit", "receiver_room", "receiver_caller",
                      "mobile_app_id", "nature_code_name"]

        # Delete columns with data that is not needed
        # del df.columns[]
        df.drop(columns=['patient_count', 'referring_doctor', 'receiving_doctor', "requestor_unit", "requestor_room",
                         "receiver_unit", "receiver_room", "receiver_caller", "mobile_app_id", "nature_code_name"])
        # Remove the last two rows of the spreadsheet to remove totals
        df = df.iloc[:-2]

        # Fill in blanks with NAN
        df[["hour", "year", "pickup_zip", "pickup_lat", "pickup_long"]] = df[[
            "hour", "year", "pickup_zip", "pickup_lat", "pickup_long"]].fillna(value=-1)

        # Cast Year and hour column to int
        df[["hour", "year", "pickup_zip"]] = df[[
            "hour", "year", "pickup_zip"]].astype(int)

        # Change transport_date field to date time
        df["transport_date"] = pd.to_datetime(df["transport_date"]).dt.date
        df["call_start_time"] = df["call_start_time"].dt.strftime(
            "%Y-%d-%m %H:%M:%S")
        df["standby_time"] = df["standby_time"].dt.strftime(
            "%Y-%d-%m %H:%M:%S")
        df["end_standby_time"] = df["end_standby_time"].dt.strftime(
            "%Y-%d-%m %H:%M:%S")
        df["launch_page_time"] = df["launch_page_time"].dt.strftime(
            "%Y-%d-%m %H:%M:%S")
        df["dispatch_time"] = df["dispatch_time"].dt.strftime(
            "%Y-%d-%m %H:%M:%S")

        # Change to CSV File for upload to database.
        df.to_csv("output.csv", index=False)

        with open('output.csv', 'r', encoding='utf-8-sig') as fin:
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = []
            for i in dr:
                if i["transport_date"] == 'tra':
                    pass

                to_db.append((i['transport_date'], i['flight_num'], i['base'], i['hour'], i['flight_date'], i['flight_month'],
                              i['year'], i['call_sign'], i['vehicle'], i["call_type"], i["initial_priority"],
                              i["outcome"], i["final_disposition"], i["primary_cancel_reason_for_miss"],
                              i["secondary_cancel_reason_for_miss"], i["referrer_name"], i["requesting_agency"],
                              i["pickup_location"], i["pickup_zip"], i["pickup_county"], i["pickup_state"],
                              i["pickup_lat"], i["pickup_long"], i["delorme_lat"], i["delorme_long"],
                              i["mappoint_lat"], i["mappoint_long"], i["receiving_agency"],
                              i["dropoff_location"], i["call_start_time"], i["standby_time"],
                              i["end_standby_time"], i["launch_page_time"], i["dispatch_time"], i["flight_accepted_time"],
                              i["depart_base"], i["arrive_pt_location"], i["depart_pt_on_board"], i[
                                  "at_receiving_facility"], i["depart_receiving_facility"],
                              i["arrive_at_base"], i["cancel_time"], i["pilot"], i["medical_1"], i["medical_2"], i["medical_3"]))

            cur.executemany("INSERT INTO AirmedFlights (transport_date, flight_num,base,hour,flight_date,flight_month,year,"
                            "call_sign,vehicle,call_type,initial_priority,outcome,final_disposition,"
                            "primary_cancel_reason_for_miss, secondary_cancel_reason_for_miss, referrer_name,"
                            "requesting_agency, pickup_location,pickup_zip,pickup_county,pickup_state,"
                            "pickup_lat,pickup_long,delorme_lat,delorme_long,mappoint_lat,mappoint_long"
                            ",receiving_agency,dropoff_location,call_start_time,standby_time,end_standby_time,launch_page_time,"
                            "dispatch_time,flight_accepted_time,depart_base,arrive_pt_location,depart_pt_on_board,at_receiving_facility,"
                            "depart_receiving_facility,arrive_at_base,cancel_time,pilot,medical_1,medical_2,medical_3) "
                            "VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                            "%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (flight_num) DO NOTHING;", to_db)

        conn.commit()
        conn.close()
        return render(request, 'flight_data/data_upload_success.html')
    else:
        return render(request, 'flight_data/flight_numbers.html')


def upload_success(request):
    return render(request, 'flight_numbers/data_upload_success.html')


def flight_data(request):
    flights = Airmedflights.objects.all()
    df = pd.DataFrame(list(Airmedflights.objects.all().values()))
    by_date = Airmedflights.objects.filter(transport_date__lte='2021-01-01')

    return render(request, 'flight_data/flight_data.html', {
        "flights": flights,
        "Jan2022": by_date,
    })


def flight_search(request):
    listings = Airmedflights.objects.all()
    listing_filter = AirmedflightsFilter(request.GET, queryset=listings)
    context = {
        'listing_filter': listing_filter
    }
    return render(request, 'flight_data/search_request.html', context)

# flight_search_result helper function


def is_valid_query(param):
    return param != '' and param is not None


# def transport_search(request):
#     listings = Airmedflights.objects.all()
#     listing_filter = AirmedflightsFilter(request.GET, queryset=listings)
#     context = {
#         'listing_filter': listing_filter
#     }

#     return render(request, 'flight_data/transport_search.html', context)


def transport_search(request):

    def get_top_requestor(base):
        return base.values('requesting_agency').annotate(
            call_count=Count('requesting_agency')).order_by('call_count').reverse()

    def get_top_reciever(base):
        return base.values('dropoff_location').annotate(
            call_count=Count('dropoff_location')).order_by('call_count').reverse()

    def get_missed_reason(base):
        return base.values('primary_cancel_reason_for_miss').annotate(
            call_count=Count('primary_cancel_reason_for_miss')).order_by('call_count').reverse()

    def get_day_of_week(base):
        return base.values('flight_date').annotate(
            call_count=Count('flight_date')).order_by('call_count').reverse()

    def get_time_of_day(base):

        return base.values('hour').annotate(
            call_count=Count('hour')).order_by('hour')

    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    date_seperated = Airmedflights.objects.filter(
        transport_date__range=[start_date, end_date]).filter(outcome="Complete")

    interfacility = date_seperated.filter(
        Q(call_type="Revenue - Interhospital") | Q(call_type="Revenue - Team - NICU"))

    scene = date_seperated.filter(call_type="Revenue - Scene")

    # DSM Flight Totals
    dsm_all_flights = Airmedflights.objects.filter(
        transport_date__range=[start_date, end_date]).filter(base="IA Air Med 01 Des Moines")
    dsm_all_transported = date_seperated.filter(base="IA Air Med 01 Des Moines").filter(
        Q(call_type="Revenue - Interhospital") | Q(call_type="Revenue - Team - NICU") | Q(call_type="Revenue - Scene"))
    dsm_interfacility = interfacility.filter(base="IA Air Med 01 Des Moines")
    dsm_scene = scene.filter(base="IA Air Med 01 Des Moines")
    dsm_total_flights = dsm_interfacility.count() + dsm_scene.count()
    dsm_interfacility_requestor = get_top_requestor(dsm_interfacility)
    dsm_scene_requestor = get_top_requestor(dsm_scene)
    dsm_reciever = get_top_reciever(dsm_all_transported)
    dsm_missed = dsm_all_flights.filter(
        Q(outcome="Decline/Miss") | Q(outcome="Abort") | Q(outcome="Cancel"))
    dsm_missed_by_count = get_missed_reason(dsm_missed)
    dsm_day_of_week = get_day_of_week(dsm_all_transported)
    dsm_time_of_day = get_time_of_day(dsm_all_transported)

    # Knoxville Flight Numbers
    kx_all_flights = Airmedflights.objects.filter(
        transport_date__range=[start_date, end_date]).filter(base="IA Air Med 02 Knoxville")
    kx_all_transported = date_seperated.filter(base="IA Air Med 02 Knoxville").filter(
        Q(call_type="Revenue - Interhospital") | Q(call_type="Revenue - Team - NICU") | Q(call_type="Revenue - Scene"))
    kx_interfacility = interfacility.filter(base="IA Air Med 02 Knoxville")
    kx_scene = scene.filter(base="IA Air Med 02 Knoxville")
    kx_total_flights = kx_interfacility.count() + kx_scene.count()
    kx_interfacility_requestor = get_top_requestor(kx_interfacility)
    kx_scene_requestor = get_top_requestor(kx_scene)
    kx_missed = kx_all_flights.filter(
        Q(outcome="Decline/Miss") | Q(outcome="Abort") | Q(outcome="Cancel"))
    kx_missed_by_count = get_missed_reason(kx_missed)
    kx_day_of_week = get_day_of_week(kx_all_transported)
    kx_time_of_day = get_time_of_day(kx_all_transported)

    # Mason City Flight Numbers
    mc_all_flights = Airmedflights.objects.filter(
        transport_date__range=[start_date, end_date]).filter(base="IA Air Med 03 Mason City")
    mc_all_transported = date_seperated.filter(base="IA Air Med 03 Mason City").filter(
        Q(call_type="Revenue - Interhospital") | Q(call_type="Revenue - Team - NICU") | Q(call_type="Revenue - Scene"))
    mc_interfacility = interfacility.filter(base="IA Air Med 03 Mason City")
    mc_scene = scene.filter(base="IA Air Med 03 Mason City")
    mc_total_flights = mc_interfacility.count() + mc_scene.count()
    mc_interfacility_requestor = get_top_requestor(mc_interfacility)
    mc_scene_requestor = get_top_requestor(mc_scene)
    mc_missed = mc_all_flights.filter(
        Q(outcome="Decline/Miss") | Q(outcome="Abort") | Q(outcome="Cancel"))
    mc_missed_by_count = get_missed_reason(mc_missed)
    mc_day_of_week = get_day_of_week(mc_all_transported)
    mc_time_of_day = get_time_of_day(mc_all_transported)

    # Sioux City Flight Numbers
    sc_all_flights = Airmedflights.objects.filter(
        transport_date__range=[start_date, end_date]).filter(base="IA Air Med 04 Sioux City")
    sc_all_transported = date_seperated.filter(base="IA Air Med 04 Sioux City").filter(
        Q(call_type="Revenue - Interhospital") | Q(call_type="Revenue - Team - NICU") | Q(call_type="Revenue - Scene"))
    sc_scene = scene.filter(base="IA Air Med 04 Sioux City")
    sc_interfacility = interfacility.filter(base="IA Air Med 04 Sioux City")
    sc_total_flights = sc_interfacility.count() + sc_scene.count()
    sc_interfacility_requestor = get_top_requestor(sc_interfacility)
    sc_scene_requestor = get_top_requestor(sc_scene)
    sc_missed = sc_all_flights.filter(
        Q(outcome="Decline/Miss") | Q(outcome="Abort") | Q(outcome="Cancel"))
    sc_missed_by_count = get_missed_reason(sc_missed)
    sc_day_of_week = get_day_of_week(sc_all_transported)
    sc_time_of_day = get_time_of_day(sc_all_transported)

    # listing_filter = AirMedDashboardFilter(request.GET, queryset=listings)
    # print(listing_filter.qs.)
    # count = listing_filter.qs.count()
    # print("COUNT" + str(count))
    context = {
        'listing_filter': date_seperated,
        'interfacility': interfacility,
        'scene': scene,

        'dsm_all_flights': dsm_all_flights,
        'dsm_interfacility': dsm_interfacility,
        'dsm_scene': dsm_scene,
        'dsm_total_flights': dsm_total_flights,
        'dsm_missed': dsm_missed,
        'dsm_missed_by_count': dsm_missed_by_count,
        'dsm_all_transported': dsm_all_transported,
        'dsm_reciever': dsm_reciever,
        'dsm_day_of_week': dsm_day_of_week,
        'dsm_time_of_day': dsm_time_of_day,


        'kx_interfacility': kx_interfacility,
        'kx_scene': kx_scene,
        'kx_total_flights': kx_total_flights,
        'kx_interfacility_requestor': kx_interfacility_requestor,
        'kx_scene_requestor': kx_scene_requestor,
        'kx_missed': kx_missed,
        'kx_missed_by_count': kx_missed_by_count,
        'kx_all_transported': kx_all_transported,
        'kx_day_of_week': kx_day_of_week,
        'kx_time_of_day': kx_time_of_day,


        'mc_interfacility': mc_interfacility,
        'mc_scene': mc_scene,
        'mc_total_flights': mc_total_flights,
        'mc_interfacility': mc_interfacility,
        'mc_interfacility_requestor': mc_interfacility_requestor,
        'mc_scene_requestor': mc_scene_requestor,
        'mc_missed': mc_missed,
        'mc_missed_by_count': mc_missed_by_count,
        'mc_all_transported': mc_all_transported,
        'mc_day_of_week': mc_day_of_week,
        'mc_time_of_day': mc_time_of_day,



        'sc_interfacility': sc_interfacility,
        'sc_scene': sc_scene,
        'sc_total_flights': sc_total_flights,
        'start_date': start_date,
        'sc_interfacility_requestor': sc_interfacility_requestor,
        'sc_scene_requestor': sc_scene_requestor,
        'sc_missed': sc_missed,
        'sc_missed_by_count': sc_missed_by_count,
        'sc_all_transported': sc_all_transported,
        'sc_day_of_week': sc_day_of_week,
        'sc_time_of_day': sc_time_of_day,


        'end_date': end_date,
        'dsm_interfacility_requestor': dsm_interfacility_requestor,
        'dsm_scene_requestor': dsm_scene_requestor



    }

    return render(request, 'flight_data/transport_search.html', context)
