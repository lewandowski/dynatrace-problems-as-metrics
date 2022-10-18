import logging

logger = logging.getLogger(__name__)

def get_minutes(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return minutes

def get_problem_ttr_payloads(problems_from_api, problems_from_file):
    local_problem_id_status = {}
    for problem in problems_from_file:
        new_dict = {problem['displayId'] : problem['status']}
        local_problem_id_status.update(new_dict)
    
    problem_ttr_payloads=[]    
    for problem in problems_from_api:        
        if problem['status'] == "CLOSED": 
            display_id = problem['displayId']
            if display_id in local_problem_id_status and local_problem_id_status[display_id] == "OPEN":
                time_to_repair_ms = problem['endTime'] - problem['startTime']
                time_to_repair_mins = get_minutes(time_to_repair_ms)
                severity = problem['severityLevel']
                severity_level = get_severity_level(severity)
                payload = "dtapi.problem.ttr.global,severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" " + str(time_to_repair_mins)
                logger.debug(payload)                               
                problem_ttr_payloads.append(payload)
                mzs = problem['managementZones']
                if len(mzs) == 0:
                    mzs = {"name": "NONE_MZ"}
                for management_zone in mzs:   
                    mz_name = management_zone['name']
                    payload_mz = "dtapi.problem.ttr.managementZone,dt.management_zone=\""+mz_name+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" "+ str(time_to_repair_mins)                    
                    logger.debug(payload_mz)
                    problem_ttr_payloads.append(payload_mz)
                # for management_zone in problem['managementZones']:
                #problem_title_raw = problem['title'].split()
                #problem_title = "_".join(problem_title_raw)
                #payload_problem = "dtapi.problem.ttr.title,dt.title=\""+problem_title+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" "+ str(time_to_repair_mins)                    
                #logger.debug(payload_problem)
                #logger.info("PAYLOAD PROBLEM :"+ payload_problem)
                #problem_ttr_payloads.append(payload_problem)
                #problem_impact_level_raw = problem['impactLevel'].split()
                #problem_impact_level = "_".join(problem_impact_level_raw)
                #payload_problem_impact_level = "dtapi.problem.ttr.impact_level,dt.impact_level=\""+problem_impact_level+"\",severity=\""+severity+"\",severity_level=\""+str(severity_level)+"\" "+ str(time_to_repair_mins)                    
                #logger.debug(payload_problem_impact_level)
                #logger.info("PAYLOAD PROBLEM :"+ payload_problem)
                #problem_ttr_payloads.append(payload_problem_impact_level)
    return problem_ttr_payloads    

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