from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List
from datetime import datetime

class rakeQuotaUpdate(BaseModel):
    month: Optional[str] = None
    source_type: Optional[str] = None
    rakes_planned_for_month: Optional[int] = None
    expected_rakes: Optional[dict]
    cancelled_rakes: Optional[int] = None
    remarks: Optional[str] = None
    

#NEW 

class rcraveryUserData(BaseModel):
    indexing : Optional[int] = None
    wagon_owner : Optional[str] = None
    wagon_type : Optional[str] = None
    wagon_no : Optional[int] = None
    ser_no : Optional[int] = None
    rake_no : Optional[int] = None
    rake_id : Optional[int] = None
    wagon_no_avery : Optional[int] = None
    wagon_id : Optional[int] = None
    wagon_type : Optional[str] = None
    wagon_cc : Optional[str] = None
    mode : Optional[str] = None
    tip_startdate : Optional[datetime] = None
    tip_starttime : Optional[datetime] = None
    tip_enddate : Optional[datetime] = None
    tip_endtime : Optional[str] = None
    tipple_time : Optional[str] = None
    status : Optional[bool] = None
    gwel_gross_wt : Optional[float] = None
    gwel_tare_wt : Optional[float] = None
    gwel_net_wt : Optional[float] = None
    time_in_tipp : Optional[str] = None
    po_number : Optional[int] = None
    coal_grade : Optional[str] = None
    data_from: Optional[str] = None 
    
class averyUserData(BaseModel):
    indexing : Optional[int] = None
    wagon_owner : Optional[str] = None
    wagon_type : Optional[str] = None
    wagon_no : Optional[int] = None
    ser_no : Optional[int] = None
    rake_no : Optional[int] = None
    rake_id : Optional[int] = None
    wagon_no_avery : Optional[int] = None
    wagon_id : Optional[int] = None
    wagon_type : Optional[str] = None
    wagon_cc : Optional[str] = None
    mode : Optional[str] = None
    tip_startdate : Optional[datetime] = None
    tip_starttime : Optional[datetime] = None
    tip_enddate : Optional[datetime] = None
    tip_endtime : Optional[str] = None
    tipple_time : Optional[str] = None
    status : Optional[bool] = None
    gwel_gross_wt : Optional[float] = None
    gwel_tare_wt : Optional[float] = None
    gwel_net_wt : Optional[float] = None
    time_in_tipp : Optional[str] = None
    po_number : Optional[int] = None
    coal_grade : Optional[str] = None
    data_from: Optional[str] = None
    
class RailwayData(BaseModel):
    rr_no: Optional[int] = None
    rr_qty: Optional[int] = None
    po_no: Optional[int] = None
    po_date: Optional[datetime] = None
    line_item: Optional[int] = None
    source: Optional[str] = None
    placement_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    drawn_date: Optional[datetime] = None
    total_ul_wt: Optional[float] = None
    boxes_supplied: Optional[int] = None
    total_secl_gross_wt: Optional[float] = None
    total_secl_tare_wt: Optional[float] = None
    total_secl_net_wt: Optional[float] = None
    total_secl_ol_wt: Optional[float] = None
    boxes_loaded: Optional[int] = None
    total_rly_gross_wt: Optional[float] = None
    total_rly_tare_wt: Optional[float] = None
    total_rly_net_wt: Optional[float] = None
    total_rly_ol_wt: Optional[float] = None
    total_secl_chargable_wt: Optional[float] = None
    total_rly_chargable_wt: Optional[float] = None
    freight: Optional[float] = None
    gst: Optional[float] = None
    pola: Optional[float] = None
    sd: Optional[str] = None
    total_freight: Optional[float] = None
    source_type: Optional[str] = None
    secl_rly_data: List[dict]
    month: Optional[str] = None
    GWEL_pending_wagons: Optional[int] = None
    GWEL_received_wagons: Optional[int] = None
    total_gwel_gross_wt: Optional[float] = None
    total_gwel_net_wt: Optional[float] = None
    total_gwel_tare_wt: Optional[float] = None
    avery_completion_date: Optional[datetime] = None
    avery_placement_date: Optional[datetime] = None
    avery_rly_data : List[rcraveryUserData] =None


 

class mainAveryData(BaseModel):
    data : List[averyUserData]
