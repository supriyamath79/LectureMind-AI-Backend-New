progress = {
    "step": "Idle",
    "progress": 0
}


def update_progress(step, progress_value):
    global progress

    progress["step"] = step
    progress["progress"] = progress_value


def get_progress():
    return progress