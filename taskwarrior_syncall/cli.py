"""CLI argument functions - reuse across your apps.

This module will be loaded regardless of extras - don't put something here that requires an
extra dependency.
"""
import click

from taskwarrior_syncall.app_utils import name_to_resolution_strategy_type
from taskwarrior_syncall.constants import COMBINATION_FLAGS


def opt_default_duration_event_mins():
    return click.option(
        "--default-event-duration-mins",
        "default_event_duration_mins",
        default=30,
        type=int,
        help=(
            f"The default duration of an event that is to be created on Google Calendar [in"
            f" minutes]"
        ),
    )


def opt_prefer_scheduled_date():
    return click.option(
        "--prefer-scheduled-date",
        "prefer_scheduled_date",
        is_flag=True,
        help=(
            f'Prefer using the "scheduled" date field instead of the "due" date if the former'
            f" is available"
        ),
    )


def opt_list_combinations(name_A: str, name_B: str):
    return click.option(
        "--list-combinations",
        "do_list_combinations",
        is_flag=True,
        help=f"List the available named {name_A}<->{name_B} combinations",
    )


def opt_tw_tags():
    return click.option(
        "-t",
        "--taskwarrior-tags",
        "tw_tags",
        type=str,
        help="Taskwarrior tags to synchronize",
        multiple=True,
    )


def opt_tw_project():
    return click.option(
        "-p",
        "--tw-project",
        "tw_project",
        type=str,
        help="Taskwarrior project to synchronize",
    )


def opt_filesystem_root():
    return click.option(
        "--fs",
        "--fs-root",
        "filesystem_root",
        required=False,
        type=str,
        help="Directory to consider as root for synchronization operations",
    )


def opt_resolution_strategy():
    return click.option(
        "-r",
        "--resolution-strategy",
        default="AlwaysSecondRS",
        type=click.Choice(list(name_to_resolution_strategy_type.keys())),
        help="Resolution strategy to use during conflicts",
    )


def opt_combination(name_A: str, name_B: str):
    return click.option(
        COMBINATION_FLAGS[0],
        COMBINATION_FLAGS[1],
        "combination_name",
        type=str,
        help=f"Name of an already saved {name_A}<->{name_B} combination",
    )


def opt_custom_combination_savename(name_A: str, name_B: str):
    return click.option(
        "-s",
        "--save-as",
        "custom_combination_savename",
        type=str,
        help=(
            f"Save the given {name_A}<->{name_B} filters combination using a specified custom"
            " name."
        ),
    )


def opt_notion_page_id():
    return click.option(
        "-n",
        "--notion-page",
        "notion_page_id",
        type=str,
        help="Page ID of the Notion page to synchronize",
    )


def opt_notion_token_pass_path():
    return click.option(
        "--token",
        "--token-pass-path",
        "token_pass_path",
        help="Path in the UNIX password manager to fetch",
        default="notion.so/dev/integration/taskwarrior/token",
    )


def opt_gkeep_user_pass_path():
    return click.option(
        "--user",
        "--user-pass-path",
        "gkeep_user_pass_path",
        help="Path in the UNIX password manager to fetch the Google username from",
        default="gkeepapi/user",
    )


def opt_gkeep_passwd_pass_path():
    return click.option(
        "--passwd",
        "--passwd-pass-path",
        "gkeep_passwd_pass_path",
        help="Path in the UNIX password manager to fetch the Google password from",
        default="gkeepapi/passwd",
    )


def opt_gkeep_token_pass_path():
    return click.option(
        "--token",
        "--token-pass-path",
        "gkeep_token_pass_path",
        help="Path in the UNIX password manager to fetch the google keep token from",
        default="gkeepapi/token",
    )


def opt_gcal_calendar():
    return click.option(
        "-c",
        "--gcal-calendar",
        type=str,
        help="Name of the Google Calendar to synchronize (will be created if not there)",
    )


def opt_gkeep_labels():
    return click.option(
        "-k",
        "--gkeep-labels",
        type=str,
        multiple=True,
        help="Google Keep labels whose notes to synchronize",
    )


def opt_gkeep_ignore_labels():
    return click.option(
        "-i",
        "--gkeep-ignore-labels",
        type=str,
        multiple=True,
        help="Google Keep labels whose notes will be explicitly ignored",
    )


def opt_gkeep_note():
    return click.option(
        "-k",
        "--gkeep-note",
        type=str,
        help=(
            "Full title of the Google Keep Note to synchronize - Make sure you enable the"
            " checkboxes"
        ),
    )


def opt_google_secret_override():
    return click.option(
        "--google-secret",
        default=None,
        type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
        help="Override the client secret used for the communication with the Google APIs",
    )


def opt_google_oauth_port():
    return click.option(
        "--oauth-port",
        default=8081,
        type=int,
        help="Port to use for OAuth Authentication with Google Applications",
    )
