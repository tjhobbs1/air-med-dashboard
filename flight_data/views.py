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
        #     "pickup_state CHAR(10),"
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

        # Fill in blanks with NAN
        df[["hour", "year", "pickup_zip", "pickup_lat", "pickup_long"]] = df[[
            "hour", "year", "pickup_zip", "pickup_lat", "pickup_long"]].fillna(value=-1)

        # Cast Year and hour column to int
        df[["hour", "year", "pickup_zip"]] = df[[
            "hour", "year", "pickup_zip"]].astype(int)

        # Remove the last two rows of the spreadsheet to remove totals
        df = df.iloc[:-2]

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

        print(df['call_start_time'])

        with open('output.csv', 'r', encoding='utf-8-sig') as fin:
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            for line in dr:
                if line["transport_date"] == 'tra':
                    pass
                else:
                    #x = line["transport_date"]
                    #new_date = datetime.datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")
                    #line["transport_date"] = new_date
                    pass
                to_db = [(i['transport_date'], i['flight_num'], i['base'], i['hour'], i['flight_date'], i['flight_month'],
                          i['year'], i['call_sign'], i['vehicle'], i["call_type"], i["initial_priority"],
                          i["outcome"], i["final_disposition"], i["primary_cancel_reason_for_miss"],
                          i["secondary_cancel_reason_for_miss"], i["referrer_name"], i["requesting_agency"],
                          i["pickup_location"], i["pickup_zip"], i["pickup_county"], i["pickup_state"],
                          i["pickup_lat"], i["pickup_long"], i["delorme_lat"], i["delorme_long"],
                          i["mappoint_lat"], i["mappoint_long"], i["receiving_agency"],
                          i["dropoff_location"], i["call_start_time"], i["standby_time"],
                          i["end_standby_time"], i["launch_page_time"], i["dispatch_time"], i["flight_accepted_time"],
                          i["depart_base"], i["arrive_pt_location"], i["depart_pt_on_board"], i["at_receiving_facility"], i["depart_receiving_facility"],
                          i["arrive_at_base"], i["cancel_time"], i["pilot"], i["medical_1"], i["medical_2"], i["medical_3"]) for i in dr]

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
    print(df['depart_base'].dtype)
    by_date = Airmedflights.objects.filter(transport_date__lte='2021-01-01')

    return render(request, 'flight_data/flight_data.html', {
        "flights": flights,
        "Jan2022": by_date,
    })


def flight_search(request):
    qs = Airmedflights.objects.all()
    call_sign = request.GET.get('call_sign')
    trip_start = request.GET.get('trip_start')
    trip_end = request.GET.get('trip_end')

    if call_sign != '' and call_sign is not None:
        qs = qs.filter(vehicle__exact=call_sign,
                       transport_date__gte=trip_start, transport_date__lte=trip_end)
    else:
        qs = qs.filter(
            transport_date__gte=trip_start, transport_date__lte=trip_end)
    context = {
        'queryset': qs
    }
    return render(request, 'flight_data/search.html', context)
