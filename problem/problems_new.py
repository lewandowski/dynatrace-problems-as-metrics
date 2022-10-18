
import logging

logger = logging.getLogger(__name__)

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

def get_new_problems_payloads(problems_from_api, problems_from_file):
    # Global per title
    global_open_problems_payloads_title = get_global_open_problems_payloads_title(problems_from_api, problems_from_file)

    global_open_problems_payloads = get_new_problems_payloads_global(problems_from_api, problems_from_file)
    #def get_open_problems_payloads(problems_from_api, all_management_zone_names):
    
    global_open_problems_payloads_impact = get_global_open_problems_payloads_impact_level(problems_from_api, problems_from_file)

    global_open_problems_payloads_severity = get_global_open_problems_payloads_severity(problems_from_api, problems_from_file)

    new_problems_payloads = []
    new_problems_payloads = global_open_problems_payloads + global_open_problems_payloads_title + global_open_problems_payloads_impact + global_open_problems_payloads_severity

    return new_problems_payloads

def get_new_problems_payloads_global(problems_from_api, problems_from_file):
    # global_new_problems_by_severity = get_severity_dict_template()
    local_problem_ids = []
    for problem in problems_from_file:        
        local_problem_ids.append(problem['displayId'])        
    
    global_new_problem_count = 0
    mz_problem_count_dict = {}
    new_problem_payloads = []
    for problem in problems_from_api:
        if problem['status'] == "OPEN" and not problem['displayId'] in local_problem_ids:
            global_new_problem_count += 1      
            mzs = problem['managementZones']
            if len(mzs) == 0:
                mzs = {"name": "NONE_MZ"}
            for management_zone in mzs:          
                mz_name = management_zone['name']
                if not mz_name in mz_problem_count_dict:
                    new_dict = {mz_name : 1}
                    mz_problem_count_dict.update(new_dict)
                else:
                    mz_problem_count_dict[mz_name] = mz_problem_count_dict[mz_name] + 1

    payload_global = "dtapi.problem.open.new.global count,delta="+ str(global_new_problem_count)
    new_problem_payloads.append(payload_global)

    for mz_name in mz_problem_count_dict:
        payload_mz = "dtapi.problem.open.new.managementZone,dt.management_zone=\""+mz_name+"\" count,delta="+ str(mz_problem_count_dict[mz_name])
        new_problem_payloads.append(payload_mz)

    return new_problem_payloads

def get_global_open_problems_payloads_title(problems_from_api, problems_from_file):
    global_open_problems_payloads = []
    global_open_problems_by_title = get_global_open_problems_by_title(problems_from_api, problems_from_file)    
    for mz_name in global_open_problems_by_title:
        for title in global_open_problems_by_title[mz_name]:            
            payload = "dtapi.problem.open.global.per_title,dt.management_zone=\""+mz_name+"\",dt.title=\""+title+"\" count,delta="+ str(global_open_problems_by_title[mz_name][title])
            global_open_problems_payloads.append(payload)            
            logger.debug(payload)    
    return global_open_problems_payloads        

def get_global_open_problems_by_title(problems_from_api, problems_from_file):
    local_problem_ids = []
    for problem in problems_from_file:        
        local_problem_ids.append(problem['displayId']) 

    mz_title_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN" and not problem['displayId'] in local_problem_ids:
            management_zone_names = []
            mzs = problem['managementZones']
            if len(mzs) == 0:
                mzs = {"name": "NONE_MZ"}
            for management_zone in mzs:   
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
    
def get_global_open_problems_by_impact_level(problems_from_api, problems_from_file):

    local_problem_ids = []
    for problem in problems_from_file:        
        local_problem_ids.append(problem['displayId']) 

    mz_impact_level_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN" and not problem['displayId'] in local_problem_ids:
            management_zone_names = []
            mzs = problem['managementZones']
            if len(mzs) == 0:
                mzs = {"name": "NONE_MZ"}
            for management_zone in mzs:   
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

def get_global_open_problems_payloads_impact_level(problems_from_api, problems_from_file):
    global_open_problems_payloads = []
    global_open_problems_by_impact_level = get_global_open_problems_by_impact_level(problems_from_api, problems_from_file)    
    for mz_name in global_open_problems_by_impact_level:
        for impact_level in global_open_problems_by_impact_level[mz_name]:            
            payload = "dtapi.problem.open.global.per_impact_level,dt.management_zone=\""+mz_name+"\",dt.impact_level=\""+impact_level+"\" count,delta="+ str(global_open_problems_by_impact_level[mz_name][impact_level])
            global_open_problems_payloads.append(payload)            
            logger.debug(payload)    
    return global_open_problems_payloads

def get_global_open_problems_by_severity(problems_from_api, problems_from_file):
    local_problem_ids = []
    for problem in problems_from_file:        
        local_problem_ids.append(problem['displayId']) 

    mz_severity_dict = {}
    for problem in problems_from_api:
        if problem['status'] == "OPEN" and not problem['displayId'] in local_problem_ids: 
            management_zone_names = []
            mzs = problem['managementZones']
            if len(mzs) == 0:
                mzs = {"name": "NONE_MZ"}
            for management_zone in mzs:                
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

def get_global_open_problems_payloads_severity(problems_from_api, problems_from_file):
    global_open_problems_payloads = []
    global_open_problems_by_severity = get_global_open_problems_by_severity(problems_from_api, problems_from_file)    
    for mz_name in global_open_problems_by_severity:
        for severity in global_open_problems_by_severity[mz_name]: 
            severity_level = get_severity_level(severity)
            payload = "dtapi.problem.open.global,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" count,delta="+ str(global_open_problems_by_severity[mz_name][severity])
            global_open_problems_payloads.append(payload)            
            logger.debug(payload)    
    return global_open_problems_payloads