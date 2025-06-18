from fastapi import APIRouter, Query
from typing import Optional
from api.rail_operations.logistics_movements.coal_journey.rail import coal_journey_rail
from api.rail_operations.logistics_movements.coal_journey.rail_rake_quota import coal_journey_rail_rake_quota
from api.rail_operations.logistics_movements.coal_journey.rcr_road_and_rail import coal_journey_rcr_all
from api.rail_operations.logistics_movements.coal_journey.rcr_rake_quota import coal_jouney_rcr_rake_quota

from api.service.serializers import rakeQuotaUpdate,RailwayData,mainAveryData

router = APIRouter()

#Logistic Movements -> Coal Journey - Rail -> Rail Coal Journey Table  Pending

@router.get("/coal_journey/rail_pending", tags=["Logistic Movements - Coal Journey Rail V2"]) 
def endpoint_for_coal_journey_rail_pending(
                                        currentPage: Optional[int] = None, 
                                        perPage: Optional[int] = None,                                                            
                                        search_text: Optional[str] =Query(None,description="RR No. / Po No. / Source"),
                                        start_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT00:00"),
                                        end_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT23:59"),
                                        month_date: Optional[str] = Query(None,description="YYYY-MM"), 
                                ):
        """
        **Fetches Coal Journey Rail data from the RailData and sapRecordsRail collection.**
        
        ---
        ### 🔍 Parameters:

        - **currentPage** : Page number for pagination.

        - **perpage** : No. of data on Current Page.
         
        - **search_text** : Search for data using `RR No. / Po No / Source`.

        - **start_timestamp** : Start datetime of Placement Date e.g. `2024-01-01T00:00`

        - **end_timestamp** : End datetime of Placement Date e.g. `2025-01-01T23:59`

        - **month_date** : Filter by a single month of Placement Date  e.g.- `2025-01`

        ---
        ### 📦Returns:
        - **Set of data with counts.**
        """

        return coal_journey_rail.coal_journey_rail_pending(currentPage, perPage, search_text, start_timestamp, end_timestamp, month_date)



# Logistic Movements -> Coal Journey-Rail -> Rail Coal Journey Table  Completed

@router.get("/coal_journey/rail_completed", tags=["Logistic Movements - Coal Journey Rail V2"])
def endpoint_for_coal_journey_rail_completed(
                                        currentPage: Optional[int] = None, 
                                        perPage: Optional[int] = None,                                                            
                                        search_text: Optional[str] =Query(None,description="RR No. / Po No. / Source"),
                                        start_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT00:00"),
                                        end_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT23:59"),
                                        month_date: Optional[str] = Query(None,description="YYYY-MM"),
                                ):
        """
        **Fetches Coal Journey Rail data from the RailData and sapRecordsRail collection.**
        
        ---
        ### 🔍 Parameters:

        - **currentPage** : Page number for pagination.
 
        - **perpage** : No. of data on Current Page.
         
        - **search_text** : Search for data using `RR No. / Po No / Source`.

        - **start_timestamp** : Start datetime of Placement Date e.g. `2024-01-01T00:00`

        - **end_timestamp** : End datetime of Placement Date e.g. `2025-01-01T23:59`

        - **month_date** : Filter by a single month of Placement Date  e.g.- `2025-01`

        ---
        ### 📦 Returns:
        - **Set of data with counts.**
        """
        
        return coal_journey_rail.coal_journey_rail_completed(currentPage, perPage, search_text, start_timestamp, end_timestamp, month_date)


# Logistic Movements -> Coal Journey -> Rail -> Rail Coal Journey Table -> Form Pending and Completed 
@router.get("/coal_journey/rail/fetch_allminenames", tags=["Logistic Movements - Coal Journey Rail V2"])
def endpoint_for_coal_journey_rail_allminenames():

        return coal_journey_rail.coal_journey_rail_allminenames()


# Logistic Movements -> Coal Journey -> Rail -> Rail Coal Journey Table -> Form Pending 
@router.get("/coal_journey/rail/fetch_singlerail", tags=["Logistic Movements - Coal Journey Rail V2"])
async def endpoint_for_coal_journey_rail_singlerail(
                                        rr_no: str
                                ):
        
        return await coal_journey_rail.coal_journey_rail_singlerail(rr_no)


# Logistic Movements -> Coal Journey -> Rail -> Rail Coal Journey Table -> Form Pending and Completed 
@router.get("/coal_journey/rail/mine_shortcode_sourcetype", tags=["Logistic Movements - Coal Journey Rail V2"])
def endpoint_for_coal_journey_rail_mine_shortcodes_sourcetype():

        return coal_journey_rail.coal_journey_rail_mine_shortcodes_sourcetype()


# Logistic Movements -> Coal Journey -> Rail -> Rail Coal Journey Table -> Form Pending
@router.post("/coal_journey/rail/insert", tags=["Logistic Movements - Coal Journey Rail V2"])
def endpoint_for_coal_journey_rail_insert(
                                payload: RailwayData, 
                                id: Optional[str] = None
                        ):
        
        return coal_journey_rail.coal_journey_rail_insert(payload, id)


# Logistic Movements -> Coal Journey -> Rail -> Rail Coal Journey Table -> Form Completed
@router.get("/coal_journey/avery/singlerail", tags=["Logistic Movements - Coal Journey Rail V2"])
def endpoint_for_coal_journey_avery_singlerail(
                                        rr_no: str
                                ):
        
        return coal_journey_rail.coal_journey_avery_singlerail(rr_no)


# Logistic Movements -> Coal Journey -> Rail -> Rail Coal Journey Table -> Form Completed
@router.post("/coal_journey/avery_data/update", tags=["Logistic Movements - Coal Journey Rail V2"])
def endpoint_for_coal_journey_avery_data_update( 
                                        data: mainAveryData, 
                                        rr_no: int, 
                                        placement_date: str, 
                                        completion_date: str, 
                                        GWEL_received_wagons: str,
                                        GWEL_pending_wagons: str, 
                                        Total_gwel_gross: str, 
                                        Total_gwel_tare: str, 
                                        Total_gwel_net: str, 
                                        Total_no_of_boxes_supplied: str, 
                                        Total_no_of_boxes_loaded: str, 
                                        source: str, 
                                        source_type: str
                                ):
        
        return coal_journey_rail.coal_journey_avery_data_update(data,rr_no,placement_date,completion_date,GWEL_received_wagons,GWEL_pending_wagons,Total_gwel_gross,Total_gwel_tare,Total_gwel_net,Total_no_of_boxes_supplied,Total_no_of_boxes_loaded,source,source_type)




#--------------------------------------------------------------------------------------------------------------------------------


# Logistic Movements -> Coal Journey -> Rail -> Rake Quota Table -> Pending
@router.get("/coal_journey/rail_rake_quota_pending", tags=["Logistic Movements - Coal Journey Rail Rake V2"])
def endpoint_for_coal_journey_rail_rake_quota_pending(
                                                currentPage: Optional[int] = None,
                                                perPage: Optional[int] = None,
                                                # search_text: Optional[str] = None,
                                                # month_date: Optional[str] = None,
                                                start_timestamp: Optional[str] = None,
                                                end_timestamp: Optional[str] = None,
                                        ):
        
        """
        **Fetches Coal Journey Rail Rake Quota data from the rakeQuota and RailData collection.**
        
        ---
        ### 🔍 Parameters:

        - **currentPage** : Page number for pagination.

        - **perpage** : No. of data on Current Page.

        - **start_timestamp** : Start datetime of Created At e.g. `2024-01-01T00:00`

        - **end_timestamp** : End datetime of Created At e.g. `2025-01-01T23:59`

        ---
        ### 📦 Returns:
        - **Set of data with counts.**
        """
        
        return coal_journey_rail_rake_quota.coal_journey_rail_rake_quota_pending(currentPage,perPage,start_timestamp,end_timestamp)
  

# Logistic Movements -> Coal Journey -> Rail -> Rake Quota Table -> Completed
@router.get("/coal_journey/rail_rake_quota_completed", tags=["Logistic Movements - Coal Journey Rail Rake V2"])
def endpoint_for_coal_journey_rail_rake_quota_completed(
                                                currentPage: Optional[int] = None,
                                                perPage: Optional[int] = None,
                                                # search_text: Optional[str] = None,
                                                # month_date: Optional[str] = None,
                                                start_timestamp: Optional[str] = None,
                                                end_timestamp: Optional[str] = None,
                                        ):
        
        """
        **Fetches Coal Journey Rail Rake Quota data from the rakeQuota and RailData collection.**
        
        ---
        ### 🔍 Parameters:

        - **currentPage** : Page number for pagination.

        - **perpage** : No. of data on Current Page.

        - **start_timestamp** : Start datetime of Created At e.g. `2024-01-01T00:00`

        - **end_timestamp** : End datetime of Created At e.g. `2025-01-01T23:59`

        ---
        ### 📦 Returns:
        - **Set of data with counts.**
        """
        
        return coal_journey_rail_rake_quota.coal_journey_rail_rake_quota_completed(currentPage, perPage, start_timestamp, end_timestamp)


# Logistic Movements -> Coal Journey -> Rail -> Rake Quota Table -> Form Pending and Completed
@router.post("/coal_journey/rail_rake_quota_update", tags=["Logistic Movements - Coal Journey Rail Rake V2"])
def endpoint_to_coal_journey_rail_rake_quota_update(
                                                data : rakeQuotaUpdate
                                        ):
        """
        **Fetches Coal Journey Rail Rake Quota data from the rakeQuota collection.**
        
        ---
        ### 🔍 Parameters:

        - **data** : Update the data

        ---
        ### 📦 Returns:
        - **success : If data updated successfully.**
        """
   
        return coal_journey_rail_rake_quota.coal_journey_rail_rake_quota_update(data)


#--------------------------------------------------------------------------------------------------------------------------------


#Logistic Movements -> Coal Journey - RCR -> RCR Road Journey Table 
 
@router.get("/coal_journey/rcr_road", tags=["Logistic Movements - Coal Journey RCR Road V2"]) 
def endpoint_for_coal_journey_rcr_road( 
                                        currentPage: Optional[int] = None, 
                                        perPage: Optional[int] = None,                                                            
                                        search_text: Optional[str] = Query(None,description="Do No. / Mine"),
                                        start_timestamp: Optional[str] = Query(None,description="YYYY-MM-ddTHH:MM"), 
                                        end_timestamp: Optional[str] = Query(None,description="YYYY-MM-ddTHH:MM"), 
                                        month_date: Optional[str] =  Query(None,description="YYYY-MM"), 
                                      ):
        """
        **Fetches Coal Journey RCR data from the RcrRoadData collection.**

        ---
        ### 🔍 Parameters:

        - **currentPage** : Page number for pagination.
        
        - **perpage** : No. of data on Current Page.
         
        - **search_text** : Search for data using `Do No. / Mine`.

        - **start_timestamp** : Start datetime of Tar Wt Date  e.g.`2024-01-01T00:00`

        - **end_timestamp** : End datetime of Tar Wt Date e.g.-`2025-01-01T23:59`

        - **month_date** : Filter by a single month of Tar Wt Date e.g. `2025-01`

        ---
        ### 📦 Returns:
        - **Set of data with counts.**
        """

        return coal_journey_rcr_all.coal_journey_rcr_road(currentPage, perPage, search_text, start_timestamp, end_timestamp, month_date) 
 

#Logistic Movements -> Coal Journey -> RCR Rail Journey Table Pending

@router.get("/coal_journey/rcr_rail_pending", tags=["Logistic Movements - Coal Journey RCR Rail V2"])
def endpoint_for_coal_journey_rcr_rail_pending(
                                        currentPage: Optional[int] = None,
                                        perPage: Optional[int] = None, 
                                        search_text: Optional[str] = Query(None , description="RR No. / Mine"), 
                                        start_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT00:00"), 
                                        end_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT00:00"), 
                                        # month: Optional[str] = Query(None,description="YYYY-MM"),
                                ):
        
        """
        **Fetches Coal Journey SAP RCR data from RcrData Collection.**

        ---
        ### 🔍 Parameters:

        - **currentPage** : Page Number for pagination.

        - **perPage** :  No. of data on Current Page.
        
        - **search_text** :  Search for data using - `RR No. / Mine`.
        
        - **start_timestamp** : Start datetime of Placement Date Eg: `2024-02-01T00:00`.
        
        - **end_timestamp**  : End datetime of Placement Date Eg: `2025-02-01T23:59`.

        - **month** :  Month of Placement Date Eg: `2025-02`.
        
        ---
        ### 📦 Returns:
        - **Set of data with counts**
        """
        
        return coal_journey_rcr_all.coal_journey_rcr_rail_pending(currentPage, perPage, search_text, start_timestamp, end_timestamp)


#Logistic Movements -> Coal Journey -> RCR -> GWEL RCR Rail Journey Table Completed

@router.get("/coal_journey/rcr_rail_completed", tags=["Logistic Movements - Coal Journey RCR Rail V2"])
def endpoint_for_coal_journey_rcr_rail_completed(
                                        currentPage: Optional[int] = None,
                                        perPage: Optional[int] = None,
                                        search_text: Optional[str] = Query(None , description="RR No. / PO No. / Source"),
                                        start_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT00:00"),
                                        end_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT23:59"),
                                        # month: Optional[str] = Query(None,description="YYYY-MM"),
                                ):
        """
        **Fetches Coal Journey RCR data from RcrData and sapRecordsRCR Collection.**

        ---
        ### 🔍 Parameters:

        - **currentPage** : Page Number for pagination.

        - **perPage** :  No. of data on Current Page.
        
        - **search_text** :  Search for data using - `RR No. / PO No. / Source`.
        
        - **start_timestamp** : Start datetime of Avery Placement Eg: `2024-02-01T00:00`.
        
        - **end_timestamp**  : End datetime of Avery Placement Eg: `2025-02-01T23:59`.

        - **month** :  Month of Avery Placement Eg: `2025-02`.
        
        ---
        ### 📦 Returns:
        - **Set of data with counts**
        """
        return coal_journey_rcr_all.coal_journey_rcr_rail_completed(currentPage, perPage, search_text, start_timestamp, end_timestamp)


# Logistic Movements -> Coal Journey -> RCR -> Rail Journey Table Form Pending and Completed
@router.get("/coal_journey/rcr_rail/fetch_allminenames", tags=["Logistic Movements - Coal Journey RCR Rail V2"])
def endpoint_for_coal_journey_rcr_rail_allminenames():

        return coal_journey_rcr_all.coal_journey_rcr_rail_allminenames()


# Logistic Movements -> Coal Journey -> RCR -> Rail Journey Table Form Pending
@router.get("/coal_journey/rcr_rail/fetch_singlercr", tags=["Logistic Movements - Coal Journey RCR Rail V2"])
def endpoint_for_coal_journey_rcr_rail_singlercr(
                                rr_no: str
                        ):
        
        return coal_journey_rcr_all.coal_journey_rcr_rail_singlercr(rr_no)


# Logistic Movements -> Coal Journey -> RCR -> Rail Journey Table Form Completed
@router.get("/coal_journey/rcr_rail/fetch_singlercravery", tags=["Logistic Movements - Coal Journey RCR Rail V2"])
def endpoint_for_coal_journey_rcr_rail_singlercravery(
                                                rr_no: str
                                        ):
        
        return coal_journey_rcr_all.coal_journey_rcr_rail_singlercravery(rr_no)


# Logistic Movements -> Coal Journey - RCR -> Rail Journey Table -> Form Pending and Completed
@router.post("/coal_journey/rcr_rail/insert", tags=["Logistic Movements - Coal Journey RCR Rail V2"])
def endpoint_for_coal_journey_rcr_rail_insert(
                                        payload: RailwayData, 
                                        id: Optional[str] = None
                                ):
            
        return coal_journey_rcr_all.coal_journey_rcr_rail_insert(payload,id)


#--------------------------------------------------------------------------------------------------------------------------------

#Logistic Movements -> Coal Journey -> RCR Rake Quota Table  Pending
@router.get("/coal_journey/rcr_rake_quota_pending", tags=["Logistic Movements - Coal Journey RCR Rake V2"])
def endpoint_for_coal_journey_rcr_rake_quota_pending(
                                        currentPage: Optional[int] = None,
                                        perPage: Optional[int] = None,
                                        # search_text: Optional[str] = None,
                                        # month_date: Optional[str] = None,
                                        start_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT00:00"),
                                        end_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDT23:59"),
                                 ):
        """
        **Fetches Bunker Quality Analysis table data from rcrrakeQuota, RcrData and RailData collection.**

        ---
        ### 🔍 Parameters:

        - **currentPage** : Page number for pagination.
        
        - **perpage** : No. of data on Current Page.

        - **start_timestamp** : Start datetime of Created At e.g.-`2024-01-01T00:00`

        - **end_timestamp** : End datetime of Created At e.g.- `2025-01-01T23:59`

        ---
        ### 📦 Returns:
        - **Set of data with counts.**
        """
        return coal_jouney_rcr_rake_quota.coal_journey_rcr_rake_quota_pending(currentPage,perPage,start_timestamp,end_timestamp)


#Logistic Movements -> Coal Journey -> RCR Rake Quota Table  Completed
@router.get("/coal_journey/rcr_rake_quota_completed", tags=["Logistic Movements - Coal Journey RCR Rake V2"])
def endpoint_for_coal_journey_rcr_rake_quota_completed(
                                                currentPage: Optional[int] = None,
                                                perPage: Optional[int] = None,
                                                start_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDTHH:MM"), 
                                                end_timestamp: Optional[str] = Query(None,description="YYYY-MM-DDTHH:MM"), 
                                        ):
        """
        **Fetches Bunker Quality Analysis table data from rcrrakeQuota, RcrData and RailData collection.**

        ---
        ### 🔍 Parameters:
        - **currentPage** : Page number for pagination.
        
        - **perpage** : No. of data on Current Page.

        - **start_timestamp** : Start datetime of Created At e.g.- `2024-01-11T00:00`

        - **end_timestamp** : End datetime of Created At e.g.- `2025-01-11T23:59`

        ---
        ### 📦 Returns:
        - **Set of data with counts.**
        """
        return coal_jouney_rcr_rake_quota.coal_journey_rcr_rake_quota_completed(currentPage,perPage,start_timestamp,end_timestamp)
     

#Logistic Movements -> Coal Journey -> RCR Rake Quota Table  Update
@router.post("/coal_journey/rcr_rake_quota/update", tags=["Logistic Movements - Coal Journey RCR Rake V2"])
def endpoint_for_coal_journey_rcr_rake_quota_update(
                                data : rakeQuotaUpdate
                        ):

        return coal_jouney_rcr_rake_quota.coal_journey_rcr_rake_quota_update(data)


