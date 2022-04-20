"""__init__"""


from taskwarrior_syncall.aggregator import Aggregator
from taskwarrior_syncall.app_utils import (
    app_name,
    cache_or_reuse_cached_combination,
    fetch_app_configuration,
    fetch_from_pass_manager,
    get_config_name_for_args,
    get_resolution_strategy,
    inform_about_app_extras,
    inform_about_combination_name_usage,
    list_named_combinations,
    name_to_resolution_strategy_type,
    report_toplevel_exception,
)
from taskwarrior_syncall.cli import (
    opt_combination,
    opt_custom_combination_savename,
    opt_filesystem_root,
    opt_gcal_calendar,
    opt_gkeep_labels,
    opt_gkeep_note,
    opt_gkeep_passwd_pass_path,
    opt_gkeep_user_pass_path,
    opt_google_oauth_port,
    opt_google_secret_override,
    opt_list_combinations,
    opt_notion_page_id,
    opt_notion_token_pass_path,
    opt_resolution_strategy,
    opt_tw_project,
    opt_tw_tags,
)
from taskwarrior_syncall.filesystem_side import FilesystemSide
from taskwarrior_syncall.sync_side import ItemType, SyncSide
from taskwarrior_syncall.taskwarrior_side import TaskWarriorSide

__all__ = [
    "Aggregator",
    "ItemType",
    "SyncSide",
    "TaskWarriorSide",
    "FilesystemSide",
    "app_name",
    "cache_or_reuse_cached_combination",
    "fetch_app_configuration",
    "fetch_from_pass_manager",
    "get_config_name_for_args",
    "inform_about_app_extras",
    "inform_about_combination_name_usage",
    "list_named_combinations",
    "get_resolution_strategy",
    "name_to_resolution_strategy_type",
    "opt_combination",
    "opt_custom_combination_savename",
    "opt_gcal_calendar",
    "opt_gkeep_note",
    "opt_gkeep_passwd_pass_path",
    "opt_gkeep_user_pass_path",
    "opt_google_oauth_port",
    "opt_google_secret_override",
    "opt_list_combinations",
    "opt_notion_page_id",
    "opt_notion_token_pass_path",
    "opt_resolution_strategy",
    "opt_tw_project",
    "opt_filesystem_root",
    "opt_tw_tags",
    "opt_gkeep_labels",
    "report_toplevel_exception",
]

# Notion --------------------------------------------------------------------------------------
try:
    from taskwarrior_syncall.notion_side import NotionSide
    from taskwarrior_syncall.tw_notion_utils import convert_notion_to_tw, convert_tw_to_notion

    __all__.extend(["NotionSide", "convert_notion_to_tw", "convert_tw_to_notion"])
except ImportError:
    pass

# Gcal ----------------------------------------------------------------------------------------
try:
    from taskwarrior_syncall.google.gcal_side import GCalSide
    from taskwarrior_syncall.tw_gcal_utils import convert_gcal_to_tw, convert_tw_to_gcal
except ImportError:
    __all__.extend(
        [
            "GCalSide",
            "convert_gcal_to_tw",
            "convert_tw_to_gcal",
        ]
    )

try:
    from taskwarrior_syncall.fs_gkeep_utils import (
        convert_fs_file_to_gkeep_note,
        convert_gkeep_note_to_fs_file,
    )
    from taskwarrior_syncall.google.gkeep_note_side import GKeepNoteSide
    from taskwarrior_syncall.google.gkeep_todo_item import GKeepTodoItem
    from taskwarrior_syncall.google.gkeep_todo_side import GKeepTodoSide
    from taskwarrior_syncall.tw_gkeep_utils import (
        convert_gkeep_todo_to_tw,
        convert_tw_to_gkeep_todo,
    )

    __all__.extend(
        [
            "GKeepNoteSide",
            "GKeepNoteSide",
            "GKeepTodoItem",
            "GKeepTodoSide",
            "convert_gkeep_todo_to_tw",
            "convert_tw_to_gkeep_todo",
            "convert_gkeep_note_to_fs_file",
            "convert_fs_file_to_gkeep_note",
        ]
    )
except ImportError:
    pass

__version__ = "1.2.2a0"
