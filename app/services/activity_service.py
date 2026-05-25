from app.schemas.activity import ActivityCreate, ActivityRead, Activity

activities: dict[int, Activity] = {}
next_activity_id: int = 1

def create_activity(data: ActivityCreate) -> Activity:
    global next_activity_id

    activity = Activity(
        id=next_activity_id,
        name=data.name,
    )

    activities[activity.id] = activity
    next_activity_id += 1

    return activity

def get_activities() -> list[ActivityRead]:
    return list(activities.values())

def get_activity(activity_id: int) -> ActivityRead | None:
    return activities.get(activity_id)