import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import wta.helpers
from wta.main import run

manual_log_calendar = {
    'Marcus': [
        {'from': 'MONDAY', 'to': 'MONDAY', 'beginTime': '10:00:00', 'endTime': '12:00:00'},
        {'from': 'TUESDAY', 'to': 'TUESDAY', 'beginTime': '10:00:00', 'endTime': '12:00:00'},
        {'from': 'WEDNESDAY', 'to': 'WEDNESDAY', 'beginTime': '10:00:00', 'endTime': '12:00:00'},
        {'from': 'THURSDAY', 'to': 'THURSDAY', 'beginTime': '10:00:00', 'endTime': '12:00:00'},
        {'from': 'FRIDAY', 'to': 'FRIDAY', 'beginTime': '10:00:00', 'endTime': '12:00:00'},
        {'from': 'MONDAY', 'to': 'MONDAY', 'beginTime': '12:30:00', 'endTime': '20:00:00'},
        {'from': 'TUESDAY', 'to': 'TUESDAY', 'beginTime': '12:30:00', 'endTime': '20:00:00'},
        {'from': 'WEDNESDAY', 'to': 'WEDNESDAY', 'beginTime': '12:30:00', 'endTime': '20:00:00'},
        {'from': 'THURSDAY', 'to': 'THURSDAY', 'beginTime': '12:30:00', 'endTime': '20:00:00'},
        {'from': 'FRIDAY', 'to': 'FRIDAY', 'beginTime': '12:30:00', 'endTime': '20:00:00'},
    ],
    'Anya': [
        {'from': 'MONDAY', 'to': 'MONDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'TUESDAY', 'to': 'TUESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'WEDNESDAY', 'to': 'WEDNESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'THURSDAY', 'to': 'THURSDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'FRIDAY', 'to': 'FRIDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
    ],
    'Dom': [
        {'from': 'MONDAY', 'to': 'MONDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'TUESDAY', 'to': 'TUESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'WEDNESDAY', 'to': 'WEDNESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'THURSDAY', 'to': 'THURSDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'FRIDAY', 'to': 'FRIDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
    ],
    'Carmine': [
        {'from': 'MONDAY', 'to': 'MONDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'TUESDAY', 'to': 'TUESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'WEDNESDAY', 'to': 'WEDNESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'THURSDAY', 'to': 'THURSDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'FRIDAY', 'to': 'FRIDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
    ],
    'Cole': [
        {'from': 'MONDAY', 'to': 'MONDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'TUESDAY', 'to': 'TUESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'WEDNESDAY', 'to': 'WEDNESDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'THURSDAY', 'to': 'THURSDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
        {'from': 'FRIDAY', 'to': 'FRIDAY', 'beginTime': '10:00:00', 'endTime': '20:00:00'},
    ],
}

infsys_data = [
    # Automated testing

    {'log_name': 'handoff-test.csv',
     'parallel_run': True,
     'batch_size': 10,
     'expected': 'handoff-test_expected.csv',
     'save_report': False},
    {'log_name': 'manual_log_1.csv',
     'parallel_run': True,
     'batch_size': 2,
     'calendar': manual_log_calendar,
     'expected': 'manual_log_1_expected.csv',
     'save_report': False},
    {'log_name': 'manual_log_2.csv',
     'parallel_run': True,
     'batch_size': 2,
     'calendar': manual_log_calendar,
     'expected': 'manual_log_2_expected.csv',
     'save_report': False},
    {'log_name': 'manual_log_3.csv',
     'parallel_run': True,
     'batch_size': 2,
     'calendar': manual_log_calendar,
     'expected': 'manual_log_3_expected.csv',
     'save_report': False},
    {'log_name': 'manual_log_4.csv',
     'parallel_run': True,
     'batch_size': 2,
     'calendar': manual_log_calendar,
     'expected': 'manual_log_4_expected.csv',
     'save_report': False},
    {'log_name': 'manual_log_5.csv',
     'parallel_run': True,
     'batch_size': 2,
     'calendar': manual_log_calendar,
     'expected': 'manual_log_5_expected.csv',
     'save_report': False},

    # Manual testing

    # {'log_name': 'Production.csv', 'parallel_run': True, 'batch_size': 2},
    # {'log_name': 'LoanApp_infRes_9-5_timers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_timers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_timers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_noTimers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_noTimers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_timers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_noTimers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_noTimers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_noTimers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_noTimers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_timers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_noTimers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_noTimers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_noTimers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_timers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_timers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_noTimers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_timers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_timers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_timers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_noTimers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_noTimers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_timers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_timers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_9-5_noTimers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_timers_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_timers.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_9-5_noTimers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_noTimers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_noTimers_prior.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_infRes_24-7_timers_prior_batch.CSV', 'parallel_run': True, 'batch_size': 10},
    # {'log_name': 'LoanApp_fewRes_24-7_timers.CSV', 'parallel_run': True, 'batch_size': 10},
]


def __remove_nan_resources(event_log: pd.DataFrame) -> pd.DataFrame:
    event_log = event_log.dropna(subset=['Resource'])
    return event_log


def __filter_specific_case(event_log: pd.DataFrame) -> pd.DataFrame:
    event_log = event_log[event_log['case_id'] == 20]
    return event_log


def __generate_calendars(log_name: str):
    prefixes = ["Clerk", "Loan Officer", "AML Investigator", "Appraiser", "Senior Officer", "Applicant"]
    calendars_24_7 = {}
    calendars_9_5 = {}
    for prefix in prefixes:
        for i in range(1000):
            resource = "{}-{number:06}".format(prefix, number=(i + 1))
            calendars_24_7[resource] = [
                {'from': 'MONDAY', 'beginTime': '00:00:00', 'to': 'MONDAY', 'endTime': '23:59:59.999999'},
                {'from': 'TUESDAY', 'beginTime': '00:00:00', 'to': 'TUESDAY', 'endTime': '23:59:59.999999'},
                {'from': 'WEDNESDAY', 'beginTime': '00:00:00', 'to': 'WEDNESDAY', 'endTime': '23:59:59.999999'},
                {'from': 'THURSDAY', 'beginTime': '00:00:00', 'to': 'THURSDAY', 'endTime': '23:59:59.999999'},
                {'from': 'FRIDAY', 'beginTime': '00:00:00', 'to': 'FRIDAY', 'endTime': '23:59:59.999999'},
                {'from': 'SATURDAY', 'beginTime': '00:00:00', 'to': 'SATURDAY', 'endTime': '23:59:59.999999'},
                {'from': 'SUNDAY', 'beginTime': '00:00:00', 'to': 'SUNDAY', 'endTime': '23:59:59.999999'}
            ]
            if prefix == "Loan Officer":
                calendars_9_5[resource] = [
                    {'from': 'MONDAY', 'beginTime': '09:00:00', 'to': 'MONDAY', 'endTime': '17:00:00'},
                    {'from': 'TUESDAY', 'beginTime': '09:00:00', 'to': 'TUESDAY', 'endTime': '17:00:00'},
                    {'from': 'WEDNESDAY', 'beginTime': '09:00:00', 'to': 'WEDNESDAY', 'endTime': '17:00:00'}
                ]
            elif prefix == "Senior Officer":
                calendars_9_5[resource] = [
                    {'from': 'THURSDAY', 'beginTime': '09:00:00', 'to': 'THURSDAY', 'endTime': '17:00:00'},
                    {'from': 'FRIDAY', 'beginTime': '09:00:00', 'to': 'FRIDAY', 'endTime': '17:00:00'}
                ]
            else:
                calendars_9_5[resource] = [
                    {'from': 'MONDAY', 'beginTime': '09:00:00', 'to': 'MONDAY', 'endTime': '17:00:00'},
                    {'from': 'TUESDAY', 'beginTime': '09:00:00', 'to': 'TUESDAY', 'endTime': '17:00:00'},
                    {'from': 'WEDNESDAY', 'beginTime': '09:00:00', 'to': 'WEDNESDAY', 'endTime': '17:00:00'},
                    {'from': 'THURSDAY', 'beginTime': '09:00:00', 'to': 'THURSDAY', 'endTime': '17:00:00'},
                    {'from': 'FRIDAY', 'beginTime': '09:00:00', 'to': 'FRIDAY', 'endTime': '17:00:00'}
                ]

    # log_name in the format of "LoanApp_fewRes_9-5_noTimers.CSV"
    calendar_time = log_name.split('_')[2]
    if calendar_time == '9-5':
        return calendars_9_5
    elif calendar_time == '24-7':
        return calendars_24_7
    else:
        raise Exception("Unknown calendar time: {}".format(calendar_time))


def extract_configuration(assets_path, test_data):
    log_path = assets_path / 'infsys-evaluation' / test_data['log_name']
    parallel = test_data['parallel_run']
    log_ids = wta.EventLogIDs()
    log_ids.start_time = 'start_time'
    log_ids.end_time = 'end_time'
    log_ids.case = 'case_id'
    log_ids.activity = 'Activity'
    log_ids.resource = 'Resource'
    calendar = test_data['calendar'] if 'calendar' in test_data else None
    return run(log_path, parallel, log_ids=log_ids, calendar=calendar), log_ids


def aggregate_report(report, log_ids):
    report['frequency'] = 1
    return report.groupby(['source_activity', 'source_resource',
                           'destination_activity', 'destination_resource']).agg(
        frequency=('frequency', 'size'),
        wt_total=(log_ids.wt_total, 'sum'),
        wt_batching=(log_ids.wt_batching, 'sum'),
        wt_prioritization=(log_ids.wt_prioritization, 'sum'),
        wt_contention=(log_ids.wt_contention, 'sum'),
        wt_unavailability=(log_ids.wt_unavailability, 'sum'),
        wt_extraneous=(log_ids.wt_extraneous, 'sum')
    ).reset_index()


def rename_columns(aggregated_report):
    aggregated_report.rename(
        columns={'destination_activity': 'target_activity', 'destination_resource': 'target_resource'}, inplace=True)
    return aggregated_report


def load_expected_data(assets_path, test_data, log_ids):
    expected_path = (assets_path / 'infsys-evaluation' / test_data['expected']) if 'expected' in test_data else None
    if expected_path:
        expected_data = wta.helpers.read_csv(expected_path)
        # Convert to seconds if needed
        for col in [
            log_ids.wt_total, log_ids.wt_batching, log_ids.wt_contention,
            log_ids.wt_prioritization, log_ids.wt_unavailability, log_ids.wt_extraneous
        ]:
            expected_data[col] = pd.to_timedelta(expected_data[col]).dt.total_seconds()
        return expected_data


def assert_report(aggregated_report, expected_data, log_ids):
    if expected_data is not None:
        columns_to_compare = [
            'source_activity', 'source_resource', 'target_activity', 'target_resource', 'frequency',
            log_ids.wt_total, log_ids.wt_batching, log_ids.wt_contention,
            log_ids.wt_prioritization, log_ids.wt_unavailability, log_ids.wt_extraneous
        ]
        wt_columns = [
            log_ids.wt_total, log_ids.wt_batching, log_ids.wt_contention,
            log_ids.wt_prioritization, log_ids.wt_unavailability, log_ids.wt_extraneous
        ]
        for col in wt_columns:
            aggregated_report[col] = pd.to_timedelta(aggregated_report[col]).dt.total_seconds()
            expected_data[col] = pd.to_timedelta(expected_data[col]).dt.total_seconds()
        aggregated_report['frequency'] = aggregated_report['frequency'].astype(float)
        expected_data['frequency'] = expected_data['frequency'].astype(float)
        assert_frame_equal(aggregated_report[columns_to_compare], expected_data[columns_to_compare])


def save_report(aggregated_report, assets_path, log_path, test_data):
    if test_data.get('save_report') and aggregated_report is not None:
        output_dir = assets_path / 'infsys-evaluation'
        handoff_output_path = output_dir / (log_path.stem + '_handoff')
        handoff_csv_path = handoff_output_path.with_suffix('.csv')
        aggregated_report.to_csv(handoff_csv_path, index=False)


@pytest.mark.infsys
@pytest.mark.integration
@pytest.mark.parametrize(
    'test_data', infsys_data,
    ids=map(lambda x: f"{x['log_name']}, parallel={x['parallel_run']}, batch_size={x['batch_size']}", infsys_data)
)
def test_for_information_systems(assets_path, test_data):
    report, log_ids = extract_configuration(assets_path, test_data)
    aggregated_report = aggregate_report(report, log_ids)
    aggregated_report = rename_columns(aggregated_report)
    expected_data = load_expected_data(assets_path, test_data, log_ids)
    assert_report(aggregated_report, expected_data, log_ids)
    save_report(aggregated_report, assets_path, test_data['log_name'], test_data)
