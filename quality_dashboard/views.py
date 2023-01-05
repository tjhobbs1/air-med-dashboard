from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from models import AdultQuality
import psycopg2
import csv
import pandas as pd
from django.db.models import Avg, Count, Min, Sum

# Create your views here.


def quality_dashboard(request):
    quality = AdultQuality.objects.filter(
        mission_date__range=['2022-08-01', '2022-09-30'])

    def get_stat(numerator, denominator):
        """
        This method takes in a numerator and denomitor to get the percentage for the given QI indicator
        RETURNS: Percentage 
        """
        try:
            return round((numerator.count()/denominator.count()) * 100, 2)
        except ZeroDivisionError:
            return "NA"

    def get_airway_type(base_airway_type):
        """
        This method breaks down the airway by types.  
        RETURNS: Dictonary of airway types. 
        """
        airway_type = {
            "ET Tube": 0,
            "Supraglottic Airway": 0,
            "Cricothyrotomy": 0,
            "Tracheostomy": 0
        }
        for i in base_airway_type:
            if i['whatadvancedairwaydevicewasinplace'].strip() == "trachealTube":
                airway_type["ET Tube"] = i['total_count']
            elif i['whatadvancedairwaydevicewasinplace'].strip() == "supraglotticAirway":
                airway_type["Supraglottic Airway"] = i['total_count']
            elif i['whatadvancedairwaydevicewasinplace'].strip() == "cricothyrotomy":
                airway_type["Cricothyrotomy"] = i['total_count']
            else:
                i['whatadvancedairwaydevicewasinplace'].strip() == "tracheostomy"
                airway_type["Tracheostomy"] = i['total_count']

        return airway_type

    # Bases
    des_moines = quality.filter(base="airMed1")
    knoxville = quality.filter(base="airMed2")
    mason_city = quality.filter(base="airMed3")
    sioux_city = quality.filter(base="airMed4")

    # Get transports
    des_moines_transport = des_moines.filter(
        wasthisanopatienttransport='no')
    knoxville_transport = knoxville.filter(
        wasthisanopatienttransport='no')
    mason_city_transport = mason_city.filter(
        wasthisanopatienttransport='no')
    sioux_city_transport = sioux_city.filter(
        wasthisanopatienttransport='no')

    # Get no transports
    des_moines_no_transport = des_moines.filter(
        wasthisanopatienttransport='yes')
    knoxville_no_transport = knoxville.filter(
        wasthisanopatienttransport='yes')
    mason_city_no_transport = mason_city.filter(
        wasthisanopatienttransport='yes')
    sioux_city_no_transport = sioux_city.filter(
        wasthisanopatienttransport='yes')

    # Get number of scenes
    des_moines_scenes = des_moines.filter(
        mission_type_id="911 Response (Scene)")
    knoxville_scenes = knoxville.filter(
        mission_type_id="911 Response (Scene)")
    mason_city_scenes = mason_city.filter(
        mission_type_id="911 Response (Scene)")
    sioux_city_scenes = sioux_city.filter(
        mission_type_id="911 Response (Scene)")

    # Get number of IFT
    des_moines_ift = des_moines.filter(
        mission_type_id="Interfacility Transport")
    knoxville_ift = knoxville.filter(
        mission_type_id="Interfacility Transport")
    mason_city_ift = mason_city.filter(
        mission_type_id="Interfacility Transport")
    sioux_city_ift = sioux_city.filter(
        mission_type_id="Interfacility Transport")

    # Advanced Airway
    des_moines_advanced_airway_in = des_moines.filter(
        wasthepatienttransportedwithanadvancedairwayinplace="yes").filter(wastheadvancedairwayachronictracheostomytubeandthepatientdidnot="no")
    knoxville_advanced_airway_in = knoxville.filter(
        wasthepatienttransportedwithanadvancedairwayinplace="yes").filter(wastheadvancedairwayachronictracheostomytubeandthepatientdidnot="no")
    mason_city_advanced_airway_in = mason_city.filter(
        wasthepatienttransportedwithanadvancedairwayinplace="yes").filter(wastheadvancedairwayachronictracheostomytubeandthepatientdidnot="no")
    sioux_city_advanced_airway_in = sioux_city.filter(
        wasthepatienttransportedwithanadvancedairwayinplace="yes").filter(wastheadvancedairwayachronictracheostomytubeandthepatientdidnot="no")

    # Advanced Airway By Type
    des_moines_adv_airway_type = des_moines_advanced_airway_in.values('whatadvancedairwaydevicewasinplace').annotate(
        total_count=Count('whatadvancedairwaydevicewasinplace')).order_by('total_count')
    knoxville_adv_airway_type = knoxville_advanced_airway_in.values('whatadvancedairwaydevicewasinplace').annotate(
        total_count=Count('whatadvancedairwaydevicewasinplace')).order_by('total_count')
    mason_city_adv_airway_type = mason_city_advanced_airway_in.values('whatadvancedairwaydevicewasinplace').annotate(
        total_count=Count('whatadvancedairwaydevicewasinplace')).order_by('total_count')
    sioux_city_adv_airway_type = sioux_city_advanced_airway_in.values('whatadvancedairwaydevicewasinplace').annotate(
        total_count=Count('whatadvancedairwaydevicewasinplace')).order_by('total_count')

    des_moines_airway_type = get_airway_type(des_moines_adv_airway_type)
    knoxville_airway_type = get_airway_type(knoxville_adv_airway_type)
    mason_city_airway_type = get_airway_type(mason_city_adv_airway_type)
    sioux_city_airway_type = get_airway_type(sioux_city_adv_airway_type)

    # Advanced Airway Placed by Flight Crew
    des_moines_adv_airway_by_flight_crew = des_moines_advanced_airway_in.filter(
        wastheadvancedairwayplacedbythetransportteam="yes")
    knoxville_adv_airway_by_flight_crew = knoxville_advanced_airway_in.filter(
        wastheadvancedairwayplacedbythetransportteam="yes")
    mason_city_adv_airway_by_flight_crew = mason_city_advanced_airway_in.filter(
        wastheadvancedairwayplacedbythetransportteam="yes")
    sioux_city_adv_airway_by_flight_crew = sioux_city_advanced_airway_in.filter(
        wastheadvancedairwayplacedbythetransportteam="yes")

    # RSI Utlized

    des_moines_rsi_utlized = des_moines_adv_airway_by_flight_crew.filter(
        wasrsiutilizedtosecuretheairway="yes")
    knoxville_rsi_utlized = knoxville_adv_airway_by_flight_crew.filter(
        wasrsiutilizedtosecuretheairway="yes")
    mason_city_rsi_utlized = mason_city_adv_airway_by_flight_crew.filter(
        wasrsiutilizedtosecuretheairway="yes")
    sioux_city_rsi_utlized = sioux_city_adv_airway_by_flight_crew.filter(
        wasrsiutilizedtosecuretheairway="yes")

    # Intubations Done it Transport Vehicle
    des_moines_intbation_in_vehicle = des_moines_adv_airway_by_flight_crew.filter(
        wastheintubationdoneintransportvehicle="yes")
    knoxville_intbation_in_vehicle = knoxville_adv_airway_by_flight_crew.filter(
        wastheintubationdoneintransportvehicle="yes")
    mason_city_intbation_in_vehicle = mason_city_adv_airway_by_flight_crew.filter(
        wastheintubationdoneintransportvehicle="yes")
    sioux_city_intbation_in_vehicle = sioux_city_adv_airway_by_flight_crew.filter(
        wastheintubationdoneintransportvehicle="yes")

    # Intubation Successful on 1st Attempt
    des_moines_intubation_on_first_attempt = des_moines_adv_airway_by_flight_crew.filter(
        wastheintubationsuccessfulonthefirstattempt="yes")

    des_moines_intubation_on_first_attempt_percent = get_stat(
        des_moines_intubation_on_first_attempt, des_moines_adv_airway_by_flight_crew)

   # ETCO2 Usage
    des_moines_etco2 = des_moines_advanced_airway_in.filter(
        wastheredocumentationofatleast2formsofconfirmationoftheadvanced='yes')
    knoxville_etco2 = knoxville_advanced_airway_in.filter(
        wastheredocumentationofatleast2formsofconfirmationoftheadvanced='yes')
    mason_city_etco2 = mason_city_advanced_airway_in.filter(
        wastheredocumentationofatleast2formsofconfirmationoftheadvanced='yes')
    sioux_city_etco2 = sioux_city_advanced_airway_in.filter(
        wastheredocumentationofatleast2formsofconfirmationoftheadvanced='yes')

    des_moines_etco2_percent = get_stat(
        des_moines_etco2, des_moines_advanced_airway_in)
    knoxville_etco2_percent = get_stat(
        knoxville_etco2, knoxville_advanced_airway_in)
    mason_city_etco2_percent = get_stat(
        mason_city_etco2, mason_city_advanced_airway_in)
    sioux_city_etco2_percent = get_stat(
        sioux_city_etco2, sioux_city_advanced_airway_in)

    # Invasive Ventilation
    des_moines_invasive_vent = des_moines_advanced_airway_in.filter(
        wasinvasiveventilationusedonthepatientwithanadvancedairway='yes')

    des_moines_invasive_vent_percent = get_stat(
        des_moines_invasive_vent, des_moines_advanced_airway_in)

    # Patient Temp Documented

    des_moines_temp_documented = des_moines_transport.filter(
        wasapttempdocumented='yes')
    knoxville_temp_documented = knoxville_transport.filter(
        wasapttempdocumented='yes')
    mason_city_temp_documented = mason_city_transport.filter(
        wasapttempdocumented='yes')
    sioux_city_temp_documented = sioux_city_transport.filter(
        wasapttempdocumented='yes')

    des_moines_temp_percent = get_stat(
        des_moines_temp_documented, des_moines_transport)
    knoxville_temp_percent = get_stat(
        knoxville_temp_documented, knoxville_transport)
    mason_city_temp_percent = get_stat(
        mason_city_temp_documented, mason_city_transport)
    sioux_city_temp_percent = get_stat(
        sioux_city_temp_documented, sioux_city_transport)

    # RSI Utilized

    context = {
        'quality': quality,

        # Patient Transports
        'des_moines_transport': des_moines_transport,
        'knoxville_transport': knoxville_transport,
        'mason_city_transport': mason_city_transport,
        'sioux_city_transport': sioux_city_transport,
        # No Patient Transport
        'des_moines_no_transport': des_moines_no_transport,
        'knoxville_no_transport': knoxville_no_transport,
        'mason_city_no_transport': mason_city_no_transport,
        'sioux_city_no_transport': sioux_city_no_transport,
        # Number of Scenes
        'des_moines_scenes': des_moines_scenes,
        'knoxville_scenes': knoxville_scenes,
        'mason_city_scenes': mason_city_scenes,
        'sioux_city_scenes': sioux_city_scenes,
        # Number of Interfacility Transports
        'des_moines_ift': des_moines_ift,
        'knoxville_ift': knoxville_ift,
        'mason_city_ift': mason_city_ift,
        'sioux_city_ift': sioux_city_ift,
        # Advanced Airway
        'des_moines_advanced_airway_in': des_moines_advanced_airway_in,
        'knoxville_advanced_airway_in': knoxville_advanced_airway_in,
        'mason_city_advanced_airway_in': mason_city_advanced_airway_in,
        'sioux_city_advanced_airway_in': sioux_city_advanced_airway_in,
        # Advanced Airway Placed by Transport Team
        'des_moines_adv_airway_by_flight_crew': des_moines_adv_airway_by_flight_crew,
        'knoxville_adv_airway_by_flight_crew': knoxville_adv_airway_by_flight_crew,
        'mason_city_adv_airway_by_flight_crew': mason_city_adv_airway_by_flight_crew,
        'sioux_city_adv_airway_by_flight_crew': sioux_city_adv_airway_by_flight_crew,
        # RSI Utilized
        'des_moines_rsi_utlized': des_moines_rsi_utlized,
        'knoxville_rsi_utlized': knoxville_rsi_utlized,
        'mason_city_rsi_utlized': mason_city_rsi_utlized,
        'sioux_city_rsi_utlized': sioux_city_rsi_utlized,
        # Intubation in Transport Vehicle
        'des_moines_intbation_in_vehicle': des_moines_intbation_in_vehicle,
        'knoxville_intbation_in_vehicle': knoxville_intbation_in_vehicle,
        'mason_city_intbation_in_vehicle': mason_city_intbation_in_vehicle,
        'sioux_city_intbation_in_vehicle': sioux_city_intbation_in_vehicle,
        # FirstAttemptIntubation
        'des_moines_intubation_on_first_attempt_percent': des_moines_intubation_on_first_attempt_percent,

        # Advanced Airway Types
        'des_moines_airway_type': des_moines_airway_type,
        'knoxville_airway_type': knoxville_airway_type,
        'mason_city_airway_type': mason_city_airway_type,
        'sioux_city_airway_type': sioux_city_airway_type,

        # ETCO2
        'des_moines_etco2_percent': des_moines_etco2_percent,
        'knoxville_etco2_percent': knoxville_etco2_percent,
        'mason_city_etco2_percent': mason_city_etco2_percent,
        'sioux_city_etco2_percent': sioux_city_etco2_percent,

        # Invasive Ventilation
        'des_moines_invasive_vent_percent': des_moines_invasive_vent_percent,
        # Pt Temp Documented
        'des_moines_temp_percent': des_moines_temp_percent,
        'knoxville_temp_percent': knoxville_temp_percent,
        'mason_city_temp_percent': mason_city_temp_percent,
        'sioux_city_temp_percent': sioux_city_temp_percent,



        'des_moines_adv_airway_type': des_moines_adv_airway_type,




    }
    return render(request, 'quality_dashboard/quality_dashboard.html', context)


def upload_qi_csv(request):
    if request.method == 'POST':
        new_qi_data = request.FILES["excel_file"]
        if not new_qi_data.name.endswith('.csv'):
            messages.error(request, "Not Valid File Type")
            return HttpResponseRedirect('quality_dashboard/upload_csv.html')

        conn = psycopg2.connect(database="airmed_db",
                                host="localhost",
                                user="postgres",
                                password="medic9367",
                                port="5433")

        print("Database Connected....")
        cur = conn.cursor()
        cur.execute("DROP TABLE AdultQuality")

        cur.execute(
            "CREATE TABLE AdultQuality("
            "flight_num CHAR(100),"
            "mission_date DATE,"
            "mission_num CHAR(50),"
            "base CHAR(50),"
            "ref_company CHAR(250),"
            "rec_company CHAR(250),"
            "staff_attendant_1 CHAR(250),"
            "staff_attendant_2 CHAR(250),"
            "vehicle_name CHAR(50),"
            "mission_type_id CHAR(250),"
            "camtsCategoryAdult CHAR(1000),"
            "wasThisANoPatientTransport CHAR(50),"
            "wasThePatientTransportedWithAnAdvancedAirwayInPlace CHAR(50),"
            "wasTheAdvancedAirwayAChronicTracheostomyTubeAndThePatientDidNotNeedVentilatorSupportManagementForTheirAirway CHAR(50),"
            "whatAdvancedAirwayDeviceWasInPlace CHAR(250),"
            "wasTheSupraglotticAirwayPlacedAfterUnsuccessfulIntubationAttempts CHAR(50),"
            "wasTheAdvancedAirwayPlacedByTheTransportTeam CHAR(50),"
            "wasThereDocumentationOfAtLeast2FormsOfConfirmationOfTheAdvancedAirwayCorrectPlacement CHAR(50),"
            "wasInvasiveVentilationUsedOnThePatientWithAnAdvancedAirway CHAR(50),"
            "wasWaveformCapnographyUsedThroughoutTransport CHAR(50),"
            "wasTheSpO2Ever90OrAbove CHAR(50),"
            "didThePulseOximetryFallBelow90DuringOurCare CHAR(50),"
            "wasTheSpO293 CHAR(50),"
            "wasSupplementalOxygenAdministered CHAR(50),"
            "medical_oxygenation_didSupplementalOxygenMaintainSpO293 char(50),"
            "wasPatientTransportedWithAppropriateVascularAccess CHAR(50),"
            "wasCardiopulmonaryResuscitationWithChestCompressionsRequiredWhileInTransportTeamCare CHAR(50),"
            "wereChestCompressionsPerformedInAMovingTransportVehicle CHAR(50),"
            "wasACommercialCprDeviceUsed CHAR(50),"
            "didPatientHaveReturnOfSpontaneousCirculation CHAR(50),"
            "wasAGcsDocumented CHAR(50),"
            "didThePatientHaveAnAlteredMentalStatusWithAGcs15AndOrAFocalNeurologicalDeficit CHAR(50),"
            "wasABloodGlucoseLevelMeasuredByEitherPreHospitalHospitalOrTransportTeamAndValueResultDocumentedByTheTransportTeam CHAR(50),"
            "wasAPtTempDocumented CHAR(50),"
            "wasThereDocumentationOfAPainAssessmentOrReasonWhyItCouldNotBeAssessed CHAR(50),"
            "werePainMedsGiven CHAR(50),"
            "wasAPainReassessmentDonePriorToTheEndOfTheTransportOrAReasonWhyItWasntDoneDocumented CHAR(50),"
            "wasTheSendingEmsAgencyNameDocumented CHAR(50),"
            "wasRsiUtilizedToSecureTheAirway CHAR(50),"
            "wasTheIntubationDoneInTransportVehicle CHAR(50),"
            "wasTheIntubationSuccessfulOnTheFirstAttempt CHAR(50),"
            "wasTheRsiChecklistUtilizedOrReasonDocumentedWhyItWasntUsed CHAR(50),"
            "wasTheRsiProtocolFollowed CHAR(50),"
            "explainRsiProtocolNotFollowedConcern CHAR(1000),"
            "wasTheVentUtilizedBedsideToBesideOrFromTimeOfIntubationToReceivingBedsideOrIfNotWasItDocumentedWhyItWasntDone CHAR(50),"
            "wasThePatientVentilatedInPressureOrVolumeMode CHAR(250),"
            "wasAPPlatDocumented CHAR(50),"
            "wasThePPlatGreaterThan30 CHAR(50),"
            "wasThereDocumentationOfStrategiesOnMeasuresToGetThePPlatBelow30 CHAR(50),"
            "wasAVteDocumented CHAR(50),"
            "wasSedationGivenPerProtocol CHAR(50),"
            "explainSedationConcerns CHAR(1000),"
            "postIntubationWereParalyticsGivenToThePatient CHAR(50),"
            "werePainMedsGivenIncludingKetamineAdministeredToTheIntubatedPt CHAR(50),"
            "didPatientExperienceAnySideEffectsOrTransfusionReaction CHAR(50),"
            "wasPatientTemperatureDocumented CHAR(50),"
            "wasBloodAdministeredAsAResultOfTraumaticInjury CHAR(50),"
            "wasThePatientPronouncedDead CHAR(50),"
            "wasItCalledByTheFlightCrew CHAR(50),"
            "wasTimeOfDeathDocumentedInChart CHAR(50),"
            "wasTheNameOfTheDoctorThatWasCalledToPronounceTheDeathNotedInTheChart CHAR(50),"
            "wasPatientTransportedToBurnCenter CHAR(50),"
            "wasTheCorrectVolumeOfIvfAdministeredBasedOnParklandFormula CHAR(50),"
            "wasPatientDiagnosedOrSuspectedCovid19Positive CHAR(50),"
            "wereLungProtectiveVentilatorSettings6MlKgUtilizedForIntubatedPatient CHAR(50),"
            "wasNihStrokeScoreDocumented CHAR(50),"
            "ifNihss4WasPatientTransportedToThrombectomyCapableFacility CHAR(50),"
            "wasPatientExperiencingAcuteCoronarySyndromeAcsOrStemi CHAR(50),"
            "wasThereDocumentationOf12LeadEcgInterpretationConsistentWithStElevationInPatientCareRecord CHAR(50),"
            "atAnyPointDuringTransportWereTheHrAndBloodPressureOutsideProtocolParametersHr5060Sbp90110MmHg CHAR(50),"
            "PRIMARY KEY (flight_num));")
        print("Table Created....")
        conn.commit()

        df = pd.read_csv(new_qi_data)

        # Delete columns with data that is not needed
        # del df.columns[]
        df.drop(columns=['Base Name', 'OASIS ID', 'Template ID', 'Status', 'Add Member Name', 'Add Date', 'Update Member Name',
                         'Last Update', 'Session Title', 'Priority', 'reviewerComments'], axis=1, inplace=True)
        # Change the Column Headings

        df.rename(columns={'Mission Number': 'flight_num'}, inplace=True)

        df.to_csv("new_output.csv", index=False)

        with open('new_output.csv', 'r') as f:
            next(f)

        with open('new_output.csv', 'r', encoding='utf-8-sig', newline='') as fin:
            dr = csv.DictReader(fin, delimiter=',')

            to_db = []
            for i in dr:
                to_db.append((i['flight_num'],
                              i['mission_date'],
                              i['mission_num'],
                              i['base'],
                              i['ref_company'],
                              i['rec_company'],
                              i['staff_attendant_1'],
                              i['staff_attendant_2'],
                              i['vehicle_name'],
                              i['mission_type_id'],

                              i['camtsCategoryAdult'],
                              i['wasThisANoPatientTransport'],
                              i['wasThePatientTransportedWithAnAdvancedAirwayInPlace'],
                              i['wasTheAdvancedAirwayAChronicTracheostomyTubeAndThePatientDidNotNeedVentilatorSupportManagementForTheirAirway'],
                              i['whatAdvancedAirwayDeviceWasInPlace'],
                              i['wasTheSupraglotticAirwayPlacedAfterUnsuccessfulIntubationAttempts'],
                              i['wasTheAdvancedAirwayPlacedByTheTransportTeam'],
                              i['wasThereDocumentationOfAtLeast2FormsOfConfirmationOfTheAdvancedAirwayCorrectPlacement'],
                              i['wasInvasiveVentilationUsedOnThePatientWithAnAdvancedAirway'],
                              i['wasWaveformCapnographyUsedThroughoutTransport'],

                              i['wasTheSpO2Ever90OrAbove'],
                              i['didThePulseOximetryFallBelow90DuringOurCare'],
                              i['wasTheSpO293'],
                              i['wasSupplementalOxygenAdministered'],
                              i['medical_oxygenation_didSupplementalOxygenMaintainSpO293'],
                              i['wasPatientTransportedWithAppropriateVascularAccess'],
                              i['wasCardiopulmonaryResuscitationWithChestCompressionsRequiredWhileInTransportTeamCare'],
                              i['wereChestCompressionsPerformedInAMovingTransportVehicle'],
                              i['wasACommercialCprDeviceUsed'],
                              i['didPatientHaveReturnOfSpontaneousCirculation'],

                              i['wasAGcsDocumented'],
                              i['didThePatientHaveAnAlteredMentalStatusWithAGcs15AndOrAFocalNeurologicalDeficit'],
                              i['wasABloodGlucoseLevelMeasuredByEitherPreHospitalHospitalOrTransportTeamAndValueResultDocumentedByTheTransportTeam'],
                              i['wasAPtTempDocumented'],
                              i['wasThereDocumentationOfAPainAssessmentOrReasonWhyItCouldNotBeAssessed'],
                              i['werePainMedsGiven'],
                              i['wasAPainReassessmentDonePriorToTheEndOfTheTransportOrAReasonWhyItWasntDoneDocumented'],
                              i['wasTheSendingEmsAgencyNameDocumented'],
                              i['wasRsiUtilizedToSecureTheAirway'],
                              i['wasTheIntubationDoneInTransportVehicle'],

                              i['wasTheIntubationSuccessfulOnTheFirstAttempt'],
                              i['wasTheRsiChecklistUtilizedOrReasonDocumentedWhyItWasntUsed'],
                              i['wasTheRsiProtocolFollowed'],
                              i['explainRsiProtocolNotFollowedConcern'],
                              i['wasTheVentUtilizedBedsideToBesideOrFromTimeOfIntubationToReceivingBedsideOrIfNotWasItDocumentedWhyItWasntDone'],
                              i['wasThePatientVentilatedInPressureOrVolumeMode'],
                              i['wasAPPlatDocumented'],
                              i['wasThePPlatGreaterThan30'],
                              i['wasThereDocumentationOfStrategiesOnMeasuresToGetThePPlatBelow30'],
                              i['wasAVteDocumented'],

                              i['wasSedationGivenPerProtocol'],
                              i['explainSedationConcerns'],
                              i['postIntubationWereParalyticsGivenToThePatient'],
                              i['werePainMedsGivenIncludingKetamineAdministeredToTheIntubatedPt'],
                              i['didPatientExperienceAnySideEffectsOrTransfusionReaction'],
                              i['wasPatientTemperatureDocumented'],
                              i['wasBloodAdministeredAsAResultOfTraumaticInjury'],
                              i['wasThePatientPronouncedDead'],
                              i['wasItCalledByTheFlightCrew'],
                              i['wasTimeOfDeathDocumentedInChart'],

                              i['wasTheNameOfTheDoctorThatWasCalledToPronounceTheDeathNotedInTheChart'],
                              i['wasPatientTransportedToBurnCenter'],
                              i['wasTheCorrectVolumeOfIvfAdministeredBasedOnParklandFormula'],
                              i['wasPatientDiagnosedOrSuspectedCovid19Positive'],
                              i['wereLungProtectiveVentilatorSettings6MlKgUtilizedForIntubatedPatient'],
                              i['wasNihStrokeScoreDocumented'],
                              i['ifNihss4WasPatientTransportedToThrombectomyCapableFacility'],
                              i['wasPatientExperiencingAcuteCoronarySyndromeAcsOrStemi'],
                              i['wasThereDocumentationOf12LeadEcgInterpretationConsistentWithStElevationInPatientCareRecord'],
                              i['atAnyPointDuringTransportWereTheHrAndBloodPressureOutsideProtocolParametersHr5060Sbp90110MmHg']))

                cur.executemany("INSERT INTO AdultQuality ("
                                "flight_num,"
                                "mission_date,"
                                "mission_num,"
                                "base,"
                                "ref_company,"
                                "rec_company,"
                                "staff_attendant_1,"
                                "staff_attendant_2,"
                                "vehicle_name,"
                                "mission_type_id,"

                                "camtsCategoryAdult,"
                                "wasThisANoPatientTransport,"
                                "wasThePatientTransportedWithAnAdvancedAirwayInPlace,"
                                "wasTheAdvancedAirwayAChronicTracheostomyTubeAndThePatientDidNotNeedVentilatorSupportManagementForTheirAirway,"
                                "whatAdvancedAirwayDeviceWasInPlace,"
                                "wasTheSupraglotticAirwayPlacedAfterUnsuccessfulIntubationAttempts,"
                                "wasTheAdvancedAirwayPlacedByTheTransportTeam,"
                                "wasThereDocumentationOfAtLeast2FormsOfConfirmationOfTheAdvancedAirwayCorrectPlacement,"
                                "wasInvasiveVentilationUsedOnThePatientWithAnAdvancedAirway,"
                                "wasWaveformCapnographyUsedThroughoutTransport,"

                                "wasTheSpO2Ever90OrAbove,"
                                "didThePulseOximetryFallBelow90DuringOurCare,"
                                "wasTheSpO293,"
                                "wasSupplementalOxygenAdministered,"
                                "medical_oxygenation_didSupplementalOxygenMaintainSpO293,"
                                "wasPatientTransportedWithAppropriateVascularAccess,"
                                "wasCardiopulmonaryResuscitationWithChestCompressionsRequiredWhileInTransportTeamCare,"
                                "wereChestCompressionsPerformedInAMovingTransportVehicle,"
                                "wasACommercialCprDeviceUsed,"
                                "didPatientHaveReturnOfSpontaneousCirculation,"

                                "wasAGcsDocumented, "
                                "didThePatientHaveAnAlteredMentalStatusWithAGcs15AndOrAFocalNeurologicalDeficit,"
                                "wasABloodGlucoseLevelMeasuredByEitherPreHospitalHospitalOrTransportTeamAndValueResultDocumentedByTheTransportTeam,"
                                "wasAPtTempDocumented,"
                                "wasThereDocumentationOfAPainAssessmentOrReasonWhyItCouldNotBeAssessed,"
                                "werePainMedsGiven,"
                                "wasAPainReassessmentDonePriorToTheEndOfTheTransportOrAReasonWhyItWasntDoneDocumented,"
                                "wasTheSendingEmsAgencyNameDocumented,"
                                "wasRsiUtilizedToSecureTheAirway,"
                                "wasTheIntubationDoneInTransportVehicle,"

                                "wasTheIntubationSuccessfulOnTheFirstAttempt,"
                                "wasTheRsiChecklistUtilizedOrReasonDocumentedWhyItWasntUsed,"
                                "wasTheRsiProtocolFollowed,"
                                "explainRsiProtocolNotFollowedConcern,"
                                "wasTheVentUtilizedBedsideToBesideOrFromTimeOfIntubationToReceivingBedsideOrIfNotWasItDocumentedWhyItWasntDone,"
                                "wasThePatientVentilatedInPressureOrVolumeMode,"
                                "wasAPPlatDocumented,"
                                "wasThePPlatGreaterThan30,"
                                "wasThereDocumentationOfStrategiesOnMeasuresToGetThePPlatBelow30,"
                                "wasAVteDocumented,"

                                "wasSedationGivenPerProtocol,"
                                "explainSedationConcerns,"
                                "postIntubationWereParalyticsGivenToThePatient,"
                                "werePainMedsGivenIncludingKetamineAdministeredToTheIntubatedPt,"
                                "didPatientExperienceAnySideEffectsOrTransfusionReaction,"
                                "wasPatientTemperatureDocumented,"
                                "wasBloodAdministeredAsAResultOfTraumaticInjury,"
                                "wasThePatientPronouncedDead,"
                                "wasItCalledByTheFlightCrew,"
                                "wasTimeOfDeathDocumentedInChart,"

                                "wasTheNameOfTheDoctorThatWasCalledToPronounceTheDeathNotedInTheChart,"
                                "wasPatientTransportedToBurnCenter,"
                                "wasTheCorrectVolumeOfIvfAdministeredBasedOnParklandFormula,"
                                "wasPatientDiagnosedOrSuspectedCovid19Positive,"
                                "wereLungProtectiveVentilatorSettings6MlKgUtilizedForIntubatedPatient,"
                                "wasNihStrokeScoreDocumented,"
                                "ifNihss4WasPatientTransportedToThrombectomyCapableFacility,"
                                "wasPatientExperiencingAcuteCoronarySyndromeAcsOrStemi,"
                                "wasThereDocumentationOf12LeadEcgInterpretationConsistentWithStElevationInPatientCareRecord,"
                                "atAnyPointDuringTransportWereTheHrAndBloodPressureOutsideProtocolParametersHr5060Sbp90110MmHg)"
                                "VALUES("
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                "ON CONFLICT (flight_num) DO NOTHING;", to_db)

        conn.commit()
        conn.close()
        return render(request, 'flight_data/data_upload_success.html')
    else:
        return render(request, 'quality_dashboard/upload_csv.html')
