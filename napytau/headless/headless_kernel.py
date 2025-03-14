from pathlib import PurePath

import numpy as np

from napytau.cli.cli_arguments import CLIArguments
from napytau.core.chi import optimize_tau_factor
from napytau.core.core import (
    calculate_lifetime_for_fit,
    calculate_lifetime_for_custom_tau_factor,
    calculate_optimal_tau_factor,
)
from napytau.headless.logging import log_dataset, log_dataset_setup_data
from napytau.import_export.import_export import (
    IMPORT_FORMAT_LEGACY,
    IMPORT_FORMAT_NAPYTAU,
    import_legacy_format_from_files,
    read_legacy_setup_data_into_data_set,
    import_napytau_format_from_file,
    read_napytau_setup_data_into_data_set,
)
from napytau.import_export.model.dataset import DataSet


def init(cli_arguments: CLIArguments) -> None:
    if cli_arguments.get_dataset_format() == IMPORT_FORMAT_LEGACY:
        setup_files_directory_path = cli_arguments.get_data_files_directory_path()

        fit_file_path = cli_arguments.get_fit_file_path()

        dataset: DataSet = import_legacy_format_from_files(
            PurePath(setup_files_directory_path),
            PurePath(fit_file_path) if fit_file_path else None,
        )

        log_dataset(dataset)

        setup_file_path = cli_arguments.get_setup_identifier()
        if setup_file_path is not None:
            read_legacy_setup_data_into_data_set(dataset, PurePath(setup_file_path))
            log_dataset_setup_data(dataset)

    elif cli_arguments.get_dataset_format() == IMPORT_FORMAT_NAPYTAU:
        setup_files_directory_path = cli_arguments.get_data_files_directory_path()
        setup_identifier = cli_arguments.get_setup_identifier()

        (dataset, raw_setups) = import_napytau_format_from_file(
            PurePath(setup_files_directory_path)
        )

        log_dataset(dataset)

        if setup_identifier is not None:
            read_napytau_setup_data_into_data_set(dataset, raw_setups, setup_identifier)
            log_dataset_setup_data(dataset)
    else:
        raise ValueError(
            f"Unknown dataset format: {cli_arguments.get_dataset_format()}"
        )

    (tau_fit, tau_fit_error) = calculate_lifetime_for_fit(
        dataset=dataset,
        polynomial_degree=2,
    )
    print(f"Calculated lifetime: {tau_fit} ± {tau_fit_error}")

    t_hyp_estimate = cli_arguments.get_t_hyp_estimate()
    if t_hyp_estimate is not None:
        print(f"Tau factor: {t_hyp_estimate}")
        tau_custom, tau_custom_error = calculate_lifetime_for_custom_tau_factor(
            dataset=dataset,
            custom_tau_factor=t_hyp_estimate,
            polynomial_degree=2,
        )
    else:
        t_hyp = calculate_optimal_tau_factor(
            dataset=dataset,
            t_hyp_range=(0.1, 1.0),
            weight_factor=1.0,
            polynomial_degree=2,
        )
        print(f"Tau factor: {t_hyp}")

        tau_custom, tau_custom_error = calculate_lifetime_for_custom_tau_factor(
            dataset=dataset,
            custom_tau_factor=t_hyp,
            polynomial_degree=2,
        )
    print(f"Calculated lifetime with custom tau factor: {tau_custom} ± {tau_custom_error}")