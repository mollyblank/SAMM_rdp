# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 14:06:51 2020

Import and interpret patient data from SAMM Study 

@author: Molly Blank
"""

#%%   


# --- IMOPRT packages
import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
import tqdm

# Work computer location: C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\Study summary reports\Data 
# Home computer location D:\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\Study summary reports\Data processing

def format_timepoint_data(timepoint, temp_date, index):
    
        # Simple formatting of timepoint columns
        # Done by hand and pulled out to clarify parse_timepoint_row    
    
        # FORMAT WEIGHTS 
        timepoint.bag_weight = pd.to_numeric(timepoint.bag_weight, errors = 'coerce') 
        timepoint.restart_weight = pd.to_numeric(timepoint.restart_weight, errors = 'coerce') 
        timepoint.stop_weight= pd.to_numeric(timepoint.stop_weight, errors = 'coerce') 
        
        # FORMAT TIMES - defaults to all values being the temp_date counter
        timepoint.time_weight = datetime.time(pd.to_datetime(timepoint.time_weight)[index])
        timepoint.time_weight = datetime.combine(temp_date, timepoint.time_weight[index])
           
        timepoint.stop_time = datetime.time(pd.to_datetime(timepoint.stop_time)[index])
        timepoint.stop_time = datetime.combine(temp_date, timepoint.stop_time[index])
        
        timepoint.restart_time = datetime.time(pd.to_datetime(timepoint.restart_time)[index])
        timepoint.restart_time = datetime.combine(temp_date, timepoint.restart_time[index])


        
        return timepoint 
    
def midnight_rollover_check(prev_time, next_time, temp_date):
# timepoints are ALWAYS chronoligically recorded in the raw data
# if we rolled over midnight, add a day and recalculate time_delta
    
# PAST MIDNIGHT BETWEEN OBSERVATIONS
        # these timepoints are ALWAYS chronoligically recorded in the raw data
        # if we rolled over midnight, add a day and recalculate time_delta
    if (next_time < prev_time).any() :
        # increment the current point day and subsequent points 
        temp_date = temp_date + timedelta(days=1)
        next_time = next_time + timedelta(days=1)
    
    return next_time, temp_date

def weight_mass_change(current_weight, previous_weight):
    weight_delta = current_weight - previous_weight # in the original unit, either Newtons or ounces 
    # ADD WEIGHT CHECK HERE - is it the spring or the digital 
 
    # mass_delta = weight_delta * 101.9716 # the mass in grams 
    mass_delta = weight_delta * 28.35 # the mass from oz to grams 

    
    return weight_delta, mass_delta 

def time_change(current_time, prev_time, index):
    time_delta = current_time - prev_time
    time_delta = time_delta[index].seconds/60 # puts it into minutes
    
    return time_delta

def parse_timepoint_row(timepoint_row, patient, index):
    # This function takes the chunk of the raw row that has the repeating time unit measurements
    # The output of this function is a dataframe of timepoints with each row as a new measure
    
    # Look for the starting point of each new block 
    # This is indicated by the "Observer's Number" column 
    is_obs = [('observer_number' in str(column)) for column in timepoint_row.columns]
    split_points = np.where(is_obs)[0]
    
    split_points = np.concatenate([split_points, np.array([len(is_obs)])], axis=0)
    
    # INITIALIZE DATAFRAME
    timepoints = pd.DataFrame()
    
    # SET INITIAL VARIABLES ---------------
    # This is a counter to keep track of the day, since the data only includes hour/minute
    temp_date = pd.to_datetime(patient.date_enroll)
    temp_date = datetime.date(temp_date[index])
    
    # Infusion initiation info is with the patient demographic info 
    prev_time = patient.time_start  # this is re-assigned in the timepoint loop for incrementing through observation measurements
    bag_time_start = patient.time_start # this stays fixed, and is used to calculate the overall bag measurement 
    
    prev_weight = patient.weight_start 
    bag_weight_start = patient.weight_start 
    
    # the prescribed rate for each timepoint only comes up for oxytocin 
    # this sets the first prescribed rate from the patient data/demo dataframe 
    if (patient.drug == 'Oxytocin')[index]: 
        prev_rate = pd.to_numeric(patient.prescription_dpm , errors = 'coerce')[index]
    
    
    # PARSE TIMEPOINT KEY LOOP -----------------
    # Use the split points to 'chunk' long row into individual timepoint rows
    # This loop increments through each 'timepoint' and adds it as a row to 'timepoints' 
    for i, j in zip(split_points[0:-1], split_points[1:]):
        
        timepoint = timepoint_row.iloc[[0], i:j]
        format_timepoint_data(timepoint, temp_date, index)
        
        # -- OBSERVATION CHANGE
        
        # PAST MIDNIGHT BETWEEN OBSERVATIONS - checks and increments day counter accordingly
        timepoint['time_weight'], temp_date = midnight_rollover_check(prev_time, timepoint['time_weight'], temp_date)
        #  OBSERVATION DELTAS - weight and time change 
        timepoint['weight_delta'], timepoint['mass_delta']  = weight_mass_change(timepoint.bag_weight, prev_weight)
        timepoint['time_delta'] = time_change(timepoint.time_weight, prev_time, index)
        #  OBSERVATION RATE
        timepoint['observ_avg_rate_ml/hr'] = abs(timepoint['mass_delta']/timepoint['time_delta'] * 60) # ml per hour based on weight and time 
    
            
        # -- CHANGE OF BAG CASE 
        # Set the prev_weight based on if there is a new bag hung 
        if (timepoint['infusion_stop'] == 'Yes').any():      
            
            # PAST MIDNIGHT between observation and stop - increment day
            timepoint['stop_time'], temp_date = midnight_rollover_check(timepoint['time_weight'], timepoint['stop_time'], temp_date)
            # PAST MIDNIGHT between bag stop and restart - increment day
            timepoint['restart_time'], temp_date = midnight_rollover_check(timepoint['stop_time'], timepoint['restart_time'], temp_date)


            # RECALCULATE OBSERVATION DELTAS - weight and time change for last point
            # this can either be the delta from the previous observation, or from the observation until the stop time/weight 
            timepoint['weight_delta'], timepoint['mass_delta']  = weight_mass_change(timepoint.stop_weight, prev_weight) 
            timepoint['time_delta'] = time_change(timepoint.stop_time, prev_time, index)

            timepoint['observ_avg_rate_ml/hr'] = abs(timepoint['mass_delta']/timepoint['time_delta'] * 60) # ml per hour based on weight and time      
            
            # BAG AVERAGE RATE - we use the bag change to trigger this calculation 
            timepoint['bag_total_weight_infused'], timepoint['bag_total_mass_infused']  = weight_mass_change(timepoint.stop_weight, bag_weight_start)
            timepoint['bag_total_time'] = time_change(timepoint.stop_time, bag_time_start, index)

            timepoint['bag_average_rate_ml/hr'] = abs(timepoint['bag_total_mass_infused']/timepoint['bag_total_time'] * 60) #ml/hr

            # SET PREV BAG/OBSERVATION VARIABLES 
            # Set the previous observation time/weight to the restart time 
            prev_time = timepoint.restart_time
            prev_weight = timepoint.restart_weight
            
            # Set bag start variables again 
            bag_time_start = timepoint["restart_time"]
            bag_weight_start = timepoint["restart_weight"]
        
        else:
            prev_time = timepoint.time_weight  # set prev_timefor the next loop
            prev_weight = timepoint.bag_weight
            
        # RATE ERROR VS PRESCRIBED  
        if (patient['drug'] == 'Magnesium Sulphate')[index]:
            # mgso4 has a single infusion rate prescribed, which is fixed for the duration of the infusion across bags
            timepoint['prescribed_rate']= pd.to_numeric(patient.infusion_rate[index], errors = 'coerce') 
            timepoint['observ_rate_error']= timepoint['observ_avg_rate_ml/hr']-timepoint['prescribed_rate']
            timepoint['observ_rate_error_ratio']= timepoint['observ_avg_rate_ml/hr']/timepoint['prescribed_rate']
            
        else: # oxytocin 
            # oxytocin rates can change very half hour
            current_rate = pd.to_numeric(timepoint.prescribed_rate_dpm[index], errors = 'coerce')
            # so if there's a jump of 20dpm or more, there is an increase in rate between measurements
            if np.abs(prev_rate - current_rate) > 20 :
                prescribed_rate = current_rate
            else: 
                # otherwise default to the current rate being the point of comparison
                prescribed_rate = (prev_rate + current_rate)/2 
            
            timepoint['observ_rate_error']= timepoint['observ_avg_rate_ml/hr']-(prescribed_rate*3) # x3 is from: dpm * 20 gtt * 60 min/hr
            timepoint['observ_rate_error_ratio']= timepoint['observ_avg_rate_ml/hr']/(prescribed_rate*3)
            timepoint['prescribed_rate']= prescribed_rate
            
            prev_rate = current_rate # set for the next loop 
        
        if pd.isna(timepoint.loc[:, 'bag_weight'].values):     # Checks if there are no more measurements
            break                                               # Once you encounter empty rows, kick from the loop
                  
        timepoints = timepoints.append(timepoint)  
    
    return timepoints


def parse_raw_row(raw_row, index):
    # This takes in a full row from the raw csv and returns separate lists of patient data, 
    # and the timepoint data (separated into rows by hour/measurement)
        
    # take demographic information and initial measurement information 
    #     the first block (common) 
    #     the next block (oxy)
    #     the middle block (mag sulfate)
    # take all timepoints with information that is populated 
    #     for either oxy or mag sulfate, iterate through the row
    #     look for observer number to chunk into rows 
    
    
    #get all of the columns in the row
    row_columns = np.array(raw_row.columns)
    
    # all of the columns up to and including the 'drug' column are patient info
    
    # figure out where the drug column is
    drug_column_index = np.where(row_columns == 'drug')[0][0] + 1
    
    # get the patient info / get our patient row
    patient = raw_row.iloc[[0], 0:drug_column_index]

    timepoint_row = raw_row.iloc[[0], drug_column_index:]
    
    #Now split the timepoint row into drug 'Oxytocin' or 'Magnesium Sulphate'
    timepoint_columns = timepoint_row.columns
    
    split_col = np.where(timepoint_columns == 'criteria_bp')[0][0]
    
    # account for the different repeating data units between drugs 
    row_oxy = timepoint_row.iloc[[0], 0:split_col]
    row_mag = timepoint_row.iloc[[0], split_col:]

    drug = patient['drug'].item()
    
    # only get the relevant timepoint columns 
    if drug == 'Oxytocin':
        timepoint_row = row_oxy
    elif drug == 'Magnesium Sulphate':
        timepoint_row = row_mag
    
    # Everything up to the first 'observer_number' column is more patient info
        
    # now find the first 'observer_number' column
    timepoint_columns = timepoint_row.columns
    
    is_obs = ["observer_number" in str(column) for column in timepoint_columns]
    
    split_col = np.where(is_obs)[0][0]
    patient_appendix = timepoint_row.iloc[[0], 0:split_col]
    
    # append first measurement to patient info
    patient = pd.concat([patient, patient_appendix], axis = 1)
 
    
    # FORMAT---- 
    
    # set the bag weight to a numeric value so we can do math to it
    patient.weight_start = pd.to_numeric(patient.weight_start, errors = 'coerce') 
    # set the infusion start time to a time value
    patient.time_start = pd.to_datetime(patient.date_enroll + ' ' + patient.time_start)

    # The rest of the row is the repeating timepoints, so we get those and parse them
    timepoint_row = timepoint_row.iloc[[0], split_col:]
    
    # Now we pop into the other function to process this row into observation instances
    timepoints = parse_timepoint_row(timepoint_row, patient, index)
    
    
    return patient, timepoints

# STARTING CODE  ------- 
# --- IMOPRT DATA FROM REDCAP FILE
def process(
    csv_path='SAMM_CONTROL_HEADERS.csv', 
    timepoints_out_path=r'C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\processed_timepoints.csv',
    patients_out_path=r'C:\Users\Molly Blank\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\processed_patients.csv'
    ):

    raw = pd.read_csv(csv_path, header=None) 
    raw.columns = raw.iloc[0]
    raw = raw.reindex(raw.index.drop(0)).reset_index(drop=True)

    # this determines what value will be used to index the later dataframes
    patient_id_column = 'record_no'

    patient_master = list()
    timepoint_master = list()

    # CORE LOOP ---- 

    for index in tqdm.tqdm(range(raw.shape[0])): # Do the whole file (500 patients)
    #for index in range(400,420): # sample some sub range
        row = raw.iloc[[index]]
        patient_id = row.loc[:, patient_id_column][index]
        
        # This returns a one row dataframe of patient demographic info,
        # and a dataframe with rows that are timepoints associated with that patient
        patient, timepoints = parse_raw_row(row, index)    
        patient = patient.set_index(patient_id_column) 
        
        # Add a column to timepoints corresponding with the patientID so it can be standalone and indexed
        timepoints[patient_id_column] = patient_id
        timepoints = timepoints.set_index(patient_id_column) 
        
        # After stepping through the loop, this adds each new set of rows to the summary
        patient_master.append(patient)           # puts the current patient info at the end of the master list 
        timepoint_master.append(timepoints)      # puts the current timepoints at the end of the master list 

    # takes dataframe format and makes it into a single table to output to csv (formatting step)
    timepoints_to_csv = pd.concat(timepoint_master)
    patients_to_csv = pd.concat(patient_master)

    #%%

    # SAVE TO FILE 
    timepoints_to_csv.to_csv(timepoints_out_path)
    patients_to_csv.to_csv(patients_out_path)

                






