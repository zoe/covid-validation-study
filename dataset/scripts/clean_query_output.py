import pandas as pd
import argparse
import warnings
from datetime import datetime, timedelta
import gcsfs
import os

warnings.filterwarnings('ignore')

def clean_data(data):
    #create the episode ID
    data['episode_id'] = data.patient_id + data['date_sick']
    #ensure that each episode has the test closest to the onset of symptoms
    ids = data.sort_values(['date_taken_specific'], ascending=True).groupby('episode_id').head(1).test_id
    #select only the logs associated to those tests
    data = data[data.test_id.isin(ids)].reset_index(drop=True)
    #get the latest assessment for a day
    data = data.sort_values(['patient_id','updated_at'], ascending=False).groupby(['patient_id','day_updated_at']).head(1).reset_index()
    #generate the age for the patient 
    data['age'] = 2020 - data['year_of_birth']
    #generate whether this is healthcare worker 
    data['hcw'] = data[['have_worked_in_hospital_care_facility', 
                       'have_worked_in_hospital_clinic',
                       'have_worked_in_hospital_home_health',
                       'have_worked_in_hospital_inpatient',
                       'have_worked_in_hospital_other',
                       'have_worked_in_hospital_outpatient',
                       'have_worked_in_hospital_school_clinic',
                       'contact_health_worker']].any(axis=1)
    #generate the BMI feature 
    data['bmi_clean'] = data['weight_kg']/(df['height_cm']/100)**2
    #generate whether patient needs help
    data['needs_help'] = data.need_inside_help | data.need_outside_help
    #generate whether patient is a PRISMA patient
    data['prisma'] = (data.age>85).astype(int) + (data.gender==1).astype(int) + (data.needs_help==True).astype(int) +  (data.housebound_problems==True).astype(int) +  (data.help_available==True).astype(int) +  (data.mobility_aid==True).astype(int) 
    #map the target to boolean values 
    data['result'] = data.result.map({'negative':False,'positive':True})
#use the country as NHS region for these ones 
    data.loc[data.country.isin(['Scotland', 'Wales', 'Northern Ireland']), 'nhser19nm'] = data.loc[data.country.isin(['Scotland', 'Wales', 'Northern Ireland']), 'country']
    #get the prevalence data fro the NHS regions
    nhs_region_data = get_data_nhs_region(datetime.today())
    # left join with region and date
    data = pd.merge(data, nhs_region_data,  how='left', left_on=['nhser19nm','day_updated_at'], right_on = ['nhser19nm','day_updated_at'])
    #add the prevalence ratio feature 
    data['prevalence_ratio'] = data['corrected_covid_positive'] / data['population']
    #add the study_day field 
    data['study_day'] = (pd.to_datetime(data.day_updated_at) - (pd.to_datetime(data.date_sick))).dt.days
    return data

#get the data for the NHS region
def get_data_nhs_region(date_today):
    'get the prevalence data for the LADs within a specific window'
    #get most recent uploaded map
    fs = gcsfs.GCSFileSystem()
    final = date_today
    month = "0" + str(final.month) if final.month < 10 else str(final.month)
    day = final.day
    year = final.year
    start_date = datetime(2020, 6 , 12)
    end_date = datetime.strptime(f"{year}{month}{day}", "%Y%m%d")
    #declare the different maps
    maps = []
    end_date_str = datetime.strftime(end_date, '%Y%m%d')
    for day in pd.date_range(start_date, end_date, freq = "24H"):
        #get the right format 
        date_file = str(day).split(" ")[0].replace("-","")
        with fs.open(os.path.join(f'covid-internal-data/covid-predictions/extrapolations/prevalence_history_{end_date_str}/corrected_prevalence_{date_file}.csv')) as fileptr:
            #read the file
            file_prev = pd.read_csv(fileptr).groupby('nhser19nm')['respondent_count', 'predicted_covid_positive_count', 'population', 'corrected_covid_positive'].sum().reset_index()
            #create the date 
            file_prev['day_updated_at'] = str(day).split(" ")[0]
            maps.append(file_prev)
    return pd.concat(maps)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-inputfile", help="Raw file to clean", type=str)
    parser.add_argument("-outfile", help="Outputfile", type=str)
    args = parser.parse_args()
    #pass the raw file to clean
    df = pd.read_csv(args.inputfile)
    #clean the data 
    cleaned_data = clean_data(df)
    #save the file to CSV
    cleaned_data.to_csv(args.outfile, index=False)
