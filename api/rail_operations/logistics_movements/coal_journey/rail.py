from mongoengine import Q,DoesNotExist
import os,datetime,re
from dateutil.relativedelta import relativedelta
from api import short_mine_collection
from api.logger.logger import console_logger
from api.service.helpers import helpers
from fastapi import HTTPException
from api.service.models import (
    RailData,
    sapRecordsRail,
    SeclRailData,
    AveryRailData,
    Grn
)
from bson.objectid import ObjectId
import camelot
import pdftotext

class CoalJourneyDashboard:

    def __init__(self) -> None:
        self.service_id = os.environ.get("SERVICE_ID", "gmr_api")

    def search_text(self, pending_query, completed_query, search_text):
        if search_text.isdigit():
            query_filter = (Q(rr_no__icontains=search_text) | Q(po_no__icontains=search_text))
        else:
            query_filter = Q(source__icontains=search_text)

        pending_query &= query_filter
        completed_query &= query_filter

        return pending_query, completed_query
            
    def coal_journey_rail_pending(self, currentPage, perPage,search_text, start_timestamp, end_timestamp, month_date):
        try:
            result = {
                "labels": [],
                "records": [],
                "count": {
                    "pending": 0,
                    "completed": 0
                },
                "page_size": perPage or 15,
                "page_no": currentPage or 1
            }

            page_no = currentPage or 1
            page_len = 10 

            pending_data = Q(avery_placement_date =None)
            completed_data = Q(avery_placement_date__ne =None)

            if search_text:
                pending_data, completed_data = self.search_text(pending_data, completed_data, search_text)
                
            try:
                if start_timestamp:
                    # start_date = helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M")
                    pending_data &= Q(placement_date__gte=start_timestamp)

                if end_timestamp:
                    # end_date = helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M","Asia/Kolkata",False)
                    pending_data &= Q(placement_date__lte=end_timestamp)

                if month_date:
                    start_date = f'{month_date}-01'
                    startd_date=datetime.datetime.strptime(f"{start_date}T00:00","%Y-%m-%dT%H:%M")
                    end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(day=31)).strftime("%Y-%m-%d")
                    pending_data &= Q(placement_date__gte=startd_date.strftime("%Y-%m-%dT%H:%M"))
                    pending_data &= Q(placement_date__lte=f"{end_date}T23:59")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
                
            offset = (page_no - 1) * page_len

            try:
                logs = (RailData.objects(pending_data)
                        .order_by("-placement_date").
                        skip(offset).
                        limit(page_len)
                        )
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RailData")
            
            if any(logs):
                for log in logs:
                    result["labels"] = list(log.simplepayload().keys())
                    result["records"].append(log.simplepayload())

            result["count"]["pending"] = RailData.objects(pending_data).count()
            result["count"]["completed"] = RailData.objects(completed_data).count()

            return result
        
        except Exception as e:
           helpers.error_handler(e)  
           raise e
           
    def coal_journey_rail_completed(self, currentPage, perPage, search_text, start_timestamp, end_timestamp , month_date):
        try:
            result = {        
                "labels": [],
                "datasets": [],
                "count": {
                    "pending": 0,
                    "completed": 0
                },
                "page_size": perPage or  15,
                "page_no":currentPage or 1
            }

            pending_data = Q(avery_placement_date =None)
            completed_data = Q(avery_placement_date__ne =None)

            page_no =currentPage or 1
            page_len = result["page_size"]

            if search_text:
                pending_data, completed_data = self.search_text(pending_data, completed_data, search_text)

            try:
                if start_timestamp:
                    start_date = helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M")
                    completed_data &= Q(avery_placement_date__gte = start_date)

                if end_timestamp:
                    end_date = helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M","Asia/Kolkata",False)
                    completed_data &= Q(avery_placement_date__lte = end_date)

                if month_date:
                    start_date = f'{month_date}-01'
                    startd_date=datetime.datetime.strptime(f"{start_date}T00:00:00","%Y-%m-%dT%H:%M:%S")
                    end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(day=31)).strftime("%Y-%m-%d")
                    completed_data &= Q(avery_placement_date__gte = startd_date.strftime("%Y-%m-%dT%H:%M:%S"))
                    completed_data &= Q(avery_placement_date__lte = f"{end_date}T23:59:59")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
                    
            offset = (page_no - 1) * page_len

            try:
                logs = (
                        RailData.objects(completed_data)
                        .order_by("-avery_placement_date", "-avery_completion_date")
                        .skip(offset)
                        .limit(page_len)
                    )
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RailData")
            
            listData = []
            if any(logs):
                for log in logs:
                    payload = log.averyPayloadMain()

                    try:
                        fetch_grn_no = Grn.objects.get(do_no=payload.get("rr_no"), grn_completed=True)
                        if fetch_grn_no.grn_no:
                            payload["grn_no"] = fetch_grn_no.grn_no
                        else:
                            payload["grn_no"] = "N/A"
                    except Exception as e:
                        payload["grn_no"] = "N/A"
                        
                    payload['total_gwel_gross_wt'] = 0
                    payload['total_gwel_tare_wt'] = 0
                    payload['total_gwel_net_wt'] = 0
                    
                    fields = [
                        "adho_sanrachna_vikas", "assessable_value", "dmf", "evac_facility_charge",
                        "gross_bill_value", "gst_comp_cess", "igst", "less_underloading_charges",
                        "net_value", "nmet_charges", "pariyavaran_upkar", "sizing_charges",
                        "royality_charges", "total_amount"
                    ]

                    try:
                        fetchsapDatarails = sapRecordsRail.objects.get(rr_no=log.rr_no)
                        for field in fields:
                            payload[field] = getattr(fetchsapDatarails, field, 0) or 0

                    except Exception as e:
                        for field in fields:
                            payload[field] = 0
                        
                    if log.avery_rly_data:
                        total_wagon_gross_wt = 0
                        total_wagon_tare_wt = 0
                        total_wagon_net_wt = 0
                        for singleRailData in log.avery_rly_data:
                                # Handle wagon_gross_wt
                            if singleRailData.gwel_gross_wt:
                                try:
                                    # total_wagon_gross_wt += float(singleRailData.gwel_gross_wt)
                                    total_wagon_gross_wt += float(singleRailData.gwel_gross_wt)
                                except ValueError:
                                    print(f"Warning: Invalid data for wagon_gross_wt: {singleRailData.gwel_gross_wt}")

                                # Handle wagon_tare_wt
                            if singleRailData.gwel_tare_wt:
                                try:
                                    total_wagon_tare_wt += float(singleRailData.gwel_tare_wt)
                                except ValueError:
                                    print(f"Warning: Invalid data for wagon_tare_wt: {singleRailData.gwel_tare_wt}")

                                # Handle wagon_net_wt
                            if singleRailData.gwel_net_wt:
                                try:
                                    total_wagon_net_wt += float(singleRailData.gwel_net_wt)
                                except ValueError:
                                    print(f"Warning: Invalid data for wagon_net_wt: {singleRailData.gwel_net_wt}")
                            payload['total_gwel_gross_wt'] = round(total_wagon_gross_wt, 2)
                            payload['total_gwel_tare_wt'] = round(total_wagon_tare_wt, 2)
                            payload['total_gwel_net_wt'] = round(total_wagon_net_wt, 2)
                                # payload["GWEL_received_wagons"] = gwel_received_wagons
                                # payload["GWEL_pending_wagons"] = int(log.boxes_loaded) - int(gwel_received_wagons)

                    else:
                        console_logger.debug("inside else")
                        if log.Total_gwel_net:
                            payload['total_gwel_net_wt'] = round(float(log.Total_gwel_net), 2)
                        # result["labels"] = list(payload.keys())

                    result["datasets"].append(payload)

                result["labels"] = ["rr_no", "rr_qty", "po_no", "po_date", "line_item", "source", 
                                    "GWEL_placement_date", "GWEL_completion_date", "GWEL_received_wagons", "GWEL_pending_wagons", 
                                    "boxes_loaded", "total_secl_gross_wt", "total_secl_tare_wt", "total_secl_net_wt", 
                                    "total_rly_gross_wt", "total_rly_tare_wt", "total_rly_net_wt", "total_gwel_gross_wt", 
                                    "total_gwel_tare_wt", "total_gwel_net_wt", "source_type", "month", "rr_date", 
                                    "siding", "mine", "grade", "adho_sanrachna_vikas", "assessable_value", "dmf", 
                                    "evac_facility_charge", "gross_bill_value", "gst_comp_cess", "igst", "less_underloading_charges", 
                                    "net_value", "nmet_charges", "pariyavaran_upkar", "sizing_charges", "royality_charges", 
                                    "total_amount", "freight", "gst", "pola", "total_freight", "sd", "created_at"]
                
            result["count"]["pending"] = RailData.objects(pending_data).count()
            result["count"]["completed"] = RailData.objects(completed_data).count()

            return result
        
        except Exception as e:
            helpers.error_handler(e)
            raise e 


    def coal_journey_rail_allminenames(self):
        try:
            try:
                mine_names = short_mine_collection.find({})
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing short_mine")
            dictData = {}
            railData = {}
            roadData = {}
            for single_data in mine_names:
                if single_data.get("coal_journey") == "Rail":
                    railData[single_data.get("mine_name")] = single_data.get("source_type")
                    # railData.append(single_data.get("mine_name"))
                if single_data.get("coal_journey") == "Road":
                    # roadData.append(single_data.get("mine_name"))
                    roadData[single_data.get("mine_name")] = single_data.get("source_type")
            
            dictData["road"] = roadData
            dictData["rail"] = railData

            return dictData
        except Exception as e:
            helpers.error_handler(e)
            raise e
    def update_dictionary(self,data):
        try:
            # Check if key 2 is empty and key 3 contains a space
            if data[2] == '' and ' ' in data[3]:
                # Split the value at key 3 by the first space
                parts = data[3].split(' ', 1)
                data[2] = parts[0]
                data[3] = parts[1]
            return data
        except Exception as e:
            helpers.error_handler(e)
    def outbond(self,pdf_path):
        try:
            abc = camelot.read_pdf(pdf_path, flavor="stream", compress=True, pages="all")
            filtered_tables_data = []
            for table in abc:
                df = table.df
                if df.applymap(lambda cell: "Wagon Details" in cell).any().any():
                    filtered_tables_data.extend(df.to_dict(orient="records"))
            return filtered_tables_data
        except Exception as e:
            helpers.error_handler(e)
    
    def extract_pdf_data(self,file_path):
        try:
            with open(file_path, "rb") as f:
                pdf = pdftotext.PDF(f, raw=True)
                output_string = pdf[0]
            patterns = {
                "RR_NO": r"RR NO\.\s*(\d+)",
                "RR_DATE": r"RR DATE\s*(\d{2}-\d{2}-\d{4})",
                "FREIGHT": r"FREIGHT:\s*([\d.]+)",
                "TOTAL_FREIGHT": r"TOTAL FREIGHT:\s*([\d.]+)",
                "SD": r"SD\s*([\d.]+)",
                "POLA": r"POLA\s*([\d.]+)",
                "GST": r"\*GST\s*(\d+)",
            }
            data_dictionary = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, output_string)
                data_dictionary[key] = match.group(1) if match else "Not found"
            return data_dictionary
        except Exception as e:
            helpers.error_handler(e)       
             
    async def coal_journey_rail_singlerail(self, rrno):
        """
        Function that fetches single railway data using rrno
        Parameters:
            rr_no

        Returns:
            single dictionary data for particular rr_no
        """
        try:
            fetchRailData = RailData.objects.get(rr_no=rrno)
            return fetchRailData.payload()
        except DoesNotExist as e:
            raise HTTPException(status_code=404, detail="No data found")
        except Exception as e:
            helpers.error_handler(e)


    def coal_journey_rail_mine_shortcodes_sourcetype(self):
        try:
            sourcetype = []
            try:
                result = short_mine_collection.find({},{"_id":0})
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing short_mine")
            for single_data in result:
                if single_data["source_type"] is not None:
                    sourcetype.append(single_data["source_type"])
            return sourcetype
        
        except Exception as e:
            helpers.error_handler(e)


    def coal_journey_avery_singlerail(self, rrno: str):
        try:
            try:
                fetchRailData = RailData.objects.get(rr_no=rrno)
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RailData")
            dictData = fetchRailData.averyPayload()
            if fetchRailData.avery_placement_date and fetchRailData.avery_completion_date:
                dictData["avery_placement"] = fetchRailData.avery_placement_date
                dictData["avery_completion"] = fetchRailData.avery_completion_date
            else:
                if fetchRailData.avery_rly_data:
                    startlistData = []
                    endlistData = []
                    for singleRailData in fetchRailData.avery_rly_data:
                        if singleRailData.tip_startdate and singleRailData.tip_starttime:
                            start_dated_date = f'{datetime.datetime.strptime(singleRailData.tip_startdate, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d")} {singleRailData.tip_starttime}'
                            startlistData.append(start_dated_date)
                        if singleRailData.tip_enddate and singleRailData.tip_endtime:
                            end_dated_date = f'{datetime.datetime.strptime(singleRailData.tip_startdate, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d")} {singleRailData.tip_starttime}'
                            endlistData.append(end_dated_date)
                    
                    if startlistData and endlistData:
                        dictData["avery_placement"] = startlistData[0]
                        dictData["avery_completion"] = endlistData[-1]
                    else:
                        dictData["avery_placement"] = ""
                        dictData["avery_completion"] = ""
                else:
                    dictData["avery_placement"] = ""
                    dictData["avery_completion"] = ""
                
            mongoPipeline = [
                {
                    '$match': {
                        'rr_no': rrno,
                    }
                }, {
                    '$unwind': '$avery_rly_data'
                }, {
                    '$match': {
                        'avery_rly_data.po_number': {
                            '$exists': True
                        }
                    }
                }, {
                    '$group': {
                        '_id': None, 
                        'count': {
                            '$sum': 1
                        }
                    }
                }
            ]
            try:
                railDataobjects = RailData.objects().aggregate(mongoPipeline)
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RailData")
            
            railData_result = list(railDataobjects)
            if railData_result:
                dictData["total_avery"] = railData_result[0].get("count")
            else:
                dictData["total_avery"] = 0
            return dictData

        except Exception as e:
            helpers.error_handler(e)
            raise e
    
    
    def calculate_rake_no(self,month, placement_date, existing_rake_nos):
        try:
            month_start_date = datetime.datetime.strptime(month, '%Y-%m-%d')
            placement_date_obj = datetime.datetime.strptime(placement_date, '%Y-%m-%d')
            next_month_start_date = month_start_date + datetime.timedelta(days=32)
            next_month_3rd = next_month_start_date.replace(day=3)
            if month_start_date.replace(day=4) <= placement_date_obj <= next_month_3rd:
                rake_no_base = "1"
            else:
                rake_no_base = "rev1"
            filtered_rake_nos = [rake for rake in existing_rake_nos if rake is not None]
            if "rev" in rake_no_base:
                # Filter out rake numbers that start with "rev"
                rev_list = [x for x in filtered_rake_nos if x.startswith("rev")]
                if rev_list:
                    # Extract the numeric part and find the maximum value
                    max_rev_number = max(int(x.split("rev")[1]) for x in rev_list)
                    # Increment the maximum value
                    rake_no_base = f"rev{max_rev_number + 1}"
                else:
                    rake_no_base = "rev1"
            else:
                # console_logger.debug("rev is absent")
                number_list = [int(x) for x in filtered_rake_nos if x.isdigit()]
                if number_list:
                    max_number = max(number_list)
                    rake_no_base = str(max_number + 1)
                else:
                    rake_no_base = "1" 
            return rake_no_base
        except Exception as e:
            helpers.error_handler(e)
    
    def coal_journey_rail_insert(self, payload, id):
        try:
            final_data = payload.dict()
            try:
                if id:
                    fetchRailData = RailData.objects.get(id=ObjectId(id))
                else:
                    fetchRailData = RailData.objects.get(rr_no=final_data.get("rr_no"))
                try:
                    fetchSaprecordsRail = sapRecordsRail.objects.get(rr_no=final_data.get("rr_no"))
                except DoesNotExist as e:
                    fetchSaprecordsRail = None
                avery_rail_data = fetchRailData.avery_rly_data
                if fetchSaprecordsRail:
                    # commented on 25032025 12:21 said by sachin bhai
                    # if 
                    # if fetchSaprecordsRail.month:
                        # if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fetchSaprecordsRail.month):
                        #     fetchRailData.month = datetime.datetime.strptime(fetchSaprecordsRail.month, '%Y-%m-%d').strftime('%Y-%m-%d')
                        # else:
                        #     fetchRailData.month = datetime.datetime.strptime(fetchSaprecordsRail.month, '%b %d, %Y').strftime('%Y-%m-%d')
                    fetchRailData.rr_date = fetchSaprecordsRail.rr_date
                    fetchRailData.siding = fetchSaprecordsRail.siding
                    fetchRailData.mine = fetchSaprecordsRail.mine
                    fetchRailData.grade = fetchSaprecordsRail.grade
                    fetchRailData.rr_qty = fetchSaprecordsRail.rr_qty
                    fetchRailData.po_amount = fetchSaprecordsRail.po_amount
                
                fetchRailData.placement_date = final_data.get("placement_date")
                fetchRailData.completion_date = final_data.get("completion_date")
                fetchRailData.drawn_date = final_data.get("drawn_date")
                fetchRailData.total_ul_wt = final_data.get("total_ul_wt")
                fetchRailData.boxes_supplied = final_data.get("boxes_supplied")
                fetchRailData.total_secl_gross_wt = final_data.get("total_secl_gross_wt")
                fetchRailData.total_secl_tare_wt = final_data.get("total_secl_tare_wt")
                fetchRailData.total_secl_net_wt = final_data.get("total_secl_net_wt")
                fetchRailData.total_secl_ol_wt = final_data.get("total_secl_ol_wt")
                fetchRailData.boxes_loaded = final_data.get("boxes_loaded")
                fetchRailData.total_rly_gross_wt = final_data.get("total_rly_gross_wt")
                fetchRailData.total_rly_tare_wt = final_data.get("total_rly_tare_wt")
                fetchRailData.total_rly_net_wt = final_data.get("total_rly_net_wt")
                fetchRailData.total_rly_ol_wt = final_data.get("total_rly_ol_wt")
                fetchRailData.total_secl_chargable_wt = final_data.get("total_secl_chargable_wt")
                fetchRailData.total_rly_chargable_wt = final_data.get("total_rly_chargable_wt")
                fetchRailData.freight = final_data.get("freight")
                fetchRailData.gst = final_data.get("gst")
                fetchRailData.avery_placement_date = final_data.get("avery_placement_date")
                fetchRailData.avery_completion_date = final_data.get("avery_completion_date")
                fetchRailData.GWEL_pending_wagons = final_data.get("GWEL_pending_wagons")
                fetchRailData.GWEL_received_wagons = final_data.get("GWEL_received_wagons")
                # added on 25032025 12:24
                fetchRailData.month = final_data.get("month")
                if final_data.get("pola") == "Not found":
                    fetchRailData.pola = ""
                else:
                    fetchRailData.pola = final_data.get("pola")
                if final_data.get("sd") == "Not found":
                    fetchRailData.sd = ""
                else:
                    fetchRailData.sd = final_data.get("sd")
                fetchRailData.total_freight = final_data.get("total_freight")
                fetchRailData.source_type = final_data.get("source_type")
                # fetchRailData.month = final_data.get("month")

                for key, value in final_data.items():
                    if key != 'secl_rly_data' and hasattr(fetchRailData, key):
                        setattr(fetchRailData, key, value)

                
                # for new_data in final_data.get('secl_rly_data', []):
                #     updated = False
                #     wagon_no = new_data.get('wagon_no')
                #     if wagon_no is None:
                #         # Log, skip, or raise custom error if this field is essential
                #         continue  # or log a warning

                #     for secl_data in fetchRailData.secl_rly_data:
                #         if secl_data.wagon_no == wagon_no:
                #             for key, value in new_data.items():
                #                 setattr(secl_data, key, value)
                #             updated = True
                #             break  # break here to avoid unnecessary iterations
                #     if not updated:
                #         fetchRailData.secl_rly_data.append(SeclRailData(**new_data))
                for new_data in final_data.get('secl_rly_data', []):
                    updated = False
                    for secl_data in fetchRailData.secl_rly_data:
                        if secl_data.wagon_no == new_data['wagon_no']:
                            for key, value in new_data.items():
                                setattr(secl_data, key, value)
                            updated = True
                            break
                
                    if not updated:
                        fetchRailData.secl_rly_data.append(SeclRailData(**new_data))
            
                
                if not avery_rail_data:
                    listAveryData = []
                    for new_data in final_data.get('secl_rly_data', []):
                        dictAveryData = {}
                        dictAveryData["indexing"] = new_data.get("indexing")
                        dictAveryData["wagon_owner"] = new_data.get("wagon_owner")
                        dictAveryData["wagon_type"] = new_data.get("wagon_type")
                        dictAveryData["wagon_no"] = new_data.get("wagon_no")
                        listAveryData.append(AveryRailData(**dictAveryData))
                    
                    fetchRailData.avery_rly_data = listAveryData
                else:
                    fetchRailData.avery_rly_data = avery_rail_data
                fetchRailData.save()

                return {"detail": "success"}
            
            except DoesNotExist as e:
                final_data = payload.dict()
                secl_list_data = []
                for single_data in final_data.get("secl_rly_data"):
                    secl_rly_dict_data = {
                        "indexing": single_data.get("indexing"),
                        "wagon_owner": single_data.get("wagon_owner"),
                        "wagon_type": single_data.get("wagon_type"),
                        "wagon_no": single_data.get("wagon_no"),
                        "secl_cc_wt": single_data.get("secl_cc_wt"),
                        "secl_gross_wt": single_data.get("secl_gross_wt"),
                        "secl_tare_wt": single_data.get("secl_tare_wt"),
                        "secl_net_wt": single_data.get("secl_net_wt"),
                        "secl_ol_wt": single_data.get("secl_ol_wt"),
                        "secl_ul_wt":single_data.get("secl_ul_wt"),
                        "secl_chargable_wt": single_data.get("secl_chargable_wt"),
                        "rly_cc_wt": single_data.get("rly_cc_wt"),
                        "rly_gross_wt": single_data.get("rly_gross_wt"),
                        "rly_tare_wt": single_data.get("rly_tare_wt"),
                        "rly_net_wt": single_data.get("rly_net_wt"),
                        "rly_permissible_cc_wt": single_data.get("rly_permissible_cc_wt"),
                        "rly_ol_wt": single_data.get("rly_ol_wt"),
                        "rly_norm_rate": single_data.get("rly_norm_rate"),
                        "rly_pun_rate": single_data.get("rly_pun_rate"),
                        "rly_chargable_wt": single_data.get("rly_chargable_wt"),
                        "rly_sliding_adjustment": single_data.get("rly_sliding_adjustment"),
                    }
                    secl_list_data.append(secl_rly_dict_data)

                avery_list_data = []
                
                for single_data in final_data.get("secl_rly_data"):
                    avery_rly_dict_data = {
                        "indexing": single_data.get("indexing"),
                        "wagon_owner": single_data.get("wagon_owner"),
                        "wagon_type": single_data.get("wagon_type"),
                        "wagon_no": single_data.get("wagon_no"),
                    }
                    avery_list_data.append(avery_rly_dict_data)
                try:
                    fetchSaprecordsRail = sapRecordsRail.objects.get(rr_no=final_data.get("rr_no"))
                except DoesNotExist as e:
                    fetchSaprecordsRail = None
                # console_logger.debug(final_data.get("sd"))
                console_logger.debug(final_data.get("total_secl_gross_wt"))
                console_logger.debug(final_data.get("total_secl_tare_wt"))
                console_logger.debug(final_data.get("total_secl_net_wt"))
                console_logger.debug(final_data.get("total_secl_ol_wt"))
                rail_data = RailData(
                    rr_no=final_data.get("rr_no"),
                    # rr_qty=final_data.get("rr_qty"),
                    rr_qty=fetchSaprecordsRail.rr_qty if fetchSaprecordsRail and fetchSaprecordsRail.rr_qty else 0,
                    po_no=final_data.get("po_no"),
                    po_date=final_data.get("po_date"),
                    line_item=final_data.get("line_item"),
                    source=final_data.get("source"),
                    placement_date=final_data.get("placement_date"),
                    completion_date=final_data.get("completion_date"),
                    drawn_date=final_data.get("drawn_date"),
                    total_ul_wt=final_data.get("total_ul_wt"),
                    boxes_supplied=final_data.get("boxes_supplied"),
                    total_secl_gross_wt=final_data.get("total_secl_gross_wt"),
                    total_secl_tare_wt=final_data.get("total_secl_tare_wt"),
                    total_secl_net_wt=final_data.get("total_secl_net_wt"),
                    total_secl_ol_wt=final_data.get("total_secl_ol_wt"),
                    boxes_loaded=final_data.get("boxes_loaded"),
                    total_rly_gross_wt=final_data.get("total_rly_gross_wt"),
                    total_rly_tare_wt=final_data.get("total_rly_tare_wt"),
                    total_rly_net_wt=final_data.get("total_rly_net_wt"),
                    total_rly_ol_wt=final_data.get("total_rly_ol_wt"),
                    total_secl_chargable_wt=final_data.get("total_secl_chargable_wt"),
                    total_rly_chargable_wt=final_data.get("total_rly_chargable_wt"),
                    freight=final_data.get("freight"),
                    gst=final_data.get("gst"),
                    pola=final_data.get("pola") if final_data.get("pola") != "Not found" else "",
                    sd=final_data.get("sd") if final_data.get("sd") != "Not found" else "",
                    total_freight=final_data.get("total_freight"),
                    source_type=final_data.get("source_type"),
                    month = final_data.get("month"),    # modified by faisal
                    # month=datetime.datetime.strptime(fetchSaprecordsRail.month, '%b %d, %Y').strftime('%Y-%m-%d') if fetchSaprecordsRail and fetchSaprecordsRail.month else "",
                    secl_rly_data=secl_list_data,
                    avery_rly_data=avery_list_data,
                    rr_date=fetchSaprecordsRail.rr_date if fetchSaprecordsRail and fetchSaprecordsRail.rr_date else None,
                    siding=fetchSaprecordsRail.siding if fetchSaprecordsRail and fetchSaprecordsRail.siding else "",
                    mine=fetchSaprecordsRail.mine if fetchSaprecordsRail and fetchSaprecordsRail.mine else "",
                    grade=fetchSaprecordsRail.grade if fetchSaprecordsRail and fetchSaprecordsRail.grade else "",
                    # rr_qty=fetchSaprecordsRail.get("rr_qty") if fetchSaprecordsRail.get("rr_qty") else "",
                    po_amount=fetchSaprecordsRail.po_amount if fetchSaprecordsRail and fetchSaprecordsRail.po_amount else 0,
                ) 
                existing_rake_nos = [data.rake_no for data in RailData.objects()]
                if final_data.get("placement_date") and fetchSaprecordsRail and fetchSaprecordsRail.month:
                    placement_date_obj = datetime.datetime.strptime(final_data.get("placement_date"), '%Y-%m-%dT%H:%M')
                    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fetchSaprecordsRail.month):
                        rail_data.rake_no = self.calculate_rake_no(datetime.datetime.strptime(fetchSaprecordsRail.month, '%Y-%m-%d').strftime('%Y-%m-%d'),
                                                        placement_date_obj.strftime('%Y-%m-%d'),
                                                        existing_rake_nos)
                    else:
                        rail_data.rake_no = self.calculate_rake_no(datetime.datetime.strptime(fetchSaprecordsRail.month, '%b %d, %Y').strftime('%Y-%m-%d'),
                                                        placement_date_obj.strftime('%Y-%m-%d'),
                                                        existing_rake_nos)
                rail_data.save()
                return {"message": "Data inserted successfully"}

        except Exception as e:
            helpers.error_handler(e)            
    
    
    def coal_journey_avery_data_update( self,data,rr_no, placement_date, completion_date, GWEL_received_wagons, GWEL_pending_wagons, Total_gwel_gross, Total_gwel_tare, Total_gwel_net, Total_no_of_boxes_supplied, Total_no_of_boxes_loaded, source, source_type):
        try:
            payload = data.dict()
            try:
                fetchRailData = RailData.objects.get(rr_no=rr_no)
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RailData")
            fetchRailData.avery_placement_date = placement_date
            fetchRailData.avery_completion_date = completion_date
            fetchRailData.GWEL_received_wagons = GWEL_received_wagons
            fetchRailData.GWEL_pending_wagons = GWEL_pending_wagons
            fetchRailData.Total_gwel_gross = Total_gwel_gross
            fetchRailData.Total_gwel_tare = Total_gwel_tare
            fetchRailData.Total_gwel_net = Total_gwel_net
            fetchRailData.boxes_loaded = Total_no_of_boxes_loaded
            fetchRailData.boxes_supplied = Total_no_of_boxes_supplied
            fetchRailData.source = source
            fetchRailData.source_type = source_type
            if payload.get("data"):
                avery_user_data_instances = [AveryRailData(**item) for item in payload.get("data")]
                fetchRailData.avery_rly_data = avery_user_data_instances
            else:
                fetchRailData.avery_rly_data.clear()

            fetchRailData.save()
            
            return {"details": "success"}
        except Exception as e:
            helpers.error_handler(e) 
            raise e
            
coal_journey_rail = CoalJourneyDashboard()