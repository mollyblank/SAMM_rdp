from samm_rdp import process

csv_path = r"D:\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\SAMM_CONTROL_HEADERS.csv"
timepoints_out_path = r"C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\processed_timepoints.csv"
patients_out_path = r"C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\processed_patients.csv"

process.process(csv_path=csv_path, timepoints_out_path=timepoints_out_path, patients_out_path=patients_out_path)


