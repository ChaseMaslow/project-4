"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


min_speeds = { 60: 20, 600: 15, 1000: 11.428, 1300: 13.333 }
max_speeds = { 200: 34, 400: 32, 600: 30, 1000: 28, 1300: 26 }

time_limits = { 200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75 }

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    
    t = [0, 0]
    dist = divmod(control_dist_km, 1)[0]
    cut = 0
    for bracket, speed in max_speeds.items():
        if dist <= bracket:
            q = divmod((dist - cut) / speed, 1)
            t[0] += q[0]
            t[1] += q[1]
            break
        elif bracket == brevet_dist_km:
            q = divmod((bracket - cut) / speed, 1)
            t[0] += q[0]
            t[1] += q[1]
            break
        else:
            q = divmod((bracket - cut) / speed, 1)
            t[0] += q[0]
            t[1] += q[1]
            cut = bracket

    rt = brevet_start_time.shift(hours=+t[0], minutes=+round(t[1]*60, 0))
    
    return rt


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    
    t = [0, 0]
    
    if control_dist_km >= brevet_dist_km:
        for bracket, limit in time_limits.items():
            if bracket == brevet_dist_km:
                t = divmod(limit, 1)
                break
    
    if control_dist_km < brevet_dist_km or t == [0, 0]:
        dist = divmod(control_dist_km, 1)[0]
        cut = 0
        for bracket, speed in min_speeds.items():
            if dist <= bracket:
                q = divmod((dist - cut) / speed, 1)
                t[0] += q[0]
                t[1] += q[1]
                if bracket == 60:
                    t[0] += 1
                break
            else:
                q = divmod((bracket - cut) / speed, 1)
                t[0] += q[0]
                t[1] += q[1]
                if bracket == 60:
                    t[0] += 1
                cut = bracket

    rt = brevet_start_time.shift(hours=+t[0], minutes=+round(t[1]*60, 0))
    
    return rt
