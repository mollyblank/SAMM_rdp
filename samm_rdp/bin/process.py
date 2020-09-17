#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This sample script will get deployed in the bin directory of the
users' virtualenv when the parent module is installed using pip.
"""

import argparse

from samm_rdp import process, get_module_version

###############################################################################


def main():

    p = argparse.ArgumentParser(
        prog="run_samm_rdp", description="Run the SAMM RDP ",
    )

    p.add_argument(
        "--csv_path",
        type=str,
        default='SAMM_CONTROL_HEADERS.csv',
    )
    p.add_argument(
        "--timepoints_out_path",
        type=str,
        default=r'C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\processed_timepoints.csv',
        help="The first argument value",
    )
    p.add_argument(
        "--patients_out_path",
        type=str,
        default=r'C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\processed_patient_info.csv',
        help="The first argument value",
    )
    
    args = p.parse_args()

    process.process(csv_path=args.csv_path, timepoints_out_path=args.timepoints_out_path, patients_out_path=args.patients_out_path)

###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
