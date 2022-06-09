# Python Function Dependency Graphs
- Code Structure Reviewer 

This is to plot dependency graphs at function level. [Python Function Dependency graphs](https://github.com/heraldia/pydeps-function-level)

# Another sister project
This is to plot dependency graphs at module/python-file level. 
- [Python Module Dependency graphs](https://github.com/thebjorn/pydeps)

# Setup
```sh
conda env update -f env/code_structure_review_env.yml
conda activate code_structure_review_env
python codeStructureReivewer.py
```
# Usage
Only one argument need to give: target_dir in codeStructureReivewer.py

# Enhancement changelog
- Jupyter Notebook
- avoid functionName in comments
- eliminating edge cases:
    ```
    def job_code(): # function-name exists in a plain string, but it should not taken as a function-call.
    row , CAST(a.job_code AS INT) AS WORKGROUP_ID
    ```
- module name
- class name

- detect inner method and recognize function-call
```py
def wfp_check(loaded_model_3,loaded_fe_3):

    share_wfp = loaded_model_3.rec_df[loaded_model_3.rec_df['STORE_NBR'].isin(pilot_stores)].merge(
        loaded_model_3.cp_workgroup_dim_df,on='WORKGROUP_ID').merge(
        loaded_model_3.cp_job_selection_dim_df,on='JOB_SELECTION_ID')
    def formatting(r):
        pos = str(int(r['NUM_OF_POS']))
```
- Analyze a certain script

# Info
Project starts at 2022_0413_1108 CT

