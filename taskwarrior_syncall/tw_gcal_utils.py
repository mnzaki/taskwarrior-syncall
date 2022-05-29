import traceback
from datetime import timedelta
from typing import List, Optional, Tuple
from uuid import UUID

from bubop import logger
from item_synchronizer.types import Item

from taskwarrior_syncall.google.gcal_side import GCalSide

_prefix_title_success_str = "✅"
_prefix_title_failed_str = "❌"

_failed_str = "FAIL"


def _already_has_prefix(gcal_item: Item) -> bool:
    return gcal_item["summary"].startswith(_prefix_title_success_str) or gcal_item[
        "summary"
    ].startswith(_prefix_title_failed_str)


def _add_task_prefix_if_not_present(gcal_item: Item):
    if _already_has_prefix(gcal_item):
        return
    if gcal_item["summary"].startswith(_failed_str):
        _add_failed_prefix(gcal_item)
    else:
        _add_success_prefix(gcal_item)


def _add_success_prefix(gcal_item: Item):
    gcal_item["summary"] = f'{_prefix_title_success_str}{gcal_item["summary"]}'


def _add_failed_prefix(gcal_item: Item):
    gcal_item[
        "summary"
    ] = f'{_prefix_title_failed_str}{gcal_item["summary"][len(_failed_str)+1:]}'


def convert_tw_to_gcal(tw_item: Item, prefer_scheduled_date: bool = False) -> Item:
    """TW -> GCal Converter.

    .. note:: Do not convert the ID as that may change either manually or
              after marking the task as "DONE"
    """
    assert all(
        i in tw_item.keys() for i in ("description", "status", "uuid")
    ), "Missing keys in tw_item"

    gcal_item = {}

    # Summary
    gcal_item["summary"] = tw_item["description"]
    if tw_item["status"] == "completed":
        _add_task_prefix_if_not_present(gcal_item=gcal_item)

    # description
    gcal_item["description"] = "IMPORTED FROM TASKWARRIOR\n"
    if "annotations" in tw_item.keys():
        for i, annotation in enumerate(tw_item["annotations"]):
            gcal_item["description"] += f"\n* Annotation {i + 1}: {annotation}"

    gcal_item["description"] += "\n"
    for k in ["status", "uuid"]:
        gcal_item["description"] += f"\n* {k}: {tw_item[k]}"

    date_keys = ["scheduled", "due"] if prefer_scheduled_date else ["due", "scheduled"]
    # Handle dates:
    # Walk through the date_keys using the first of them that's present in the item at hand.
    # For example if the prefered key is `scheduled` use the item["scheduled"] as the prefered
    # date and create an event with (start=scheduled, end=entry+1).
    # If the scheduled key is not found, do the same with the due key if that's found
    #
    # if none of the above keys work, use the entry key: (start=entry, end=entry+1)
    for date_key in date_keys:
        if date_key in date_keys:
            logger.trace(
                f'Using "{date_key}" date for {tw_item["uuid"]} for setting the end date of'
                " the event"
            )
            dt_gcal = GCalSide.format_datetime(tw_item[date_key])
            gcal_item["start"] = {
                "dateTime": GCalSide.format_datetime(tw_item[date_key] - timedelta(hours=1))
            }
            gcal_item["end"] = {"dateTime": dt_gcal}
            break
    else:
        logger.trace(
            f'Using "entry" date for {tw_item["uuid"]} for setting the start date of the event'
        )
        entry_dt = tw_item["entry"]
        entry_dt_gcal_str = GCalSide.format_datetime(entry_dt)

        gcal_item["start"] = {"dateTime": entry_dt_gcal_str}

        gcal_item["end"] = {
            "dateTime": GCalSide.format_datetime(entry_dt + timedelta(hours=1))
        }

    # update time
    if "modified" in tw_item.keys():
        gcal_item["updated"] = GCalSide.format_datetime(tw_item["modified"])

    return gcal_item


def convert_gcal_to_tw(gcal_item: Item, set_scheduled_date=False) -> Item:
    """GCal -> TW Converter.

    If set_scheduled_date, then it will set the "scheduled" date of the produced TW task
    instead of the "due" date
    """

    # Parse the description
    annotations, status, uuid = _parse_gcal_item_desc(gcal_item)
    assert isinstance(annotations, list)
    assert isinstance(status, str)
    assert isinstance(uuid, UUID) or uuid is None

    tw_item: Item = {}
    # annotations
    tw_item["annotations"] = annotations

    # alias - make aliases dict?
    if status == "done":
        status = "completed"

    # Status
    if status not in ["pending", "completed", "deleted", "waiting", "recurring"]:
        logger.error(
            "Invalid status {status} in GCal->TW conversion of item. Skipping status:"
        )
    else:
        tw_item["status"] = status

    # uuid - may just be created -, thus not there
    if uuid is not None:
        tw_item["uuid"] = uuid

    # Description
    gcal_summary = gcal_item["summary"]
    if gcal_summary.startswith(_prefix_title_success_str):
        gcal_summary = gcal_summary[len(_prefix_title_success_str) :]
    tw_item["description"] = gcal_summary

    # don't meddle with the 'entry' field
    if set_scheduled_date:
        date_key = "scheduled"
    else:
        date_key = "due"

    logger.debug(f'Setting TW {date_key} date for item {tw_item["uuid"]}')
    tw_item[date_key] = GCalSide.get_event_time(gcal_item, t="end")

    # update time
    if "updated" in gcal_item.keys():
        tw_item["modified"] = GCalSide.parse_datetime(gcal_item["updated"])

    # Note:
    # Don't add extra fields of GCal as TW annotations because then, if converted
    # backwards, these annotations are going in the description of the Gcal event and then
    # these are going into the event description and this happens on every conversion. Add
    # them as new TW UDAs if needed

    return tw_item


def _parse_gcal_item_desc(
    gcal_item: Item,
) -> Tuple[List[str], str, Optional[UUID]]:
    """Parse and return the necessary TW fields off a Google Calendar Item."""
    annotations: List[str] = []
    status = "pending"
    uuid = None

    if "description" not in gcal_item.keys():
        return annotations, status, uuid

    gcal_desc = gcal_item["description"]
    # strip whitespaces, empty lines
    lines = [line.strip() for line in gcal_desc.split("\n") if line][1:]

    # annotations
    i = 0
    for i, line in enumerate(lines):
        parts = line.split(":", maxsplit=1)
        if len(parts) == 2 and parts[0].lower().startswith("* annotation"):
            annotations.append(parts[1].strip())
        else:
            break

    if i == len(lines) - 1:
        return annotations, status, uuid

    # Iterate through rest of lines, find only the status and uuid ones
    for line in lines[i:]:
        parts = line.split(":", maxsplit=1)
        if len(parts) == 2:
            start = parts[0].lower()
            if start.startswith("* status"):
                status = parts[1].strip().lower()
            elif start.startswith("* uuid"):
                try:
                    uuid = UUID(parts[1].strip())
                except ValueError as err:
                    logger.error(
                        f'Invalid UUID "{err}" provided during GCal -> TW conversion,'
                        f" Using None...\n\n{traceback.format_exc()}"
                    )

    return annotations, status, uuid
