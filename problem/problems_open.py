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

def get_global_open_problems_by_severity(problems_from_api):
    mz_severity_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN":  
            management_zone_names = []
            for management_zone in problem['managementZones']:                
                mz_name = management_zone['name']
                management_zone_names.append(mz_name)
                problem_severity = "_".join(problem['severityLevel'].split())     
                if not mz_name in mz_severity_dict:
                    severity_dict = {}
                    severity_dict[problem_severity] = severity_dict.get(problem_severity, 0) + 1
                    new_dict = {mz_name : severity_dict}                    
                    mz_severity_dict.update(new_dict)
                else:
                    if not problem_severity in mz_severity_dict[mz_name]:
                        mz_severity_dict[mz_name][problem_severity] = mz_severity_dict[mz_name].get(problem_severity, 0) + 1
                    else:
                        mz_severity_dict[mz_name][problem_severity] = mz_severity_dict[mz_name][problem_severity] + 1
    return mz_severity_dict

def get_global_open_problems_by_title(problems_from_api):
    mz_title_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN":  
            management_zone_names = []
            for management_zone in problem['managementZones']:                
                mz_name = management_zone['name']
                management_zone_names.append(mz_name)       
                problem_title = "_".join(problem['title'].split())     
                if not mz_name in mz_title_dict:
                    title_dict = {}
                    title_dict[problem_title] = title_dict.get(problem_title, 0) + 1
                    new_dict = {mz_name : title_dict}                    
                    mz_title_dict.update(new_dict)
                else:
                    if not problem_title in mz_title_dict[mz_name]:
                        mz_title_dict[mz_name][problem_title] = mz_title_dict[mz_name].get(problem_title, 0) + 1
                    else:
                        mz_title_dict[mz_name][problem_title] = mz_title_dict[mz_name][problem_title] + 1
    return mz_title_dict
        
def get_global_open_problems_by_impact_level(problems_from_api):
    mz_impact_level_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN":  
            management_zone_names = []
            for management_zone in problem['managementZones']:                
                mz_name = management_zone['name']
                management_zone_names.append(mz_name)       
                problem_impact_level = "_".join(problem['impactLevel'].split()) 
                if not mz_name in mz_impact_level_dict:
                    impact_level_dict = {}
                    impact_level_dict[problem_impact_level] = impact_level_dict.get(problem_impact_level, 0) + 1
                    new_dict = {mz_name : impact_level_dict}                    
                    mz_impact_level_dict.update(new_dict)
                else:
                    if not problem_impact_level in mz_impact_level_dict[mz_name]:
                        mz_impact_level_dict[mz_name][problem_impact_level] = mz_impact_level_dict[mz_name].get(problem_impact_level, 0) + 1
                    else:
                        mz_impact_level_dict[mz_name][problem_impact_level] = mz_impact_level_dict[mz_name][problem_impact_level] + 1
    return mz_impact_level_dict

def get_global_open_problems_payloads_title(problems_from_api):
    global_open_problems_payloads = []
    global_open_problems_by_title = get_global_open_problems_by_title(problems_from_api)    
    for mz_name in global_open_problems_by_title:
        for title in global_open_problems_by_title[mz_name]:            
            payload = "dtapi.problem.open.global.per_title,dt.management_zone=\""+mz_name+"\",dt.title=\""+title+"\" "+ str(global_open_problems_by_title[mz_name][title])
            global_open_problems_payloads.append(payload)            
            logger.debug(payload)    
    return global_open_problems_payloads

def get_global_open_problems_payloads_impact_level(problems_from_api):
    global_open_problems_payloads = []
    global_open_problems_by_impact_level = get_global_open_problems_by_impact_level(problems_from_api)    
    for mz_name in global_open_problems_by_impact_level:
        for impact_level in global_open_problems_by_impact_level[mz_name]:            
            payload = "dtapi.problem.open.global.per_impact_level,dt.management_zone=\""+mz_name+"\",dt.impact_level=\""+impact_level+"\" "+ str(global_open_problems_by_impact_level[mz_name][impact_level])
            global_open_problems_payloads.append(payload)            
            logger.debug(payload)    
    return global_open_problems_payloads

def get_global_open_problems_payloads(problems_from_api):
    global_open_problems_payloads = []
    global_open_problems_by_severity = get_global_open_problems_by_severity(problems_from_api)    
    for mz_name in global_open_problems_by_severity:
        for severity in global_open_problems_by_severity[mz_name]: 
            severity_level = get_severity_level(severity)
            payload = "dtapi.problem.open.global,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" "+ str(global_open_problems_by_severity[mz_name][severity])
            global_open_problems_payloads.append(payload)            
            logger.debug(payload)    
    return global_open_problems_payloads

def get_mz_open_problems_by_severity(problems_from_api):
    mz_open_problems_by_severity = {}     
    for problem in problems_from_api:
        management_zone_names = []
        if problem['status'] == "OPEN":
            for management_zone in problem['managementZones']:                
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

def get_mz_open_problems_payloads(problems_from_api):    
    mz_open_problems_payloads = []
    mz_open_problems_by_severity = get_mz_open_problems_by_severity(problems_from_api)
    # Post problems in management zone split by severity    
    for mz_name in mz_open_problems_by_severity:
        for severity in mz_open_problems_by_severity[mz_name]:            
            severity_level = get_severity_level(severity)
            payload = "dtapi.problem.open.managementZone,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" "+str(mz_open_problems_by_severity[mz_name][severity])   
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
                payload = "dtapi.problem.open.managementZone,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" 0"
                mz_without_problems_payloads.append(payload)
                logger.debug(payload)
    return mz_without_problems_payloads



def get_open_problems_payloads(problems_from_api, all_management_zone_names):
    open_problems_payloads = []
    # Global    
    global_open_problems_payloads = get_global_open_problems_payloads(problems_from_api)
    # Global per title
    global_open_problems_payloads_title = get_global_open_problems_payloads_title(problems_from_api)
    # Global per impact
    global_open_problems_payloads_impact = get_global_open_problems_payloads_impact_level(problems_from_api)
    # Management Zones
    mz_open_problems_by_severity, mz_open_problems_payloads = get_mz_open_problems_payloads(problems_from_api)
    # Management Zones without problems    
    mz_without_problems_payloads = get_management_zones_without_problems_payloads(all_management_zone_names,mz_open_problems_by_severity)
    
    open_problems_payloads = open_problems_payloads + global_open_problems_payloads + global_open_problems_payloads_title + global_open_problems_payloads_impact + mz_open_problems_payloads + mz_without_problems_payloads

    return open_problems_payloads
