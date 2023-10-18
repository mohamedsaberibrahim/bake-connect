from datetime import datetime, timedelta

def find_available_time_slots(busy_slots, start_time, end_time):
    available_slots = []
    last_end_time = start_time
    
    for slot in busy_slots:
        if slot[0] > last_end_time:
            duration = (slot[0] - last_end_time).total_seconds() / 60
            available_slots.append((last_end_time, slot[0], duration))
        last_end_time = max(last_end_time, slot[1])
    
    if last_end_time < end_time:
        duration = (end_time - last_end_time).total_seconds() / 60
        available_slots.append((last_end_time, end_time, duration))
    
    return available_slots

def get_available_ready_times(available_slots, request_duration):
    available_ready_times = []

    for slot in available_slots:
        slot_start, slot_end, slot_duration = slot
        if slot_duration >= request_duration:
            while slot_start + timedelta(minutes=request_duration) <= slot_end:
                ready_time = slot_start + timedelta(minutes=request_duration)
                available_ready_times.append(ready_time.strftime("%H:%M"))
                slot_start = ready_time

    return available_ready_times
