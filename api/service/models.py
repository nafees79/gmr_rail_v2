from api.logger.logger import console_logger
from mongoengine import connect
import datetime, uuid
from dateutil import tz

from mongoengine import (StringField,
                         DateTimeField, 
                         Document, 
                         BooleanField,
                         IntField,
                         DictField,
                         ListField, 
                         FloatField, 
                         EmbeddedDocumentListField,
                         EmbeddedDocument,
                         DateField)

to_zone = tz.gettz("Asia/Kolkata")
file = str(datetime.datetime.now().strftime("%d-%m-%Y"))

connect('GMR_DB', alias='GMR_DB-alias', host='mongodb://admin:%40ccessDenied321@192.168.1.42:27017/GMR_DB?authSource=admin')


################################     Save Tare Request      #############################################

class SeclRailData(EmbeddedDocument):
    indexing = IntField()
    wagon_owner = StringField()
    wagon_type = StringField()
    wagon_no = IntField()
    secl_cc_wt = FloatField()
    secl_gross_wt = FloatField()
    secl_tare_wt = FloatField()
    secl_net_wt = FloatField()
    secl_ol_wt = FloatField()
    secl_ul_wt = FloatField()
    secl_chargable_wt = FloatField()
    rly_cc_wt = FloatField()
    rly_gross_wt = FloatField()
    rly_tare_wt = FloatField()
    rly_net_wt = FloatField()
    rly_permissible_cc_wt = FloatField()
    rly_ol_wt = FloatField()
    rly_norm_rate = FloatField()
    rly_pun_rate = FloatField()
    rly_chargable_wt = FloatField()
    rly_sliding_adjustment = FloatField()

    def payload(self):
        return {
            "indexing": self.indexing,
            "wagon_owner": self.wagon_owner, 
            "wagon_type": self.wagon_type,
            "wagon_no": self.wagon_no,
            "secl_cc_wt": self.secl_cc_wt,
            "secl_gross_wt": self.secl_gross_wt,
            "secl_tare_wt": self.secl_tare_wt,
            "secl_net_wt": self.secl_net_wt,
            "secl_ol_wt": self.secl_ol_wt,
            "secl_ul_wt": self.secl_ul_wt,
            "secl_chargable_wt": self.secl_chargable_wt,
            "rly_cc_wt": self.rly_cc_wt,
            "rly_gross_wt": self.rly_gross_wt,
            "rly_tare_wt": self.rly_tare_wt,
            "rly_net_wt": self.rly_net_wt,
            "rly_permissible_cc_wt": self.rly_permissible_cc_wt,
            "rly_ol_wt": self.rly_ol_wt,
            "rly_norm_rate": self.rly_norm_rate,
            "rly_pun_rate": self.rly_pun_rate,
            "rly_chargable_wt": self.rly_chargable_wt,
            "rly_sliding_adjustment": self.rly_sliding_adjustment,
        }

    def rlypayload(self):
        return {
            "indexing": self.indexing,
            "wagon_owner": self.wagon_owner, 
            "wagon_type": self.wagon_type,
            "wagon_no": self.wagon_no,
            "rly_cc_wt": self.rly_cc_wt,
            "rly_gross_wt": self.rly_gross_wt,
            "rly_tare_wt": self.rly_tare_wt,
            "rly_net_wt": self.rly_net_wt,
            "rly_permissible_cc_wt": self.rly_permissible_cc_wt,
            "rly_ol_wt": self.rly_ol_wt,
            "rly_norm_rate": self.rly_norm_rate,
            "rly_pun_rate": self.rly_pun_rate,
            "rly_chargable_wt": self.rly_chargable_wt,
            "rly_sliding_adjustment": self.rly_sliding_adjustment,
        }
    
class AveryRailData(EmbeddedDocument):
    indexing = IntField()
    wagon_owner = StringField()
    wagon_type = StringField()
    wagon_no = IntField()
    ser_no = IntField()
    rake_no = IntField()
    rake_id = IntField()
    wagon_no_avery = IntField()
    wagon_id = IntField()
    wagon_type_avery = IntField()
    wagon_cc = StringField()
    mode = StringField()
    tip_startdate = DateTimeField()
    tip_starttime = DateTimeField()
    tip_enddate = DateTimeField()
    tip_endtime = StringField()
    tipple_time = StringField()
    status = BooleanField()
    # wagon_gross_wt = StringField()
    # wagon_tare_wt = StringField()
    # wagon_net_wt = StringField()
    gwel_gross_wt = FloatField()
    gwel_tare_wt = FloatField()
    gwel_net_wt = FloatField()
    time_in_tipp = StringField()
    po_number = IntField()
    coal_grade = StringField()
    data_from = StringField()

    def payload(self):
        return {
            "indexing": self.indexing,
            "wagon_owner": self.wagon_owner,
            "wagon_type": self.wagon_type,
            "wagon_no": self.wagon_no,
            "ser_no": self.ser_no,
            "rake_no": self.rake_no,
            "rake_id": self.rake_id,
            "wagon_no_avery": self.wagon_no_avery,
            "wagon_id": self.wagon_id,
            "wagon_type": self.wagon_type,
            "wagon_cc": self.wagon_cc,
            "mode": self.mode,
            "tip_startdate": self.tip_startdate,
            "tip_starttime": self.tip_starttime,
            "tip_enddate": self.tip_enddate,
            "tip_endtime": self.tip_endtime,
            "tipple_time": self.tipple_time,
            "status": self.status,
            "wagon_type_avery": self.wagon_type_avery,
            # "wagon_gross_wt": self.wagon_gross_wt,
            # "wagon_tare_wt": self.wagon_tare_wt,
            # "wagon_net_wt": self.wagon_net_wt,
            "gwel_gross_wt": self.gwel_gross_wt,
            "gwel_tare_wt": self.gwel_tare_wt,
            "gwel_net_wt": self.gwel_net_wt,
            "time_in_tipp": self.time_in_tipp,
            "po_number": self.po_number,
            "coal_grade": self.coal_grade,
            "data_from": self.data_from,
        }
    

class Gmrdata(Document):
    record_id = StringField(default=uuid.uuid4().hex, unique=True)
    vehicle_number = StringField()
    vehicle_out_time = DateTimeField(null=True)
    delivery_challan_number = IntField()            
    arv_cum_do_number = IntField()        
    mine = StringField()
    gross_qty = FloatField()                       # gross weight extracted from challan
    tare_qty = FloatField()                        # tare weight extracted from challan        
    net_qty = FloatField()                         # net weight extracted from challan
    delivery_challan_date = DateTimeField()
    type_consumer = StringField()
    grade = StringField()
    weightment_date = DateTimeField() 
    weightment_time = StringField()
    total_net_amount = IntField() 
    challan_file = StringField()

    # lr_fasttag = BooleanField(default=False)
    lr_fasttag = BooleanField(default=True)
    
    driver_name = StringField()
    gate_pass_no = StringField()
    fr_file = StringField()

    transporter_lr_no = IntField(null=True)
    transporter_lr_date = DateTimeField(null=True)
    gate_user = StringField(null=True)

    gate_approved = BooleanField(default=False)
    gate_fastag  = BooleanField(default=False)
    
    vehicle_chassis_number = StringField()
    certificate_expiry = DateTimeField()
    actual_gross_qty = FloatField(null=True)            # actual gross weight measured from weightbridge
    actual_tare_qty = FloatField(null=True)             # actual tare weight measured from weightbridge
    actual_net_qty = FloatField(null=True)             # actual net weight measured from weightbridge
    # wastage = StringField(null=True)
    fitness_file = StringField()
    po_no = IntField(null=True)
    po_date = DateTimeField(null=True)
    po_qty = IntField(null=True)

    
    dc_request = BooleanField(default=False)
    
    tare_request = BooleanField(default=False)

    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)

    do_date = DateTimeField(null=True)
    po_amount = IntField(null=True)
    slno = DateTimeField(null=True)

    created_at = DateTimeField(default=datetime.datetime.utcnow())

    # remark = StringField(null=True)
  
    vehicle_in_time = DateTimeField(null=True)
    lot = StringField()
    line_item = IntField(null=True)
    GWEL_Gross_Time = DateTimeField(null=True)
    GWEL_Tare_Time = DateTimeField(null=True)
    grn_status  = BooleanField(default=False)

    #
    camera_name = StringField() 
    out_camera_name = StringField()
    direction = StringField()
    vehicle_type = StringField()
    vehicle_brand = StringField()
    plate_image = StringField()
    out_plate_image = StringField()
    vehicle_image = StringField()
    out_vehicle_image = StringField()
    transporter_lr_time = StringField(null=True)
    e_way_bill_no = StringField(null=True)
    lr_file = StringField()
    gross_weighbridge = StringField(null=True)
    tare_weighbridge = StringField(null=True)
    do_qty = StringField(null=True)
    mine_invoice = StringField(null=True)   #added on 11-11-2024 on 06:29pm
    dc_request_status = BooleanField(default=None, null=True)
    tare_request_status = BooleanField(default=None, null=True)


    ID = IntField(min_value=1)

    meta = {"db_alias" : "GMR_DB-alias" , "collection" : "gmrdata"}


    def payload(self):

        Loss = None
        transit_loss=None
        tat=None

        if self.net_qty is not None and self.actual_net_qty is not None:
            Loss = self.actual_net_qty - self.net_qty
            transit_loss = round(Loss,5)
            
        if self.vehicle_in_time is not None and self.GWEL_Tare_Time is not None:
            diff = self.GWEL_Tare_Time - self.vehicle_in_time
            days = diff.days
            seconds = diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            components = []
            if days > 0:
                components.append(f"{days} days")
            if hours > 0:
                components.append(f"{hours} hours")
            if minutes > 0:
                components.append(f"{minutes} minutes")
            if seconds > 0:
                components.append(f"{seconds} seconds")
            
            tat = ", ".join(components)

        return {"record_id":self.record_id,
                "_id": str(self.id),
                "Sr.No.":self.ID,
                "Mines_Name":self.mine,
                "PO_No":self.po_no,
                "PO_Date":self.po_date,
                "DO_Qty":self.po_qty, 
                "Delivery_Challan_No":self.delivery_challan_number,
                "DO_No":self.arv_cum_do_number,
                "Grade":self.grade,
                "Type_of_consumer":self.type_consumer,
                "DC_Date":self.delivery_challan_date,
                "vehicle_number":self.vehicle_number,
                "Vehicle_Chassis_No":self.vehicle_chassis_number,
                "Fitness_Expiry":self.certificate_expiry,
                "Total_net_amount":self.total_net_amount,
                # "In gate": self.camera_name if self.camera_name else None,
                "Weightment_Date" : self.weightment_date,
                "Weightment_Time" : self.weightment_time,
                # "Out gate": self.out_camera_name if self.out_camera_name else None,
                "Challan_Gross_Wt(MT)" : self.gross_qty,
                "Challan_Tare_Wt(MT)" : self.tare_qty,
                "Challan_Net_Wt(MT)" : self.net_qty,
                "GWEL_Gross_Wt(MT)" : self.actual_gross_qty,
                "GWEL_Tare_Wt(MT)" : self.actual_tare_qty,
                "GWEL_Net_Wt(MT)" : self.actual_net_qty,
                # "Wastage" : self.wastage,
                "Driver_Name" : self.driver_name,
                "Gate_Pass_No" : self .gate_pass_no,
                "Transporter_LR_No": self.transporter_lr_no,
                "Transporter_LR_Date": self.transporter_lr_date,
                "Eway_bill_No": self.e_way_bill_no,
                # "Gate_verified_time" : datetime.datetime.fromisoformat(
                #                     self.gate_verified_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                #                     ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.gate_verified_time else None,

                
                "Vehicle_in_time" : datetime.datetime.fromisoformat(
                                    self.vehicle_in_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.vehicle_in_time else None,

                "Vehicle_out_time" : datetime.datetime.fromisoformat(
                                    self.vehicle_out_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.vehicle_out_time else None,
                
                "Challan_image" : self.challan_file if self.challan_file else None,
                "Fitness_image": self.fitness_file if self.fitness_file else None,
                "Face_image": self.fr_file if self.fr_file else None,
                "Transit_Loss": transit_loss if transit_loss else 0,
                "LOT":self.lot,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "do_date": self.do_date,
                "po_amount": self.po_amount,
                "slno": self.slno,
                "grn_status": self.grn_status,
                "Line_Item" : self.line_item if self.line_item else None,

                "GWEL_Gross_Time" : datetime.datetime.fromisoformat(
                                    self.GWEL_Gross_Time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.GWEL_Gross_Time else None,

                "GWEL_Tare_Time" : datetime.datetime.fromisoformat(
                                    self.GWEL_Tare_Time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.GWEL_Tare_Time else None,

                "Scanned_Time" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,

                "mine_date" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,

                "TAT_difference": tat,
                }
    

################################     Tare Alert      #############################################



class Gmrrequest(Document):
    record_id = StringField(default=uuid.uuid4().hex, unique=True)
    mine = StringField()
    vehicle_number = StringField()
    delivery_challan_number = IntField()
    arv_cum_do_number = IntField()
    vehicle_chassis_number = StringField()
    certificate_expiry = DateTimeField()
    delivery_challan_date = DateTimeField()
    net_qty = FloatField()
    tare_qty = FloatField()
    actual_tare_qty = FloatField()
    total_net_amount = FloatField()
    expiry_validation = BooleanField(default = True)
    request = StringField(null=True)
    approved_at = DateTimeField(null=True)
    remark = StringField(null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    ID = IntField(min_value=1)

    meta = {"db_alias" : "GMR_DB-alias" , "collection" : "gmrrequest"}


    def payload(self):
        return {
                "Sr.No.":self.ID,
                "Request_type": self.request.replace("_", " "),
                "Mine":self.mine,
                "Vehicle_Number":self.vehicle_number,
                "Delivery_Challan_No":self.delivery_challan_number,
                "DO_No":self.arv_cum_do_number,
                "Vehicle_Chassis_No":self.vehicle_chassis_number,
                "Fitness_Expiry":self.certificate_expiry,
                "DC_Date":self.delivery_challan_date,
                "Challan_Net_Wt(MT)" : self.net_qty,
                "Total_net_amount":self.total_net_amount,
                "Request_Time" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
                "Comment" : self.remark,
                }
    
    def tare_payload(self):
        return {
                "Sr.No.":self.ID,
                "Request_type": self.request.replace("_", " "),
                "Mine":self.mine,
                "Vehicle_Number":self.vehicle_number,
                "Delivery_Challan_No":self.delivery_challan_number,
                "DO_No":self.arv_cum_do_number,
                "Vehicle_Chassis_No":self.vehicle_chassis_number,
                "Fitness_Expiry":self.certificate_expiry,
                "DC_Date":self.delivery_challan_date,
                "Challan_Net_Wt(MT)" : self.net_qty,
                "Challan_Tare_Wt(MT)" : self.tare_qty,
                "GWEL_Tare_Wt(MT)" : self.actual_tare_qty,
                "Total_net_amount":self.total_net_amount,
                "Request_Time" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
                "Comment" : self.remark,
                }

    def history_payload(self):

        tat = None
        if self.created_at and self.approved_at:
            diff = self.approved_at - self.created_at
            days = diff.days
            seconds = diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            components = []
            if days > 0:
                components.append(f"{days} days")
            if hours > 0:
                components.append(f"{hours} hours")
            if minutes > 0:
                components.append(f"{minutes} minutes")
            if seconds > 0:
                components.append(f"{seconds} seconds")
            
            tat = ", ".join(components)

        return {
                "Sr.No.":self.ID,
                "Request_type": self.request.replace("_", " "),
                "Mine":self.mine,
                "Vehicle_Number":self.vehicle_number,
                "Delivery_Challan_No":self.delivery_challan_number,
                "DO_No":self.arv_cum_do_number,
                "Vehicle_Chassis_No":self.vehicle_chassis_number,
                "Fitness_Expiry":self.certificate_expiry,
                "DC_Date":self.delivery_challan_date,
                "Challan_Net_Wt(MT)" : self.net_qty,
                "Total_net_amount":self.total_net_amount,
                "Remark" : self.remark,

                "Request_Time" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,

                "Approval_Time" : datetime.datetime.fromisoformat(
                    self.approved_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.approved_at else None,

                "TAT":tat                # Turn Around Time
                }

    def history_tare_payload(self):

        tat = None
        if self.created_at and self.approved_at:
            diff = self.approved_at - self.created_at
            days = diff.days
            seconds = diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            components = []
            if days > 0:
                components.append(f"{days} days")
            if hours > 0:
                components.append(f"{hours} hours")
            if minutes > 0:
                components.append(f"{minutes} minutes")
            if seconds > 0:
                components.append(f"{seconds} seconds")
            
            tat = ", ".join(components)

        return {
                "Sr.No.":self.ID,
                "Request_type": self.request.replace("_", " "),
                "Mine":self.mine,
                "Vehicle_Number":self.vehicle_number,
                "Delivery_Challan_No":self.delivery_challan_number,
                "DO_No":self.arv_cum_do_number,
                "Vehicle_Chassis_No":self.vehicle_chassis_number,
                "Fitness_Expiry":self.certificate_expiry,
                "DC_Date":self.delivery_challan_date,
                "Challan_Net_Wt(MT)" : self.net_qty,
                "Challan_Tare_Wt(MT)" : self.tare_qty,
                "GWEL_Tare_Wt(MT)" : self.actual_tare_qty,
                "Total_net_amount":self.total_net_amount,
                "Remark" : self.remark,

                "Request_Time" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,

                "Approval_Time" : datetime.datetime.fromisoformat(
                    self.approved_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.approved_at else None,

                "TAT":tat                # Turn Around Time
                }




class ReportScheduler(Document):
    report_name = StringField()
    recipient_list = ListField(StringField(unique=True), default=[])
    cc_list = ListField(StringField(unique=True), default=[])
    bcc_list = ListField(StringField(unique=True), default=[])
    filter = StringField(default="")
    schedule = StringField(default="")
    # shift_schedule = DictField(null=True)
    shift_schedule = ListField(default=[])
    time = StringField(default="")
    active = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    


    meta = {"db_alias": "GMR_DB-alias", "collection": "reportscheduler"}

    

    def payload(self):
        return {
            "id": str(self.id),
            "report_name": self.report_name,
            "recipient_list": self.recipient_list,
            "cc_list": self.cc_list,
            "bcc_list": self.bcc_list,
            "filter": self.filter,
            "schedule": self.schedule,
            "shift_schedule": self.shift_schedule,
            "time": self.time,
            "active": self.active,
            "created_at": self.created_at,
        }
    
    def report_payload(self):
        return{
            "id": str(self.id),
            "name": self.report_name,
        } 

    def status_payload(self):
        return{
            "id": str(self.id),
            "name": self.report_name,
            "active": self.active,
        } 


class EmailDevelopmentCheck(Document):
    development = StringField(default=None)
    avery_id = StringField(default=None)
    avery_pass = StringField(defaut=None)
    wagontrippler1 = StringField(default=None)
    wagontrippler2 = StringField(default=None)
    port = StringField(default=None)

    meta = {"db_alias": "GMR_DB-alias", "collection": "EmailDevelopmentCheck"}


    def payload(self):
        return {
            "development": self.development,
        }

class gmrdataHistoric(Document):
    record_id = StringField(default=uuid.uuid4().hex, unique=True)
    
    vehicle_number = StringField()
    
    vehicle_out_time = DateTimeField(null=True)
    
    delivery_challan_number = IntField()
    arv_cum_do_number = IntField()
    mine = StringField()
    gross_qty = FloatField()                       # gross weight extracted from challan
    tare_qty = FloatField()                        # tare weight extracted from challan        
    net_qty = FloatField()                         # net weight extracted from challan
    delivery_challan_date = DateTimeField()
    type_consumer = StringField()
    grade = StringField()
    weightment_date = DateTimeField() 
    weightment_time = StringField()
    challan_file = StringField()

    # lr_fasttag = BooleanField(default=False)
    lr_fasttag = BooleanField(default=True)
    
    driver_name = StringField()
    gate_pass_no = IntField()
    fr_file = StringField()

    transporter_lr_no = IntField(null=True)
    transporter_lr_date = DateTimeField(null=True)
    
    e_way_bill_no = StringField(null=True)
    gate_user = StringField(null=True)

    gate_approved = BooleanField(default=False)
    gate_fastag  = BooleanField(default=False)
    
    vehicle_chassis_number = StringField()
    certificate_expiry = DateTimeField()
    actual_gross_qty = FloatField(null=True)            # actual gross weight measured from weightbridge
    actual_tare_qty = FloatField(null=True)             # actual tare weight measured from weightbridge
    actual_net_qty = FloatField(null=True)             # actual net weight measured from weightbridge
    # wastage = StringField(null=True)
    fitness_file = StringField()
    lr_file = StringField()
    po_no = IntField(null=True)
    po_date = DateTimeField(null=True)
    po_qty = IntField(null=True)

    gross_weighbridge = StringField(null=True)
    tare_weighbridge = StringField(null=True)

    dc_request = BooleanField(default=False)
    
    tare_request = BooleanField(default=False)

    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)

    do_date = DateTimeField(null=True)
    do_qty = StringField(null=True)
    po_amount = FloatField(null=True)
    slno = DateTimeField(null=True)

    created_at = DateTimeField(default=datetime.datetime.utcnow())

    # remark = StringField(null=True)
  
    vehicle_in_time = DateTimeField(null=True)
    lot = StringField()
    line_item = IntField(null=True)
    GWEL_Gross_Time = DateTimeField(null=True)
    GWEL_Tare_Time = DateTimeField(null=True)
    grn_status  = BooleanField(default=False)
    ID = IntField(min_value=1)


    #
    camera_name = StringField()
    out_camera_name = StringField()
    direction = StringField()
    vehicle_type = StringField()
    vehicle_brand = StringField()
    plate_image = StringField()
    out_plate_image = StringField()
    vehicle_image = StringField()
    out_vehicle_image = StringField()
    total_net_amount = StringField() 
    transporter_lr_time = StringField(null=True)
    dc_request_status = BooleanField(default=None, null=True)
    tare_request_status = BooleanField(default=None, null=True)



    meta = {"db_alias" : "GMR_DB-alias" , "collection" : "gmrdataHistoric"}


    def payload(self):

        Loss = None
        transit_loss=None
        tat=None

        if self.net_qty is not None and self.actual_net_qty is not None:
            Loss = float(self.actual_net_qty) - float(self.net_qty)
            transit_loss = round(Loss,5)
            
        if self.vehicle_in_time is not None and self.GWEL_Tare_Time is not None:
            diff = self.GWEL_Tare_Time - self.vehicle_in_time
            days = diff.days
            seconds = diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            components = []
            if days > 0:
                components.append(f"{days} days")
            if hours > 0:
                components.append(f"{hours} hours")
            if minutes > 0:
                components.append(f"{minutes} minutes")
            if seconds > 0:
                components.append(f"{seconds} seconds")
            
            tat = ", ".join(components)

        return {"record_id":self.record_id,
                "Sr.No.":self.ID,
                "Mines_Name":self.mine,
                "PO_No":self.po_no,
                "PO_Date":self.po_date,
                "DO_Qty":self.po_qty, 
                "Delivery_Challan_No":self.delivery_challan_number,
                "DO_No":self.arv_cum_do_number,
                "Grade":self.grade,
                "Type_of_consumer":self.type_consumer,
                "DC_Date":self.delivery_challan_date,
                "vehicle_number":self.vehicle_number,
                "Vehicle_Chassis_No":self.vehicle_chassis_number,
                "Fitness_Expiry":self.certificate_expiry,
                "Total_net_amount":self.total_net_amount,
                # "In gate": self.camera_name if self.camera_name else None,
                "Weightment_Date" : self.weightment_date,
                "Weightment_Time" : self.weightment_time,
                # "Out gate": self.out_camera_name if self.out_camera_name else None,
                "Challan_Gross_Wt(MT)" : self.gross_qty,
                "Challan_Tare_Wt(MT)" : self.tare_qty,
                "Challan_Net_Wt(MT)" : self.net_qty,
                "GWEL_Gross_Wt(MT)" : self.actual_gross_qty,
                "GWEL_Tare_Wt(MT)" : self.actual_tare_qty,
                "GWEL_Net_Wt(MT)" : self.actual_net_qty,
                # "Wastage" : self.wastage,
                "Driver_Name" : self.driver_name,
                "Gate_Pass_No" : self .gate_pass_no,
                "Transporter_LR_No": self.transporter_lr_no,
                "Transporter_LR_Date": self.transporter_lr_date,
                "Eway_bill_No": self.e_way_bill_no,
                # "Gate_verified_time" : datetime.datetime.fromisoformat(
                #                     self.gate_verified_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                #                     ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.gate_verified_time else None,

                "Vehicle_in_time" : datetime.datetime.fromisoformat(
                                    self.vehicle_in_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.vehicle_in_time else None,

                "Vehicle_out_time" : datetime.datetime.fromisoformat(
                                    self.vehicle_out_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.vehicle_out_time else None,
                
                "Challan_image" : self.challan_file if self.challan_file else None,
                "Fitness_image": self.fitness_file if self.fitness_file else None,
                "Face_image": self.fr_file if self.fr_file else None,
                "Transit_Loss": transit_loss if transit_loss else 0,
                "LOT":self.lot,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "do_date": self.do_date,
                "po_amount": self.po_amount,
                "slno": self.slno,
                "grn_status": self.grn_status,
                "Line_Item" : self.line_item if self.line_item else None,

                "GWEL_Gross_Time" : datetime.datetime.fromisoformat(
                                    self.GWEL_Gross_Time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.GWEL_Gross_Time else None,

                "GWEL_Tare_Time" : datetime.datetime.fromisoformat(
                                    self.GWEL_Tare_Time.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.GWEL_Tare_Time else None,

                "Scanned_Time" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,

                "mine_date" : datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,

                "TAT_difference": tat,
                }
    

class SapRecords(Document):
    slno = DateTimeField(null=True)
    source = StringField(null=True)
    mine_name = StringField(null=True)
    sap_po = IntField(null=True)                      #po_number
    line_item = IntField(null=True)
    do_no = IntField(null=True)
    do_qty = IntField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    grade = StringField(null=True)
    do_date = DateTimeField(null=True)
    consumer_type = StringField(null=True)
    po_amount = FloatField(null=True)
    transport_code = IntField(null=True)
    transport_name = StringField(null=True)
    material_code = IntField(null=True)
    material_description = StringField(null=True)
    plant_code = IntField(null=True)
    storage_location = StringField(null=True)
    valuation_type = StringField(null=True)
    po_open_quantity = FloatField(null=True)
    uom = StringField(null=True)

    #particulars start 
    basic_price = FloatField(null=True)
    sizing_charges = FloatField(null=True)
    stc_charges = FloatField(null=True)
    evac_facility_charges = FloatField(null=True)
    royality_charges = FloatField(null=True)
    nmet_charges = FloatField(null=True)
    dmf = FloatField(null=True)
    cgst = FloatField(null=True)
    sgst = FloatField(null=True)
    gst_comp_cess = FloatField(null=True)
    so_value_grand_total = FloatField(null=True)
    #particulars end

    created_at = DateTimeField(default=datetime.datetime.utcnow())

    meta = {"db_alias": "GMR_DB-alias", "collection": "SapRecords"}


    def payload(self):
        return {
            # "id": str(self.id),
            "slno": self.slno,
            "source": self.source,
            "mine_name": self.mine_name,
            "sap_po": self.sap_po,
            "line_item": self.line_item,
            "do_no": self.do_no,
            "do_qty": self.do_qty,
        }

    def SimplePayload(self):
        return {
            # "id": str(self.id),
            "slno": self.slno,
            "source": self.source,
            "mine_name": self.mine_name,
            "sap_po": self.sap_po,
            "line_item": self.line_item,
            "do_no": self.do_no,
            "do_qty": self.do_qty,
            # "rake_no": self.rake_no,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "grade": self.grade,
            # "po_date": self.po_date,
        }
    


class RcrData(Document):
    rr_no = IntField()
    rr_qty = FloatField(null=True)
    po_no = IntField(null=True)
    po_date = DateTimeField(null=True)
    line_item = IntField(null=True)
    source = StringField(null=True)
    placement_date = DateTimeField(null=True)
    completion_date = DateTimeField(null=True)
    avery_placement_date = DateTimeField(null=True)
    avery_completion_date = DateTimeField(null=True)
    drawn_date = DateTimeField(null=True)
    total_ul_wt = FloatField(null=True)
    boxes_supplied = IntField(null=True)
    total_secl_gross_wt = FloatField(null=True)
    total_secl_tare_wt = FloatField(null=True)
    total_secl_net_wt = FloatField(null=True)
    total_secl_ol_wt = FloatField(null=True)
    boxes_loaded = IntField(null=True)
    total_rly_gross_wt = FloatField(null=True)
    total_rly_tare_wt = FloatField(null=True)
    total_rly_net_wt = FloatField(null=True)
    total_rly_ol_wt = FloatField(null=True)
    total_secl_chargable_wt = FloatField(null=True)
    total_rly_chargable_wt = FloatField(null=True)
    freight = FloatField(null=True)
    gst = FloatField(null=True)
    pola = FloatField(null=True)
    total_freight = FloatField(null=True)
    sd = StringField(null=True)
    source_type = StringField(null=True)
    month = DateTimeField(null=True)
    rr_date = DateTimeField(null=True)
    siding = StringField(null=True)
    mine = StringField(null=True)
    grade = StringField(null=True)
    po_amount = FloatField(null=True)
    rake_no = StringField(null=True)
    GWEL_received_wagons = IntField(null=True)
    GWEL_pending_wagons = IntField(null=True)
    total_gwel_gross = FloatField(null=True)
    total_gwel_tare = FloatField(null=True)
    total_gwel_net = FloatField(null=True)
    Total_gwel_gross = FloatField(null=True)
    Total_gwel_tare = FloatField(null=True)
    Total_gwel_net = FloatField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    slno = DateTimeField(null=True)
    type_consumer = StringField(null=True)
    po_qty = IntField(null=True)

    penalty_ol = StringField(null=True)                    # modified by faisal
    penal_ul = StringField(null=True)                      # modified by faisal
    freight_pmt = StringField(null=True)                   # modified by faisal              

    secl_rly_data = EmbeddedDocumentListField(SeclRailData)
    avery_rly_data = EmbeddedDocumentListField(AveryRailData)
    created_at = DateTimeField(default=datetime.datetime.now)

    grn_status = BooleanField(default=False)
    mine_invoice = StringField(null=True)
    
    meta = {"db_alias": "GMR_DB-alias", "collection": "RcrData"}

    def payload(self):
        seclrail = []
        for serl_data in self.secl_rly_data:
            seclrail.append(serl_data.rlypayload())

        return {
            "id": str(self.id),
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_secl_ol_wt": self.total_secl_ol_wt,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_secl_chargable_wt": self.total_secl_chargable_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "secl_rly_data": seclrail,
            
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    
    def averyPayload(self):
        averyrail = []
        for avery_data in self.avery_rly_data:
            averyrail.append(avery_data.payload())

        seclrail = []
        for serl_data in self.secl_rly_data:
            seclrail.append(serl_data.payload())

        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_secl_ol_wt": self.total_secl_ol_wt,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_secl_chargable_wt": self.total_secl_chargable_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "sd": self.sd,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "GWEL_received_wagons": self.GWEL_received_wagons,
            "GWEL_pending_wagons": self.GWEL_pending_wagons,
            "GWEL_Total_gwel_gross": self.Total_gwel_gross,
            "GWEL_Total_gwel_tare": self.Total_gwel_tare,
            "GWEL_Total_gwel_net": self.Total_gwel_net,
            "secl_rly_data": seclrail,
            "avery_rly_data": averyrail,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def averyPayloadMain(self):
        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "GWEL_placement_date": self.avery_placement_date,
            "GWEL_completion_date": self.avery_completion_date,
            "boxes_loaded": self.boxes_loaded,
            # "GWEL_received_wagons"
            # "GWEL_pending_wagons"
            # "total_gwel_gross_wt"
            # "total_gwel_tare_wt"
            # "total_gwel_net_wt"
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "sd": self.sd,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "GWEL_received_wagons": self.GWEL_received_wagons,
            "GWEL_pending_wagons": self.GWEL_pending_wagons,
            "GWEL_Total_gwel_gross": self.Total_gwel_gross,
            "GWEL_Total_gwel_tare": self.Total_gwel_tare,
            "GWEL_Total_gwel_net": self.Total_gwel_net,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def simplepayloadold(self):
        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_secl_ol_wt": self.total_secl_ol_wt,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_secl_chargable_wt": self.total_secl_chargable_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def simplepayload(self):
        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "avery_placement_date": self.avery_placement_date,
            "avery_completion_date": self.avery_completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "po_qty": self.po_qty,
            "type_consumer": self.type_consumer,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }


class Historian(Document):
    tagid = IntField()
    sum = FloatField()
    created_date =  DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    # ID = IntField(min_value=1)

    meta = {"db_alias" : "GMR_DB-alias" , "collection" : "historian"}


    def payload(self):
        return {
                "tagid": self.tagid,
                "sum": self.sum
            }
 

class RailData(Document):
    rr_no = IntField()
    rr_qty = FloatField(null=True)
    po_no = IntField(null=True)
    po_date = DateTimeField(null=True)
    line_item = IntField(null=True)
    source = StringField(null=True)
    placement_date = DateTimeField(null=True)
    completion_date = DateTimeField(null=True)
    avery_placement_date = DateTimeField(null=True)
    avery_completion_date = DateTimeField(null=True)
    drawn_date = DateTimeField(null=True)
    total_ul_wt = FloatField(null=True)
    boxes_supplied = IntField(null=True)
    total_secl_gross_wt = FloatField(null=True)
    total_secl_tare_wt = FloatField(null=True)
    total_secl_net_wt = FloatField(null=True)
    total_secl_ol_wt = FloatField(null=True)
    boxes_loaded = IntField(null=True)
    total_rly_gross_wt = FloatField(null=True)
    total_rly_tare_wt = FloatField(null=True)
    total_rly_net_wt = FloatField(null=True)
    total_rly_ol_wt = FloatField(null=True)
    total_secl_chargable_wt = FloatField(null=True)
    total_rly_chargable_wt = FloatField(null=True)
    freight = FloatField(null=True)
    gst = FloatField(null=True)
    pola = FloatField(null=True)
    total_freight = FloatField(null=True)
    sd = StringField(null=True)
    source_type = StringField(null=True)
    month = StringField(null=True)
    rr_date = DateTimeField(null=True)
    siding = StringField(null=True)
    mine = StringField(null=True)
    grade = StringField(null=True)
    po_amount = FloatField(null=True)
    rake_no = StringField(null=True)
    GWEL_received_wagons = IntField(null=True)
    GWEL_pending_wagons = IntField(null=True)
    Total_gwel_gross = FloatField(null=True)
    Total_gwel_tare = FloatField(null=True)
    Total_gwel_net = FloatField(null=True)

    penalty_ol = StringField(null=True)                    # modified by faisal
    penal_ul = StringField(null=True)                      # modified by faisal
    freight_pmt = StringField(null=True)                   # modified by faisal              

    grn_status = BooleanField(default=False)
    mine_invoice = StringField(null=True)

    secl_rly_data = EmbeddedDocumentListField(SeclRailData)
    avery_rly_data = EmbeddedDocumentListField(AveryRailData)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"db_alias": "GMR_DB-alias", "collection": "raildata"}


    def payload(self):
        seclrail = []
        for serl_data in self.secl_rly_data:
            seclrail.append(serl_data.payload())

        return {
            "id": str(self.id),
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "avery_placement_date": self.avery_placement_date,
            "avery_completion_date": self.avery_completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_secl_ol_wt": self.total_secl_ol_wt,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_secl_chargable_wt": self.total_secl_chargable_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "Total_gwel_gross": self.Total_gwel_gross,
            "Total_gwel_tare": self.Total_gwel_tare,
            "Total_gwel_net": self.Total_gwel_net,
            "secl_rly_data": seclrail,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    
    def averyPayload(self):
        averyrail = []
        for avery_data in self.avery_rly_data:
            averyrail.append(avery_data.payload())

        seclrail = []
        for serl_data in self.secl_rly_data:
            seclrail.append(serl_data.payload())

        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "avery_placement_date": self.avery_placement_date,
            "avery_completion_date": self.avery_completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_secl_ol_wt": self.total_secl_ol_wt,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_secl_chargable_wt": self.total_secl_chargable_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "GWEL_received_wagons": self.GWEL_received_wagons,
            "GWEL_pending_wagons": self.GWEL_pending_wagons,
            "GWEL_Total_gwel_gross": self.Total_gwel_gross,
            "GWEL_Total_gwel_tare": self.Total_gwel_tare,
            "GWEL_Total_gwel_net": self.Total_gwel_net,
            "secl_rly_data": seclrail,
            "avery_rly_data": averyrail,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def averyPayloadMain(self):
        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "GWEL_placement_date": self.avery_placement_date,
            "GWEL_completion_date": self.avery_completion_date,
            "boxes_loaded": self.boxes_loaded,
            # "GWEL_received_wagons"
            # "GWEL_pending_wagons"
            # "total_gwel_gross_wt"
            # "total_gwel_tare_wt"
            # "total_gwel_net_wt"
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "sd": self.sd,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "GWEL_received_wagons": self.GWEL_received_wagons,
            "GWEL_pending_wagons": self.GWEL_pending_wagons,
            "GWEL_Total_gwel_gross": self.Total_gwel_gross,
            "GWEL_Total_gwel_tare": self.Total_gwel_tare,
            "GWEL_Total_gwel_net": self.Total_gwel_net,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def simplepayload(self):
        return {
            "rr_no": self.rr_no,
            "rr_qty": self.rr_qty,
            "po_no": self.po_no,
            "po_date": self.po_date,
            "line_item": self.line_item,
            "source": self.source,
            "placement_date": self.placement_date,
            "completion_date": self.completion_date,
            "drawn_date": self.drawn_date,
            "total_ul_wt": self.total_ul_wt,
            "boxes_supplied": self.boxes_supplied,
            "total_secl_gross_wt": self.total_secl_gross_wt,
            "total_secl_tare_wt": self.total_secl_tare_wt,
            "total_secl_net_wt": self.total_secl_net_wt,
            "total_secl_ol_wt": self.total_secl_ol_wt,
            "boxes_loaded": self.boxes_loaded,
            "total_rly_gross_wt": self.total_rly_gross_wt,
            "total_rly_tare_wt": self.total_rly_tare_wt,
            "total_rly_net_wt": self.total_rly_net_wt,
            "total_rly_ol_wt": self.total_rly_ol_wt,
            "total_secl_chargable_wt": self.total_secl_chargable_wt,
            "total_rly_chargable_wt": self.total_rly_chargable_wt,
            "freight": self.freight,
            "gst": self.gst,
            "pola": self.pola,
            "total_freight": self.total_freight,
            "source_type": self.source_type,
            "month": self.month,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "GWEL_received_wagons": self.GWEL_received_wagons,
            "GWEL_pending_wagons": self.GWEL_pending_wagons,
            "GWEL_Total_gwel_gross": self.Total_gwel_gross,
            "GWEL_Total_gwel_tare": self.Total_gwel_tare,
            "GWEL_Total_gwel_net": self.Total_gwel_net,
            "po_amount": self.po_amount,
            "rake_no": self.rake_no,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }


class bunkerAnalysis(Document):
    units = StringField(default=None)
    tagid = IntField(default=None)
    bunkering = StringField(default=None)
    shift_name = StringField(default=None)
    start_date = DateTimeField(default=None)
    created_date = DateTimeField(default=None)
    ID = IntField(min_value=1)
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    #
    mgcv = StringField(default=None)
    hgcv = StringField(default=None)
    ratio = StringField(default=None)


    meta = {"db_alias": "GMR_DB-alias", "collection": "bunkerAnalysis"}


    def payload(self):
        return {
            # "id": str(self.id),
            "Sr.No": self.ID,
            "shift_name": self.shift_name,
            "unit": self.units,
            "tagid": self.tagid,
            "bunkering": self.bunkering,
            "mgcv": self.mgcv,
            "hgcv": self.hgcv,
            "ratio": self.ratio,
            "created_date": self.created_date.astimezone(tz=to_zone).strftime("%Y-%m-%dT%H:%M:%S") if self.created_date else None,
            "Date": datetime.datetime.fromisoformat(
                    self.created_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%dT%H:%M:%S") if self.created_date else None,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%dT%H:%M:%S") if self.created_at else None,
        }
    

class sapRecordsRail(Document):
    month = DateTimeField(null=True)
    rr_no = IntField(null=True)
    rr_date = DateTimeField(null=True)
    siding = StringField(null=True)
    mine = StringField(null=True)
    grade = StringField(null=True)
    rr_qty = StringField(null=True)
    po_amount = FloatField(null=True)
    sap_po = IntField(null=True)
    do_date = DateTimeField(null=True) #sap po date
    line_item = IntField(null=True)
    invoice_date = DateTimeField(null=True)
    invoice_no = StringField(null=True)
    sale_date = DateTimeField(null=True)

    #particulars start

    sizing_charges = FloatField(null=True)
    evac_facility_charge = FloatField(null=True)
    royality_charges = FloatField(null=True)
    nmet_charges = FloatField(null=True)
    dmf = FloatField(null=True)
    adho_sanrachna_vikas= FloatField(null=True)
    pariyavaran_upkar = FloatField(null=True)
    assessable_value = FloatField(null=True)
    igst = FloatField(null=True)
    gst_comp_cess = FloatField(null=True)
    gross_bill_value = FloatField(null=True)
    less_underloading_charges = FloatField(null=True)
    net_value = FloatField(null=True)
    total_amount = FloatField(null=True)

    #particulars end

    


    # wclrailinvoice start
    area_code = StringField(null=True)
    area_description = StringField(null=True)
    contract_reference = IntField(null=True)
    contract_type = StringField(null=True)
    sales_order = IntField(null=True)
    # sales_order_date added on sale_date
    delivery_number = IntField(null=True)
    mode_of_dispatch = StringField(null=True)
    net_weight = FloatField(null=True)
    dnote_no = IntField(null=True)
    dnote_date = DateField(null=True)
    loading_date = DateField(null=True)
    rake_sq_no = IntField(null=True)
    sanction_no = StringField(null=True)
    # bill start
    del_no = IntField(null=True)
    plant = StringField(null=True)
    # material = IntField(null=True) # added in material code
    gcv = StringField(null=True)
    hsn_code = IntField(null=True)
    stc_charges = FloatField(null=True)
    basic_rate = FloatField(null=True)
    billed_quantity = FloatField(null=True)
    # bill end

    # particulars start
    basic_price_rate = FloatField(null=True)
    basic_price_amount = FloatField(null=True)
    sizing_charges_rate = FloatField(null=True)
    sizing_charges_amount = FloatField(null=True)
    stc_charges_rate = FloatField(null=True)
    stc_charges_amount = FloatField(null=True)
    evac_facility_charge_rate = FloatField(null=True)
    evac_facility_charge_amount = FloatField(null=True)
    gst_comp_cess_rate = FloatField(null=True)
    gst_comp_cess_amount = FloatField(null=True)
    gross_bill_value_rate = FloatField(null=True)
    gross_bill_value_amount = FloatField(null=True)
    less_underloading_charges_rate = FloatField(null=True)
    less_underloading_charges_amount = FloatField(null=True)
    net_value_rate = FloatField(null=True)
    net_value_amount = FloatField(null=True)
    royalty_rate = FloatField(null=True)
    royalty_amount = FloatField(null=True)
    nmet_rate = FloatField(null=True)
    nmet_amount = FloatField(null=True)
    dmf_rate  = FloatField(null=True)
    dmf_amount = FloatField(null=True)
    cgst_rate = FloatField(null=True)
    cgst_amount = FloatField(null=True)
    sgst_rate = FloatField(null=True)
    sgst_amount = FloatField(null=True)
    # particulars end

    #total start

    total_tare_wt = FloatField(null=True)
    total_gross_wt = FloatField(null=True)
    total_net_wt = FloatField(null=True)
    total_ul_wt = FloatField(null=True) #underload
    total_ol_wt = FloatField(null=True) #overload


    #total end

    # wclrailinvoice end

    created_at = DateTimeField(default=datetime.datetime.utcnow)

    #
    # sap data start
    transport_code = StringField(null=True)
    transport_name = StringField(null=True)
    material_code = StringField(null=True)
    material_description = StringField(null=True)
    plant_code = StringField(null=True)
    storage_location = StringField(null=True)
    valuation_type = StringField(null=True)
    po_open_quantity = StringField(null=True)
    uom = StringField(null=True)
    # sap data end
    po_date = DateTimeField(null=True)
    meta = {"db_alias": "GMR_DB-alias", "collection": "sapRecordsRail"}


    def payload(self):
        return {
            "month": self.month,
            "rr_no": self.rr_no,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "rr_qty": self.rr_qty,
            "po_amount": self.po_amount,
            "sap_po": self.sap_po,
            "do_date": self.do_date,
            "line_item": self.line_item,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def anotherPayload(self):
        return {
            "month": self.month,
            "rr_no": self.rr_no,
            "rr_date": self.rr_date,
            "siding": self.siding,
            "mine": self.mine,
            "grade": self.grade,
            "rr_qty": self.rr_qty,
            "po_amount": self.po_amount,
            "sap_po": self.sap_po,
            "do_date": self.do_date,
            "line_item": self.line_item,
            "invoice_date": self.invoice_date,
            "invoice_no": self.invoice_no,
            "sale_date": self.sale_date,
            "sizing_charges": self.sizing_charges,
            "evac_facility_charge": self.evac_facility_charge,
            "royality_charges": self.royality_charges,
            "nmet_charges": self.nmet_charges,
            "dmf": self.dmf,
            "adho_sanrachna_vikas": self.adho_sanrachna_vikas,
            "pariyavaran_upkar": self.pariyavaran_upkar,
            "assessable_value": self.assessable_value,
            "igst": self.igst,
            "gst_comp_cess": self.gst_comp_cess,
            "gross_bill_value": self.gross_bill_value,
            "less_underloading_charges": self.less_underloading_charges,
            "net_value": self.net_value,
            "total_amount": self.total_amount,
            "transport_code": self.transport_code,
            "transport_name": self.transport_name,
            "material_code": self.material_code,
            "material_description": self.material_description,
            "plant_code": self.plant_code,
            "storage_location": self.storage_location,
            "valuation_type": self.valuation_type,
            "po_open_quantity": self.po_open_quantity,
            "uom": self.uom,
        }
    

class sapRecordsRCR(Document):
    rr_no = IntField(null=True)
    sap_po = IntField(null=True)
    rr_date = StringField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    month = DateTimeField(null=True)
    consumer_type = StringField(null=True)
    grade = StringField(null=True)
    mine = StringField(null=True)
    line_item = IntField(null=True)
    rr_qty = StringField(null=True)
    po_amount = FloatField(null=True)
    
    secl_mode_transport = StringField(null=True)
    area = StringField(null=True)
    secl_basic_price = FloatField(null=True)
    secl_sizing_charges = FloatField(null=True)
    secl_stc_charges = FloatField(null=True)
    secl_evac_facility_charges = FloatField(null=True)
    secl_royality_charges = FloatField(null=True)
    secl_nmet_charges = FloatField(null=True)
    secl_dmf = FloatField(null=True)
    secl_adho_sanrachna_vikas = FloatField(null=True)
    secl_pariyavaran_upkar = FloatField(null=True)
    secl_terminal_tax = FloatField(null=True)
    secl_assessable_tax = FloatField(null=True)
    secl_igst = FloatField(null=True)
    secl_gst_comp_cess = FloatField(null=True)
    sap_po = StringField(null=True)

    # sap data start
    transport_code = StringField(null=True)
    transport_name = StringField(null=True)
    material_code = StringField(null=True)
    material_description = StringField(null=True)
    plant_code = StringField(null=True)
    storage_location = StringField(null=True)
    valuation_type = StringField(null=True)
    po_open_quantity = StringField(null=True)
    uom = StringField(null=True)
    # sap data end
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    # id = IntField(min_value=1)

    meta = {"db_alias": "GMR_DB-alias", "collection": "sapRecordsRcr"}


    def payload(self):
        return {
            # "srno": str(self.id),
            "rr_no": self.rr_no,
            "rr_date": self.rr_date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "month": self.month,
            "consumer_type": self.consumer_type,
            "grade": self.grade,
            "mine": self.mine,
            "line_item": self.line_item,
            "rr_qty": self.rr_qty,
            "po_amount": self.po_amount,
            "sap_po": self.sap_po,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    

class rakeQuota(Document):
    ID = IntField(min_value=1)
    month = StringField(default=None)
    year = IntField(default=None)
    valid_upto = DateTimeField(default=None)
    coal_field =  StringField(default=None)
    rake_alloted = IntField(default=None)
    rake_received = StringField(default=None)
    due = StringField(default=None)
    grade = StringField(default=None)
    expected_rakes = DictField(null=True)
    source_type = StringField(null=True)
    cancelled_rakes = IntField(null=True)
    remarks = StringField(null=True)
    # created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_at = DateTimeField(default=None)


    meta = {"db_alias": "GMR_DB-alias", "collection": "rakeQuota"}

    def payload(self):
        return {
            "SrNo": self.ID,
            "month": self.month,
            "year": self.year,
            "valid_upto": self.valid_upto,
            "rake_alloted": self.rake_alloted,
            "rake_received": self.rake_received,
            "due": self.due,
            "expected_rakes": self.expected_rakes,
            "source_type": self.source_type,
            "cancelled_rakes": self.cancelled_rakes,
            "remarks": self.remarks,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    

class rcrrakeQuota(Document):
    ID = IntField(min_value=1)
    month = StringField(default=None)
    year = IntField(default=None)
    valid_upto = DateTimeField(default=None)
    coal_field =  StringField(default=None)
    rake_alloted = IntField(default=None)
    rake_received = StringField(default=None)
    due = StringField(default=None)
    grade = StringField(default=None)
    expected_rakes = DictField(null=True)
    source_type = StringField(null=True)
    cancelled_rakes = IntField(null=True)
    remarks = StringField(null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    
    meta = {"db_alias": "GMR_DB-alias", "collection": "rcrrakeQuota"}

    def payload(self):
        return {
            "SrNo": self.ID,
            "month": self.month,
            "year": self.year,
            "valid_upto": self.valid_upto,
            "rake_alloted": self.rake_alloted,
            "rake_received": self.rake_received,
            "due": self.due,
            "expected_rakes": self.expected_rakes,
            "source_type": self.source_type,
            "cancelled_rakes": self.cancelled_rakes,
            "remarks": self.remarks,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    

class RcrRoadData(Document):
    rrs_wt_date = DateTimeField(null=True)  
    grs_wt_time = StringField(null=True) 
    received_gross_weight = FloatField(null=True) 
    tar_wt_date = DateTimeField(null=True) 
    tar_wt_time = StringField(null=True) 
    received_tare_weight = FloatField(null=True)  
    received_net_weight = FloatField(null=True) 
    unloading_slip_number = StringField(null=True)
    vehicle_no = StringField(null=True)
    transporter = StringField(null=True)
    tp_number = IntField(null=True)
    do_number = IntField(null=True)
    mine = StringField(null=True)
    secl_delivery_challan_number = IntField(null=True)
    dc_gross_wt = FloatField(null=True)  
    dc_tare_wt = FloatField(null=True)  
    dc_net_wt = FloatField(null=True) 
    loading_date = DateTimeField(null=True) 
    out_time = StringField(null=True)
    lr_no = IntField(null=True)
    lr_date = DateTimeField(null=True)  
    sap_po = StringField(null=True)
    line_item = IntField(null=True)
    po_date = DateTimeField(null=True)
    do_date = DateTimeField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    slno = DateTimeField(null=True)
    type_consumer = StringField(null=True)
    grade = StringField(null=True)
    po_qty = IntField(null=True)
    po_amount = FloatField(null=True)
    
    rcr_file = StringField(null=True) # added by faizal for App on 20052025 1247
    grn_status = BooleanField(default=False)
    mine_invoice=StringField(null=True) #NEW ADD   #added on 30-05-2025 on 05:38pm
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {"db_alias": "GMR_DB-alias", "collection": "RcrRoadData"}


    def payload(self):
        return {
            "id": str(self.id),
            "grs_wt_date": self.rrs_wt_date,	
            "grs_wt_time": self.grs_wt_time,
            "received_gross_weight": self.received_gross_weight,
            "tar_wt_date": self.tar_wt_date,
            "tar_wt_time": self.tar_wt_time, 
            "received_tare_weight" : self.received_tare_weight,
            "received_net_weight": self.received_net_weight,	
            "unloading_slip_number": self.unloading_slip_number,
            "vehicle_no": self.vehicle_no,	
            "transporter": self.transporter,
            "tp_number": self.tp_number,	
            "do_number": self.do_number,	
            "mine": self.mine,	
            "secl_delivery_challan_number": self.secl_delivery_challan_number,	
            "dc_gross_wt": self.dc_gross_wt,
            "dc_tare_wt": self.dc_tare_wt,	
            "dc_net_wt": self.dc_net_wt,	
            "loading_date": self.loading_date,	
            "out_time": self.out_time,	
            "lr_no": self.lr_no,	
            "lr_date": self.lr_date,
            "sap_po": self.sap_po,
            "line_item": self.line_item,
            "po_date": self.po_date,
            "do_date": self.do_date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "slno": self.slno,
            "type_consumer": self.type_consumer,
            "grade": self.grade,
            "po_qty": self.po_qty,
            "po_amount": self.po_amount,
            "rcr_file": self.rcr_file,
            "grn_status": self.grn_status,
            "mine_invoice":self.mine_invoice, 
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    

#NEW 




    
class Grn(Document):
    do_no = StringField(null=True)
    invoice_date= StringField(null=True)
    invoice_no=StringField(null=True)
    sale_date = StringField(null=True)
    grade = StringField(null=True)
    dispatch_date = StringField(null=True)
    mine = StringField(null=True)    
    do_qty = StringField(null=True)
    # header_data = DictField()
    original_data = ListField(DictField())
    new_data = ListField(DictField())
    # approvals = ListField(DictField())
    approvals = DictField()
    changed_by = StringField(null=True)
    #raod data start
    #particulars start
    basic_price = FloatField(null=True)
    sizing_charges = FloatField(null=True)
    stc_charges = FloatField(null=True)
    evac_facility_charge = FloatField(null=True)
    royalty_charges = FloatField(null=True)
    nmet_charges = FloatField(null=True)
    imf = FloatField(null=True)
    cgst = FloatField(null=True)
    sgst = FloatField(null=True)
    gst_comp_cess = FloatField(null=True)
    gross_bill_value = FloatField(null=True)
    net_value = FloatField(null=True)
    total_amount = FloatField(null=True)
    #particulars end
    #raod data end
    mode = StringField(null=True)
    source_type = StringField(null=True) #rail
    type_consumer = StringField(null=True) #road
    rejected = BooleanField(default = False)
    posting_date = DateField()
    grn_no = StringField(null=True)
    lot_no = IntField(null=True)
    rake_no = IntField(null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    #rail data start
    # sizing_charges_rate=FloatField(null=True)
    sizing_charges_amount=FloatField(null=True)
    # evac_facility_charge_rate=FloatField(null=True)
    evac_facility_charge_amount=FloatField(null=True)
    # royalty_charges_rate=FloatField(null=True)
    royalty_charges_amount= FloatField(null=True)
    # nmet_rate=FloatField(null=True)
    nmet_amount=FloatField(null=True)
    # dmf_rate=FloatField(null=True)
    dmf_amount=FloatField(null=True)
    # adho_sanrachna_vikas_rate=FloatField(null=True)
    adho_sanrachna_vikas_amount=FloatField(null=True)
    # pariyavaran_upkar_rate=FloatField(null=True)
    pariyavaran_upkar_amount=FloatField(null=True)
    # assessable_value_rate=FloatField(null=True)
    assessable_value_amount=FloatField(null=True)
    # igst_rate=FloatField(null=True)
    igst_amount=FloatField(null=True)
    # gst_comp_cess_rate=FloatField(null=True)
    gst_comp_cess_amount=FloatField(null=True)
    # gross_bill_value_rate=FloatField(null=True)
    gross_bill_value_amount=FloatField(null=True)
    # less_underloading_charges_rate=FloatField(null=True)
    less_underloading_charges_amount=FloatField(null=True)
    # net_value_rate=FloatField(null=True)
    net_value_amount=FloatField(null=True)

    # total_gwel_net=FloatField(null=True)  #use for form15
    #rail data end

    grn_completed = BooleanField(default = False)
    extraction = StringField(null=True)

    meta = {"db_alias": "gmrDB-alias", "collection": "Grn"}

    def payload(self):
        return {
            "do_no": self.do_no,
            "invoice_date": self.invoice_date,
            "invoice_no": self.invoice_no,
            "sale_date": self.sale_date,
            "grade": self.grade,
            "dispatch_date": self.dispatch_date,
            "mine": self.mine,    
            "do_qty": self.do_qty,
            "original_data": self.original_data,
            "new_data": self.new_data,
            "approvals": self.approvals,
            "changed_by": self.changed_by,
            "mode": self.mode,
            "source_type": self.source_type, #rail
            "type_consumer": self.type_consumer, #road
            "net_value": self.net_value, #rail
            "total_amount": self.total_amount, #road
            "grn_type": self.extraction,
            "grn_no": self.grn_no,
            # "basic_price": self.basic_price,
            # "sizing_charges": self.sizing_charges,
            # "stc_charges": self.stc_charges,
            # "evac_facility_charge": self.evac_facility_charge,
            # "royalty_charges": self.royalty_charges,
            # "nmet_charges": self.nmet_charges,
            # "imf": self.imf,
            # "cgst": self.cgst,
            # "sgst": self.sgst,
            # "gst_comp_cess": self.gst_comp_cess,
            # "gross_bill_value": self.gross_bill_value,
            # "net_value": self.net_value,
            # "total_amount": self.total_amount,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
    
    def frpayload(self):
        if self.mode == "road":
            do_rr_no = "do_no"
        elif self.mode == "rail":
            do_rr_no ="rr_no"
        return {
            do_rr_no: self.do_no,
            "invoice_date": self.invoice_date,
            "invoice_no": self.invoice_no,
            "sale_date": self.sale_date,
            "grade": self.grade,
            "dispatch_date": self.dispatch_date,
            "mine": self.mine,    
            "do_qty": self.do_qty,
            "new_data": self.new_data,
            "grn_completed": self.grn_completed,
            "grn_type": self.extraction,
            "grn_no": self.grn_no,
            "posting_date": self.posting_date,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def finalPayload(self):
        if self.mode == "road":
            do_rr_no = "do_no"
        elif self.mode == "rail":
            do_rr_no ="rr_no"
        return {
            do_rr_no: self.do_no,
            "invoice_date": self.invoice_date,
            "invoice_no": self.invoice_no,
            "sale_date": self.sale_date,
            "grade": self.grade,
            "dispatch_date": self.dispatch_date,
            "mine": self.mine,    
            "do_qty": self.do_qty,
            "original_data": self.original_data,
            "new_data": self.new_data,
            "approvals": self.approvals,
            "changed_by": self.changed_by,
            "mode": self.mode,
            "source_type": self.source_type, #rail
            "type_consumer": self.type_consumer, #road
            "net_value": self.net_value, #rail
            "total_amount": self.total_amount, #road
            "basic_price": self.basic_price,
            "sizing_charges": self.sizing_charges,
            "stc_charges": self.stc_charges,
            "evac_facility_charge": self.evac_facility_charge,
            "royalty_charges": self.royalty_charges,
            "nmet_charges": self.nmet_charges,
            "imf": self.imf,
            "cgst": self.cgst,
            "sgst": self.sgst,
            "gst_comp_cess": self.gst_comp_cess,
            "gross_bill_value": self.gross_bill_value,
            "net_value": self.net_value,
            "total_amount": self.total_amount,
            "lot_no": self.lot_no,
            "rake_no": self.rake_no,
            "created_at": datetime.datetime.fromisoformat(
                    self.created_at.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "mode": self.mode,
            "source_type": self.source_type, #rail
            "type_consumer": self.type_consumer, #road
            "rejected": self.rejected,
            "sizing_charges_amount": self.sizing_charges_amount,
            "evac_facility_charge_amount": self.evac_facility_charge_amount,
            "royalty_charges_amount": self.royalty_charges_amount,
            "nmet_amount": self.nmet_amount,
            "dmf_amount": self.dmf_amount,
            "adho_sanrachna_vikas_amount": self.adho_sanrachna_vikas_amount,
            "pariyavaran_upkar_amount": self.pariyavaran_upkar_amount,
            "assessable_value_amount": self.assessable_value_amount,
            "igst_amount": self.igst_amount,
            "gst_comp_cess_amount": self.gst_comp_cess_amount,
            "gross_bill_value_amount": self.gross_bill_value_amount,
            "less_underloading_charges_amount": self.less_underloading_charges_amount,
            "net_value_amount": self.net_value_amount,
            "grn_type": self.extraction,
            "grn_no": self.grn_no,
            "lot_no": self.lot_no,
            "grn_completed": self.grn_completed,
            "extraction": self.extraction,
            "posting_date":  datetime.datetime.fromisoformat(
                    self.posting_date.strftime("%Y-%m-%d %H:%M:%S.%fZ")[:-1] + "+00:00"
                    ).astimezone(tz=to_zone).strftime("%Y-%m-%d %H:%M:%S") if self.posting_date else None,
        } 
