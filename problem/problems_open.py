import logging

logger = logging.getLogger(__name__)

def get_severity_dict_template():
    severity_dict_template = {
        "AVAILABILITY"  : 0,
        "ERROR"         : 0,
        "PERFORMANCE"   : 0,
        "RESOURCE_CONTENTION" : 0,
        "CUSTOM_ALERT"  :0
    }
    return severity_dict_template


def get_severity_level(severity):
    if severity == "AVAILABILITY":
        return 1
    if severity == "ERROR":
        return 2
    if severity == "PERFORMANCE":
        return 3
    if severity == "RESOURCE_CONTENTION":
        return 4
    if severity == "CUSTOM_ALERT":
        return 5
    return 6

def get_mz_open_problems_by_severity(problems_from_api, problems_from_file):

    local_problem_ids = []
    for problem in problems_from_file:        
        local_problem_ids.append(problem['displayId']) 

    mz_open_problems_by_severity = {}     
    for problem in problems_from_api:
        management_zone_names = []
        if problem['status'] == "OPEN" and not problem['displayId'] in local_problem_ids:
            mzs = problem['managementZones']
            if len(mzs) == 0:
                mzs = {"name": "NONE_MZ"}
            for management_zone in mzs:                
                mz_name = management_zone['name']
                management_zone_names.append(mz_name)            
                if not mz_name in mz_open_problems_by_severity:
                    severity_dict = get_severity_dict_template()
                    severity_dict[problem['severityLevel']] = severity_dict[problem['severityLevel']] + 1
                    new_dict = {mz_name : severity_dict}                    
                    mz_open_problems_by_severity.update(new_dict)
                else:                    
                    mz_open_problems_by_severity[mz_name][problem['severityLevel']] = mz_open_problems_by_severity[mz_name] [problem['severityLevel']] + 1
    return mz_open_problems_by_severity

def get_mz_open_problems_payloads(problems_from_api, problems_from_file):    
    mz_open_problems_payloads = []
    mz_open_problems_by_severity = get_mz_open_problems_by_severity(problems_from_api, problems_from_file)
    # Post problems in management zone split by severity    
    for mz_name in mz_open_problems_by_severity:
        for severity in mz_open_problems_by_severity[mz_name]:            
            severity_level = get_severity_level(severity)
            payload = "dtapi.problem.open.managementZone,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" count,delta="+str(mz_open_problems_by_severity[mz_name][severity])   
            mz_open_problems_payloads.append(payload)
            logger.debug(payload)
    return mz_open_problems_by_severity, mz_open_problems_payloads

def get_management_zones_without_problems_payloads(all_management_zone_names,mz_open_problems_by_severity):     
    mz_without_problems_payloads = []
    management_zones_with_problems = []
    management_zones_without_problems = []
    for mz_name in mz_open_problems_by_severity:
        management_zones_with_problems.append(mz_name)
        
    for mz_name in all_management_zone_names:
        if not mz_name in management_zones_with_problems:
            management_zones_without_problems.append(mz_name)
            severity_dict = get_severity_dict_template()
            for severity in severity_dict:
                severity_level = get_severity_level(severity)
                payload = "dtapi.problem.open.managementZone,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" count,delta=0"
                mz_without_problems_payloads.append(payload)
                logger.debug(payload)
    return mz_without_problems_payloads



def get_open_problems_payloads(problems_from_api, all_management_zone_names, problems_from_file):
    open_problems_payloads = []
    # Global    
    #global_open_problems_payloads = get_global_open_problems_payloads(problems_from_api)
    # Global per title
    # global_open_problems_payloads_title = get_global_open_problems_payloads_title(problems_from_api)
    # Global per impact
    #global_open_problems_payloads_impact = get_global_open_problems_payloads_impact_level(problems_from_api)
    # Management Zones
    mz_open_problems_by_severity, mz_open_problems_payloads = get_mz_open_problems_payloads(problems_from_api, problems_from_file)
    # Management Zones without problems    
    mz_without_problems_payloads = get_management_zones_without_problems_payloads(all_management_zone_names,mz_open_problems_by_severity)
    
    open_problems_payloads = mz_without_problems_payloads

    return open_problems_payloads
