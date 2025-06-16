import datetime,calendar,os
from datetime import timedelta
from mongoengine import Q
from api.service.models import rakeQuota, RailData
from api.service.helpers import helpers
from api.service.serializers import rakeQuotaUpdate
from collections import defaultdict
from fastapi import HTTPException

class CoalJourneyRailRake:
    
    def __init__(self):
        pass
    
    def convert_to_date(self,month_str):
        try:
            return datetime.datetime.strptime(month_str, "%b-%Y")
        except Exception as e:
            helpers.error_handler(e)

    def coal_journey_rail_rake_quota_pending(self, currentPage, perPage, start_timestamp, end_timestamp):
        try:
            pending_filters = Q()
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

            page_no = result["page_no"]
            page_size = result["page_size"]
            offset = (page_no - 1) * page_size

            try:
                if start_timestamp:
                    pending_filters &= Q(created_at__gte=helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M", "Asia/Kolkata", False))
                if end_timestamp:
                    pending_filters &= Q(created_at__lte=helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M", "Asia/Kolkata", False))
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
            
            # Load all matching logs first (for accurate filtered count)
            try:
                all_logs = rakeQuota.objects(pending_filters).order_by("-year", "-month")
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing rakeQuota")
            
            if not all_logs:
                return result

            # Prepare reused values
            today = datetime.datetime.now()
            today_utc = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0)
            end_of_day_utc = today_utc + timedelta(hours=23, minutes=59, seconds=59)
            start_month = today.replace(day=1)
            _, end_day = calendar.monthrange(today.year, today.month)
            end_month = today.replace(day=end_day, hour=23, minute=59, second=59)
            current_month_str = today.strftime('%b-%Y')

            list_data = []

            for log in all_logs:
                month_str = log.month
                year = log.year
                month_year = f"{year}-{month_str[:2].upper()}"
                formatted_date = datetime.datetime.strptime(month_year, "%Y-%m").strftime("%Y-%m")

                def count_rail_data(**kwargs):
                    try:
                        return RailData.objects.filter(**kwargs).count()
                    except Exception:
                        raise HTTPException(status_code=500, detail="Error processing RailData")
                    
                def get_expected_rakes(log):
                    return (
                        list(log.expected_rakes.keys())[0],
                        list(log.expected_rakes.values())[0]
                    ) if log.expected_rakes else (0, 0)

                expected_date, expected_value = get_expected_rakes(log)

                rakes_received = count_rail_data(
                    month__icontains=formatted_date,
                    avery_placement_date__ne=None,
                    source_type__iexact=log.source_type
                )

                cancelled = int(log.cancelled_rakes or 0)
                rake_alloted = int(log.rake_alloted)
                balance = rake_alloted - rakes_received - cancelled

                rakes_loaded_till_date = count_rail_data(
                    month__icontains=formatted_date,
                    source_type__iexact=log.source_type
                )

                rakes_received_today = count_rail_data(
                    month__icontains=formatted_date,
                    avery_placement_date__gte=today_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    avery_placement_date__lte=end_of_day_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    source_type__iexact=log.source_type
                )

                rakes_loaded_today = count_rail_data(
                    drawn_date__gte=today_utc,
                    drawn_date__lte=end_of_day_utc,
                    month__icontains=formatted_date,
                    source_type__iexact=log.source_type
                )

                rakes_prev_month_received = count_rail_data(
                    month__icontains=formatted_date,
                    avery_placement_date__gte=f"{start_month.date()} 00:00:00",
                    avery_placement_date__lte=f"{end_month.date()} 23:59:59",
                    source_type__iexact=log.source_type
                )

                entry = {
                    "month": datetime.datetime.strptime(log.month, "%m-%Y").strftime("%b-%Y"),
                    "source_type": log.source_type or "",
                    "rake_planned_for_the_month": rake_alloted,
                    "cancelled_rakes": cancelled,
                    "remarks": log.remarks or "",
                    "expected_rakes_date": expected_date,
                    "expected_rakes_value": expected_value,
                    "rakes_previous_month_quota_received": rakes_prev_month_received,
                    "rakes_loaded_till_date": rakes_loaded_till_date,
                    "rakes_loaded_on_date": rakes_loaded_today,
                    "rakes_received_on_date": rakes_received_today,
                    "total_rakes_received_for_month": rakes_received,
                    "balance_rakes_to_receive": balance,
                    "no_of_rakes_in_transist": rakes_loaded_till_date - rakes_received,
                }

                entry['date_obj'] = self.convert_to_date(entry['month'])
                list_data.append(entry)

            # Sort and filter
            list_data.sort(key=lambda x: x['date_obj'])
            for item in list_data:
                del item['date_obj']

            pending_filtered_data = [entry for entry in list_data if entry['balance_rakes_to_receive'] > 0]
            result["count"]["pending"] = len(pending_filtered_data)  # Total count after filtering

            pending_filtered_data.reverse()

            # Set current month's previous month quota to 0
            for entry in pending_filtered_data:
                if entry['month'] == current_month_str:
                    entry['rakes_previous_month_quota_received'] = 0

            # Pagination AFTER filtering
            pending_paginated_data = pending_filtered_data[offset:offset + page_size]
            completed_paginated_data = list_data[offset:offset + page_size]

            # Totals
            totals = defaultdict(int)
            for record in pending_filtered_data:
                for key in ['rakes_previous_month_quota_received', 'rake_planned_for_the_month',
                            'rakes_loaded_till_date', 'rakes_loaded_on_date', 'rakes_received_on_date',
                            'total_rakes_received_for_month', 'balance_rakes_to_receive',
                            'no_of_rakes_in_transist', 'expected_rakes_value']:
                    totals[key] += int(record.get(key, 0))

            dataList = {
                "data": pending_paginated_data,
                "rake_total": dict(totals)
            }

            result.update({
                "labels": list(pending_paginated_data[0].keys()) if pending_paginated_data else [],
                "datasets": dataList,
            })

            result["count"] = {
                "pending": len(pending_filtered_data),
                "completed": len(list_data)
            }

            return result

        except Exception as e:
            helpers.error_handler(e)
            raise e

    def coal_journey_rail_rake_quota_completed(self, currentPage, perPage, start_timestamp, end_timestamp):
        try:
            completed_filters = Q()
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

            page_no = result["page_no"]
            page_size = result["page_size"]
            offset = (page_no - 1) * page_size

            # Apply time filters
            try:
                if start_timestamp:
                    completed_filters &= Q(created_at__gte=helpers.convert_to_utc_format(start_timestamp, "%Y-%m-%dT%H:%M", "Asia/Kolkata", False))
                if end_timestamp:
                    completed_filters &= Q(created_at__lte=helpers.convert_to_utc_format(end_timestamp, "%Y-%m-%dT%H:%M", "Asia/Kolkata", False))
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid date format")
            try:
                all_logs = rakeQuota.objects(completed_filters).order_by("-year", "-month")
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing rakeQuota")
            
            if not all_logs:
                return result

            today = datetime.datetime.utcnow()
            start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + datetime.timedelta(hours=23, minutes=59, seconds=59)

            list_data = []

            for log in all_logs:
                year = log.year
                month = int(log.month[:2])
                formatted_month = f"{year}-{month:02d}"

                base_filter = {
                    "month__icontains": formatted_month,
                    "source_type__iexact": log.source_type
                }

                rake_alloted = int(log.rake_alloted or 0)
                cancelled_rakes = int(log.cancelled_rakes or 0)
                expected_date = list(log.expected_rakes.keys())[0] if log.expected_rakes else 0
                expected_value = list(log.expected_rakes.values())[0] if log.expected_rakes else 0

                total_received = RailData.objects.filter(
                    **base_filter,
                    avery_placement_date__ne=""
                ).count()

                rakes_previous_month = RailData.objects.filter(
                    **base_filter,
                    avery_placement_date__gte=start_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                    avery_placement_date__lte=end_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                ).count()

                loaded_till_date = RailData.objects.filter(**base_filter).count()

                rakes_received_on_date = RailData.objects.filter(
                    **base_filter,
                    avery_placement_date__gte=start_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                    avery_placement_date__lte=end_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                ).count()

                rakes_loaded_on_date = RailData.objects.filter(
                    **base_filter,
                    drawn_date__gte=start_of_day,
                    drawn_date__lte=end_of_day,
                ).count()

                balance = rake_alloted - total_received - cancelled_rakes

                dict_data = {
                    "month": datetime.datetime.strptime(log.month, "%m-%Y").strftime("%b-%Y"),
                    "source_type": log.source_type or "",
                    "rake_planned_for_the_month": rake_alloted,
                    "cancelled_rakes": cancelled_rakes,
                    "remarks": log.remarks or "",
                    "expected_rakes_date": expected_date,
                    "expected_rakes_value": expected_value,
                    "total_rakes_received_for_month": total_received,
                    "balance_rakes_to_receive": balance,
                    "rakes_previous_month_quota_received": rakes_previous_month,
                    "rakes_loaded_till_date": loaded_till_date,
                    "rakes_received_on_date": rakes_received_on_date,
                    "rakes_loaded_on_date": rakes_loaded_on_date,
                    "no_of_rakes_in_transist": loaded_till_date - total_received
                }

                dict_data["date_obj"] = self.convert_to_date(dict_data["month"])
                list_data.append(dict_data)

            # Sort
            list_data.sort(key=lambda x: x["date_obj"])
            for item in list_data:
                del item["date_obj"]

            pending_filtered_data = [entry for entry in list_data if entry['balance_rakes_to_receive'] > 0]
            result["count"]["pending"] = len(pending_filtered_data)  # Total count after filtering

            # Count before pagination
            result["count"] = len(list_data)

            # Pagination
            completed_paginated_data = list_data[offset:offset + page_size]

            # Reset previous month quota for current month
            current_month = datetime.datetime.now().strftime('%b-%Y')
            for entry in completed_paginated_data:
                if entry["month"] == current_month:
                    entry["rakes_previous_month_quota_received"] = 0

            # Totals from all records (not paginated subset)
            totals = {
                'rakes_previous_month_quota_received': 0,
                'rake_planned_for_the_month': 0,
                'rakes_loaded_till_date': 0,
                'rakes_loaded_on_date': 0,
                'rakes_received_on_date': 0,
                'total_rakes_received_for_month': 0,
                'balance_rakes_to_receive': 0,
                'no_of_rakes_in_transist': 0,
                'expected_rakes_value': 0,
            }

            for record in list_data:
                for key in totals:
                    totals[key] += int(record.get(key, 0))

            result.update({
                "labels": list(completed_paginated_data[0].keys()) if completed_paginated_data else [],
                "datasets": {"data": completed_paginated_data, "rake_total": totals},
            })

            result["count"] = {
                "pending": len(pending_filtered_data),
                "completed": len(list_data)
            }
            
            return result

        except Exception as e:
            helpers.error_handler(e)
            raise e

    
    def coal_journey_rail_rake_quota_update(self,data:rakeQuotaUpdate):
        try:
            payload = data.dict()
            try:
                fetchrakeQuota = rakeQuota.objects(month=datetime.datetime.strptime(payload.get("month"), "%b-%Y").strftime("%d-%m-%Y"), source_type=payload.get("source_type"))
            except Exception:
                raise HTTPException(status_code=500, detail="Error processing rakeQuota")
            if fetchrakeQuota:
                fetchrakeQuota.update(rake_alloted=str(payload.get("rakes_planned_for_month")), expected_rakes=payload.get("expected_rakes") if payload.get("expected_rakes") != "" else None, source_type=payload.get("source_type") if payload.get("source_type") != "" else None, cancelled_rakes=payload.get("cancelled_rakes") if payload.get("cancelled_rakes") != "" else None, remarks=payload.get("remarks") if payload.get("remarks") != "" else None)
            
            return {"details": "success"}
        
        except Exception as e:
            helpers.error_handler(e)

coal_journey_rail_rake_quota=CoalJourneyRailRake()