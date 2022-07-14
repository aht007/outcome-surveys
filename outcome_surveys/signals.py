"""
outcome_surveys signals.
"""
from datetime import timedelta
from logging import getLogger

from django.utils import timezone

from outcome_surveys.constants import SEGMENT_LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE
from outcome_surveys.models import LearnerCourseEvent

log = getLogger(__name__)


def schedule_course_passed_first_time_follow_up_segment_event(
    sender,
    user_id,
    course_id,
    event_properties,
    **kwargs  # pylint: disable=unused-argument
):
    """
    Listen for a `SCHEDULE_FOLLOW_UP_SEGMENT_EVENT_FOR_COURSE_PASSED_FIRST_TIME` signal.

    The incoming signal indicates that the segment event has fired
    for a learner who has passed a course for the first time.
    """
    log.info("[OUTCOME SURVEYS] Follow up signal recieved.")

    # add event data into model
    ninety_day_follow_up_date = timezone.now().date() + timedelta(days=90)
    LearnerCourseEvent.objects.create(
        user_id=user_id,
        course_id=course_id,
        data=event_properties,
        follow_up_date=ninety_day_follow_up_date,
        event_type=SEGMENT_LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE
    )

    log.info(
        "[OUTCOME SURVEYS] Follow up event scheduled. User: [%s], Course: [%s], Enrollment: [%s]",
        user_id,
        course_id,
        event_properties['LMS_ENROLLMENT_ID']
    )
