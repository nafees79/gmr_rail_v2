import datetime
from mongoengine import Q
from dateutil.relativedelta import relativedelta
from api import short_mine_collection
from api.service.helpers import helpers
import calendar
from datetime import timedelta
from fastapi import HTTPException
from bson.objectid import ObjectId
from api.service.models import (
                            RailData, 
                            rcrrakeQuota, 
                            RcrData, 
                            sapRecordsRCR,
                            RcrRoadData,
                            SeclRailData,
                            AveryRailData
                        )

class RcrRoadAndRail:
    
    def __init__(self):
        pass
    
    def convert_to_date(self,month_str):
        try:
            return datetime.datetime.strptime(month_str, "%b-%Y")
        except Exception as e:
            helpers.error_handler(e)

    def convert_to_float(self, value, field_name):
        """Helper function to handle conversion and error logging."""
        try:
            return float(value)
        except (ValueError, TypeError):
            # print(f"Warning: Invalid data for {field_name}: {value}")
            return 0.0
        
    def search_text(self, pending_query, completed_query, search_text):
        if search_text.isdigit():
            query_filter = Q(rr_no__icontains=search_text)
        else:
            query_filter = (Q(mine__icontains=search_text))

        pending_query &= query_filter
        completed_query &= query_filter

        return pending_query, completed_query
    
    def coal_journey_rcr_road(self,currentPage,perPage,search_text,start_timestamp,end_timestamp,month_date):
        try:
            result = {        
                    "labels": [],
                    "records": [],
                    "count" : 0,
                    "page_size": perPage or 15,
                    "page_no": currentPage or 1
            }
            page_no = currentPage or 1
            page_len = result["page_size"]
            offset = (page_no - 1) * page_len
            
            data = Q()

            if search_text:
                if search_text.isdigit():
                    data &= Q(do_number__icontains=search_text)
                else:
                    data &= (Q(mine__icontains=search_text))
            
            try:
                if start_timestamp:
                    start_date = helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M")
                    data &= Q(tar_wt_date__gte = start_date)
                
                if end_timestamp:
                    end_date = helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M","Asia/Kolkata",False)
                    data &= Q(tar_wt_date__lte = end_date)                     
                        
                if month_date:
                        start_date = f'{month_date}-01'
                        startd_date=datetime.datetime.strptime(f"{start_date}T00:00","%Y-%m-%dT%H:%M")
                        end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(day=31)).strftime("%Y-%m-%d")
                        data &= Q(tar_wt_date__gte = startd_date.strftime("%Y-%m-%dT%H:%M"))
                        data &= Q(tar_wt_date__lte = f"{end_date}T23:59")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
            
            try:
                logs = (
                    RcrRoadData.objects(data) 
                    .order_by("-created_at")
                    .skip(offset)
                    .limit(page_len)
                    )
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RcrRoadData")
               
            if logs:
                for log in logs:
                    result["labels"] = list(log.payload().keys())
                    result["records"].append(log.payload())
            
            result["count"] = RcrRoadData.objects(data).count()
            
            return result
        
        except Exception as e:
            helpers.error_handler(e)
            raise e

    def coal_journey_rcr_rail_pending(self, pageNo, perPage, search_text, start_timestamp, end_timestamp, month):
        try:
            result = {        
                "labels": [],
                "datasets": [],
                "count": {
                    "pending": 0,
                    "completed": 0
                },
                "page_no": pageNo or 1,
                "page_size":perPage or 15,
            }

            page_no = pageNo or 1
            page_len = result["page_size"]
            offset = (page_no - 1) * page_len

            pending_data = Q(avery_placement_date = None)
            completed_data = Q(avery_placement_date__ne = None)

            if search_text:
                pending_data, completed_data = self.search_text(pending_data, completed_data, search_text)
            
            try:
                if start_timestamp:
                    start_date = helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M")
                    pending_data &= Q(placement_date__gte = start_date)

                if end_timestamp:
                    end_date = helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M","Asia/Kolkata",False)
                    pending_data &= Q(placement_date__lte = end_date)

                if month:
                    start_date = f'{month}-01'
                    startd_date=datetime.datetime.strptime(f"{start_date}T00:00","%Y-%m-%dT%H:%M")
                    end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(day=31)).strftime("%Y-%m-%d")
                    # endd_date= f"{end_date}T23:59"
                    pending_data &= Q(placement_date__gte = startd_date.strftime("%Y-%m-%dT%H:%M"))
                    pending_data &= Q(placement_date__lte = f"{end_date}T23:59")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
            
            try:
                logs = (RcrData.objects(pending_data).order_by("-created_at").skip(offset).limit(page_len))
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RcrData")
            
            if any(logs):
                for log in logs:
                    result["labels"] = list(log.payload().keys())
                    result["datasets"].append(log.simplepayload())

            result["count"]["pending"] = RcrData.objects(pending_data).count()
            result["count"]["completed"] = RcrData.objects(completed_data).count()
                
            return result
            
        except Exception as e:
            helpers.error_handler(e)
            raise e


    def coal_journey_rcr_rail_completed(self, currentPage, perPage, search_text, start_timestamp, end_timestamp, month):
        try:
            result = {        
                "labels": [],
                "datasets": [],
                "count": {
                    "pending": 0,
                    "completed": 0
                },
                "page_no": currentPage or 1,
                "page_size": perPage or 15,
                    
            }
            page_no =currentPage or  1
            page_len = result["page_size"]
            offset = (page_no - 1) * page_len

            pending_data = Q(avery_placement_date = None)
            completed_data = Q(avery_placement_date__ne = None)

            if search_text:
                pending_data, completed_data = self.search_text(pending_data, completed_data, search_text)
 
            try:
                if start_timestamp:
                    # start_date = helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M")
                    completed_data &= Q(avery_placement_date__gte = start_timestamp)

                if end_timestamp:
                    # end_date = helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M","Asia/Kolkata",False)
                    completed_data &= Q(avery_placement_date__lte = end_timestamp)

                if month:
                    start_date = f'{month}-01'
                    startd_date=datetime.datetime.strptime(f"{start_date}T00:00","%Y-%m-%dT%H:%M")
                    end_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(day=31)).strftime("%Y-%m-%d")
                    completed_data &= Q(avery_placement_date__gte = startd_date.strftime("%Y-%m-%dT%H:%M"))
                    completed_data &= Q(avery_placement_date__lte = f"{end_date}T23:59")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
            
            try:
                logs = (RcrData.objects(completed_data).order_by("-avery_placement_date", "-avery_completion_date").skip(offset).limit(page_len))
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing RcrData")
            
            if any(logs):
                for log in logs:
                    payload = log.averyPayloadMain()

                    fields = [
                        'secl_mode_transport', 'area', 'secl_basic_price', 'secl_sizing_charges', 'secl_stc_charges',
                        'secl_evac_facility_charges', 'secl_nmet_charges', 'secl_dmf', 'secl_adho_sanrachna_vikas',
                        'secl_pariyavaran_upkar', 'secl_terminal_tax', 'secl_assessable_tax', 'secl_igst', 
                        'secl_gst_comp_cess', 'sap_po'
                    ]

                    default_values = {
                        'secl_mode_transport': 0, 'area': 0, 'secl_basic_price': 0, 'secl_sizing_charges': 0,
                        'secl_stc_charges': 0, 'secl_evac_facility_charges': 0, 'secl_nmet_charges': 0, 'secl_dmf': 0,
                        'secl_adho_sanrachna_vikas': 0, 'secl_pariyavaran_upkar': 0, 'secl_terminal_tax': 0,
                        'secl_assessable_tax': 0, 'secl_igst': 0, 'secl_gst_comp_cess': 0, 'sap_po': 0
                    }

                    try:
                        fetchSapRcrRecords = sapRecordsRCR.objects.get(rr_no=log.rr_no)
                        for field in fields:
                            value = getattr(fetchSapRcrRecords, field, default_values[field])
                            payload[field] = value
                    except Exception as e:
                        for field in fields:
                            payload[field] = default_values[field]

                    if log.avery_rly_data:
                        total_wagon_gross_wt = 0
                        total_wagon_tare_wt = 0
                        total_wagon_net_wt = 0
                        
                        for singleRailData in log.avery_rly_data:
                            total_wagon_gross_wt += self.convert_to_float(singleRailData.gwel_gross_wt, "gwel_gross_wt")
                            total_wagon_tare_wt += self.convert_to_float(singleRailData.gwel_tare_wt, "gwel_tare_wt")
                            total_wagon_net_wt += self.convert_to_float(singleRailData.gwel_net_wt, "gwel_net_wt")
                        
                        payload['total_gwel_gross_wt'] = round(total_wagon_gross_wt, 2)
                        payload['total_gwel_tare_wt'] = round(total_wagon_tare_wt, 2)
                        payload['total_gwel_net_wt'] = round(total_wagon_net_wt, 2)


                    result["labels"] = list(log.payload().keys())
                    result["datasets"].append(payload)
                    result["count"]["pending"] = RcrData.objects(pending_data).count()
                    result["count"]["completed"] = RcrData.objects(completed_data).count()
            return result
        
        except Exception as e:
            helpers.error_handler(e)
            raise e


    def coal_journey_rcr_rail_allminenames(self):
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
        

    def coal_journey_rcr_rail_singlercr(self, rrno):
        try:
            fetchRailData = RcrData.objects.get(rr_no=rrno)
            return fetchRailData.payload()
        
        except Exception as e:
            helpers.error_handler(e)

    
    def coal_journey_rcr_rail_singlercravery(self, rrno):
        """
        Function that fetches single rcravery data using rrno
        Parameters:
            rr_no

        Returns:
            single dictionary data for particular rr_no
        """
        try:
            fetchRcrData = RcrData.objects.get(rr_no=rrno)
            return fetchRcrData.payload()
        
        except Exception as e:
            helpers.error_handler(e)

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
        
    def coal_journey_rcr_rail_insert(self,payload, id):
        try:
            final_data = payload.dict()
            try:
                if id:
                    fetchRailData = RcrData.objects.get(id=ObjectId(id))
                else:
                    fetchRailData = RcrData.objects.get(rr_no=final_data.get("rr_no"))
                try:
                    fetchSaprecordsRail = sapRecordsRCR.objects.get(rr_no=final_data.get("rr_no"))
                except Exception as e:
                    fetchSaprecordsRail = None
                
                if fetchSaprecordsRail:
                    if fetchSaprecordsRail.month:
                        fetchRailData.month = datetime.datetime.strptime(fetchSaprecordsRail.month, '%b %d, %Y').strftime('%Y-%m-%d')
                    fetchRailData.rr_date = fetchSaprecordsRail.rr_date
                    fetchRailData.area = fetchSaprecordsRail.area
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
                fetchRailData.GWEL_pending_wagons = final_data.get("GWEL_pending_wagons")
                fetchRailData.GWEL_received_wagons = final_data.get("GWEL_received_wagons")
                fetchRailData.total_gwel_gross_wt = final_data.get("total_gwel_gross_wt")
                fetchRailData.total_gwel_net_wt = final_data.get("total_gwel_net_wt")
                fetchRailData.total_gwel_tare_wt = final_data.get("total_gwel_tare_wt")
                fetchRailData.avery_completion_date = final_data.get("avery_completion_date")
                fetchRailData.avery_placement_date = final_data.get("avery_placement_date")
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
                # changed on 13012025 for update 12:36
                fetchRailData.month = final_data.get("month")
                
                for key, value in final_data.items():
                    if key != 'secl_rly_data' and hasattr(fetchRailData, key):
                        setattr(fetchRailData, key, value)

                # if fetchRailData.placement_date:
                #     # Set rake_no based on month and placement_date
                #     fetchRailData.rake_no = calculate_rake_no(datetime.datetime.strptime(fetchSaprecordsRail.month, '%b %d, %Y').strftime('%Y-%m-%d'), fetchRailData.placement_date.strftime('%Y-%m-%d'))

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
                listAveryData = []
                # for new_data in final_data.get('secl_rly_data', []):
                if final_data.get('avery_rly_data'):
                    for new_data in final_data.get('avery_rly_data', []):
                        # console_logger.debug(new_data)
                        dictAveryData = {}
                        dictAveryData["indexing"] = new_data.get("indexing")
                        dictAveryData["wagon_owner"] = new_data.get("wagon_owner")
                        dictAveryData["wagon_type"] = new_data.get("wagon_type")
                        dictAveryData["wagon_no"] = new_data.get("wagon_no")
                        dictAveryData["gwel_gross_wt"] = new_data.get("gwel_gross_wt")
                        dictAveryData["gwel_tare_wt"] = new_data.get("gwel_tare_wt")
                        dictAveryData["gwel_net_wt"] = new_data.get("gwel_net_wt")
                        dictAveryData["coal_grade"] = new_data.get("coal_grade")
                        dictAveryData["mode"] = new_data.get("mode")
                        dictAveryData["po_number"] = new_data.get("po_number")
                        dictAveryData["rake_id"] = new_data.get("rake_id")
                        dictAveryData["rake_no"] = new_data.get("rake_no")
                        dictAveryData["ser_no"] = new_data.get("ser_no")
                        dictAveryData["status"] = new_data.get("status")
                        dictAveryData["time_in_tipp"] = new_data.get("time_in_tipp")
                        dictAveryData["tip_enddate"] = new_data.get("tip_enddate")
                        dictAveryData["tip_endtime"] = new_data.get("tip_endtime")
                        dictAveryData["tip_startdate"] = new_data.get("tip_startdate")
                        dictAveryData["tip_starttime"] = new_data.get("tip_starttime")
                        dictAveryData["tipple_time"] = new_data.get("tipple_time")
                        dictAveryData["wagon_cc"] = new_data.get("wagon_cc")
                        dictAveryData["wagon_id"] = new_data.get("wagon_id")
                        dictAveryData["wagon_no_avery"] = new_data.get("wagon_no_avery")
                        dictAveryData["wagon_type_avery"] = new_data.get("wagon_type_avery")
                        dictAveryData["data_from"] = new_data.get("data_from")
                        listAveryData.append(AveryRailData(**dictAveryData))
            
                fetchRailData.avery_rly_data = listAveryData
                fetchRailData.save()

                return {"detail": "success"}
            except Exception as e:
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
                    fetchSaprecordsRail = sapRecordsRCR.objects.get(rr_no=final_data.get("rr_no"))
                except Exception as e:
                    fetchSaprecordsRail = None

                rail_data = RcrData(
                    rr_no=final_data.get("rr_no"),
                    # rr_qty=final_data.get("rr_qty"),
                    rr_qty=fetchSaprecordsRail.rr_qty if fetchSaprecordsRail and fetchSaprecordsRail.rr_qty else "",
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
                    rr_date=fetchSaprecordsRail.rr_date if fetchSaprecordsRail and fetchSaprecordsRail.rr_date else "",
                    # siding=fetchSaprecordsRail.siding if fetchSaprecordsRail and fetchSaprecordsRail.siding else "",
                    mine=fetchSaprecordsRail.mine if fetchSaprecordsRail and fetchSaprecordsRail.mine else "",
                    grade=fetchSaprecordsRail.grade if fetchSaprecordsRail and fetchSaprecordsRail.grade else "",
                    # rr_qty=fetchSaprecordsRail.get("rr_qty") if fetchSaprecordsRail.get("rr_qty") else "",
                    po_amount=fetchSaprecordsRail.po_amount if fetchSaprecordsRail and fetchSaprecordsRail.po_amount else "",
                ) 
                existing_rake_nos = [data.rake_no for data in RailData.objects()]

                if final_data.get("placement_date") and fetchSaprecordsRail and fetchSaprecordsRail.month:
                    placement_date_obj = datetime.datetime.strptime(final_data.get("placement_date"), '%Y-%m-%dT%H:%M')
                    rail_data.rake_no = self.calculate_rake_no(datetime.datetime.strptime(fetchSaprecordsRail.month, '%b %d, %Y').strftime('%Y-%m-%d'),
                                                        placement_date_obj.strftime('%Y-%m-%d'),
                                                        existing_rake_nos)
                rail_data.save()
                return {"message": "Data inserted successfully"}

        except Exception as e:
            helpers.error_handler(e)

coal_journey_rcr_all=RcrRoadAndRail()