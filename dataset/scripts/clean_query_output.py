import pandas as pd
import argparse
import warnings

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
    return data


if __name__ == '__main__':

    warnings.filterwarnings('ignore')

    parser = argparse.ArgumentParser()
    parser.add_argument("-inputfile", help="Raw file to clean", type=str)
    parser.add_argument("-outfile", help="Outputfile", type=str)
    args = parser.parse_args()
    #pass the raw file to clean
    df = pd.read_csv(args.inputfile)
    #save the cleaned file 
    clean_data(df).to_csv(args.outfile, index=False)
