# Study: Testing the Accuracy of a Digital Test to Diagnose Covid-19

This study is registered on clinicaltrials.gov (NCTXXX). 
In this section, we describe the models that have been frozen for validation in each phase.

## Phase 1:

### Models
Random Forest classifiers were built using the RandomForestClassifer class in the `scikit-learn 0.22.2.post1` library available in `Python 3.7.7`

Hyperparameters such as `criterion`, `n_estimators`, `max_features`, `max_depth`, `min_samples_split`, `min_samples_leaf` and `bootstrap` were optimised using randomised search across 5 fold and up to 100 iterations. 

All models were trained with data previous to the start of the validation study (before the 29th of April) using the first 48/72 hours of symptoms for users that reported a positive or negative test.

Symptoms on the first 48/72 hours were aggregated per participant by averaging the number of active symptoms on this period.

#### Features

Features or predictors used by the model belong to one of these two types:

###### Participant
- `age`: age in years from date of birth to 2020
- `hcw`: {0: non-healthcare worker/ 1: health-care worker}. This field is calculated from: Have_worked_in_hospital_care_facility OR have_worked_in_hospital_clinic
- `have_worked_in_hospital_home_health` OR `have_worked_in_hospital_inpatient`
`have_worked_in_hospital_other` OR `have_worked_in_hospital_outpatient` OR `have_worked_in_hospital_school_clinic` 
OR `contact_health_worker`
- `bmi_clean`: a float value (kg/cm2) within 16 and 55. 
- `gender`: {0: female / 1: male}
- `prisma`: an integer score from 0 - 6 calculated as follows: age>85 + (gender=='male') + (need_help==True) + (housebound_problems==True) + (help_available==False) + (mobility_aid==True)
- `has_diabetes`: {0: hasn’t had diabetes / 1: has had diabetes}
- `has_heart_disease`: {0: hasn’t had heart disease / 1: has had heart disease}
- `has_lung_disease`: {0: hasn’t had lung disease / 1: has had lung disease}
- `has_kidney_disease`: {0: hasn’t had kidney disease / 1: has had kidney disease}

##### Symptoms
	All symptoms were grouped by participant and counted the number of days each symptom was logged during the first 2 or 3 days. They were also normalised to the number of days (N).  
- `persistent_cough`: a float value calculated as the sum of the persistent_cough column in the assessments of each participant divided by N. The persistent_cough column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `fatigue`:  a float value calculated as the sum of the fatigue column in the assessments of each participant divided by N. The fatigue column in each assessment takes values {No/Mild/Severe} which were mapped to {0/1/2}
- `delirium`:  a float value calculated as the sum of the delirium column in the assessments of each participant divided by N. The delirium column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `shortness_of_breath`: a float value calculated as the sum of the shortness_of_breath column in the assessments of each participant divided by N. The shortness_of_breath in each assessment takes values {No/Mild/Significant/Severe} which were mapped to {0/1/2/3}
- `fever`: a float value calculated as the sum of the fever column in the assessments of each participant divided by N. The fever column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `diarrhoea`: a float value calculated as the sum of the diarrhoea column in the assessments of each participant divided by N. The diarrhoea column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `abdominal_pain`:  a float value calculated as the sum of the abdominal_pain column in the assessments of each participant divided by N. The abdominal_pain column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `chest_pain`: a float value calculated as the sum of the chest_pain column in the assessments of each participant divided by N. The chest_pain column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `hoarse_voice`: a float value calculated as the sum of the hoarse_voice column in the assessments of each participant divided by N. The hoarse_voice column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `skipped_meals`:  a float value calculated as the sum of the skipped_meals column in the assessments of each participant divided by N. The skipped_meals column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `loss_of_smell`:  a float value calculated as the sum of the loss_of_smell column in the assessments of each participant divided by N. The loss_of_smell column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `headache`: a float value calculated as the sum of the headache column in the assessments of each participant divided by N. The headache column in each assessment takes values {No/Yes} which were mapped to {0/1}
- `sore_throat`: a float value calculated as the sum of the sore_throat column in the assessments of each participant divided by N. The sore_throat column in each assessment takes values {No/Yes} which were mapped to {0/1}

##### Response
- `tested_covid_positive`: True/False

#### Classifiers 
The 4 classifiers were created choosing their thresholds as follows:
- High sensitivity classifier: at least 90% in sensitivity and maximum specificity 
- High specificity classifier: at least 90% in specificity and maximum sensitivity
- Maximum sensitivity and specificity: Youden's J statistic 


#### Files

Binary Files storing the models
- Classifiers for the first 42 hours: `Grouped_RF_2_12_05.joblib`
- Classifiers for the first 72 hours: `Grouped_RF_3_12_05.joblib`

Each  file contains a list of with the following object:
- `clf`: Trained RandomForestClassifier object
- `idx_optimal`: integer indicating the position of the maximum sensitivity and specificity classifier in the array of thresholds.
- `idx_high_sens`: integer indicating the position of the high sensitivity classifier in the array of thresholds.
- `idx_high_spec`:  integer indicating the position of the high specificity classifier in the array of thresholds.
- `thresholds`: numpy array of thresholds from the ROC in training.
- `fpr`: numpy array with the false positive rate from the ROC in training
- `tpr`: numpy array with the true positive rate from the ROC in training
- `FEATURES`: List of all features used by the model
- `ALL_SYMPTOMS`: List of symptoms used as features by the model
- `PAT_FEATURES`: List of patient features used by the model

##### Code snippet to run predictions

`Validation script.ipynb` contains the full code to run predictions and evaluate the 8 classifiers. 

The following snippet describes the main line to run predictions. 

`test_df` is a pandas dataframe where each row contains an assessment logged by a participant with all the features and outcomes described above. 

```python

clf, idx_optimal, idx_high_sens, idx_high_spec, thresholds, fpr, tpr, FEATURES, ALL_SYMPTOMS, \
                                            PAT_FEATURES = load('../models/Grouped_RF_3_12_05.joblib')
N = 3
grouped_test_df = pd.concat([test_df.groupby('patient_id')[ALL_SYMPTOMS].agg(lambda x: 
                                            x.sum()/N), test_df.groupby('patient_id')[PAT_FEATURES+TARGET].mean()], 
                                            axis=1).reset_index(drop=True)
X_test = grouped_test_df.loc[:, FEATURES]
y_test = grouped_test_df.loc[:, TARGET].values[:,0]
X_test.loc[:,'predicted_covid'] = clf.predict_proba(X_test.loc[:, FEATURES])[:,1]>thresholds[idx]
X_test.loc[:,'p_predicted_covid'] = clf.predict_proba(X_test.loc[:, FEATURES])[:,1]
```
