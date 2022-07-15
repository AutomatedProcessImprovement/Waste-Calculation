from pathlib import Path
from typing import Optional, List, Callable, Dict

import click

import process_waste.helpers
from process_waste import log_ids_non_nil, calculate_cte_impact, activity_transitions
from process_waste.waiting_time import batching
from process_waste.waiting_time.batching import BATCH_MIN_SIZE

REPORT_INDEX_COLUMNS = ['source_activity', 'source_resource', 'destination_activity', 'destination_resource']


def run(log_path: Path,
        parallel_run=True,
        log_ids: Optional[process_waste.EventLogIDs] = None,
        preprocessing_funcs: Optional[List[Callable]] = None,
        calendar: Optional[Dict] = None,
        batch_size: int = BATCH_MIN_SIZE) -> dict:
    """
    Entry point for the project. It starts the main analysis which identifies activity transitions, and then uses them
    to analyze different types of waiting time.
    """

    log_ids = log_ids_non_nil(log_ids)

    log = process_waste.helpers.read_csv(log_path, log_ids=log_ids)

    # preprocess event log
    if preprocessing_funcs is not None:
        for preprocess_func in preprocessing_funcs:
            click.echo(f'Preprocessing [{preprocess_func.__name__}]')
            log = preprocess_func(log)

    # discarding unnecessary columns
    log = log[[log_ids.case, log_ids.activity, log_ids.resource, log_ids.start_time, log_ids.end_time]]

    # NOTE: sorting by end time is important for concurrency oracle that is run during batching analysis
    log.sort_values(by=[log_ids.end_time, log_ids.start_time, log_ids.activity], inplace=True)

    # taking batch creation time from the batch analysis
    log = batching.add_columns_from_batch_analysis(
        log,
        column_names=(log_ids.batch_instance_enabled, log_ids.batch_id),
        log_ids=log_ids,
        batch_size=batch_size)
    # NOTE: Batching analysis package adds enabled_timestamp column to the log that is used later

    # total waiting time
    log[log_ids.wt_total] = log[log_ids.start_time] - log[log_ids.enabled_time]

    parallel_activities = process_waste.helpers.parallel_activities_with_heuristic_oracle(log, log_ids=log_ids)
    handoff_report = activity_transitions.identify(log, parallel_activities, parallel_run, log_ids=log_ids,
                                                   calendar=calendar)

    process_cte_impact = calculate_cte_impact(handoff_report, log, log_ids=log_ids)

    return {'handoff': handoff_report, 'process_cte_impact': process_cte_impact}
