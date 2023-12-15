#!/usr/bin/env python
# coding: utf-8

# # Compare Well Treatements
# We compare the treatments in each well using cell treatment probabilities and negative control probabilities for each phenotype.
# This comparison is accomplished with a KS Test.

# In[1]:


import pathlib
import sys

import pandas as pd
from scipy.stats import kstest

# Import significance test utils
sys.path.append("utils")
import well_significance_testing as sig_test


# ## Find the root of the git repo on the host system

# In[2]:


# Get the current working directory
cwd = pathlib.Path.cwd()

if (cwd / ".git").is_dir():
    root_dir = cwd

else:
    root_dir = None
    for parent in cwd.parents:
        if (parent / ".git").is_dir():
            root_dir = parent
            break

# Check if a Git root directory was found
if root_dir is None:
    raise FileNotFoundError("No Git root directory found.")


# ## Input and Output Paths

# In[3]:


# Input paths
big_drive_path = f"{root_dir}/big_drive"
sqlite_data_path = f"{big_drive_path}/sc_data"

# Probability data path
proba_path = pathlib.Path(f"{big_drive_path}/cameron-request__cell-health-plate-classifications/multi_class_models")

# Probability data for each type of model
final_proba_path = proba_path / "final__CP_areashape_only__balanced"
shuf_proba_path = proba_path / "shuffled_baseline__CP_areashape_only__balanced"

# Platemap metadata
platemapdf = pd.read_csv(f"{root_dir}/0.image-download/manifest/idr0080-screenA-annotation.csv")

# Load probability data for final and shuffled models
final_probadf = pd.concat([pd.read_csv(data_file, index_col=0) for data_file in list(final_proba_path.glob("*.csv.gz"))])
shuf_probadf = pd.concat([pd.read_csv(data_file, index_col=0) for data_file in list(shuf_proba_path.glob("*.csv.gz"))])

# Output paths
comparison_results_output_filename = "class_balanced_well_log_reg_areashape_greg_model_comparisons.parquet"
output_path = pathlib.Path("class_balanced_well_log_reg_comparison_results")
output_path.mkdir(parents=True, exist_ok=True)


# ## KS test wrapper function

# In[4]:


def perform_ks_test(_dmso_probs, _treatment_probs):
    """
    Parameters
    ----------
    _dmso_probs: pandas.Series
        The down-sampled predicted probilities of DMSO for a treatment type and phenotype.

    _treatment_probs: pandas.Series
        The predicted probabilities of the treatment.

    Returns
    -------
    A zipped object which represents can be referenced by p_value and a comparison_metric_value, which are later on represented in the resulting dictionary.
    """
    stat, p_value = kstest(_dmso_probs, _treatment_probs, alternative="two-sided")
    return zip(["comparison_metric_value", "p_value"], [stat, p_value])


# ## Combine shuffled and final model data

# In[5]:


# Define the type of model
final_probadf["Metadata_Model_Type"] = "final"
shuf_probadf["Metadata_Model_Type"] = "shuffled"

probadf = pd.concat([final_probadf, shuf_probadf])


# ## Merge the platemap and probability data

# In[6]:


platemap_metacols = ["Plate", "Well"]
platemap_cols = ["Reagent Identifier", "Characteristics [Cell Line]", "Control Type"]
probadf = probadf.merge(platemapdf[platemap_cols + platemap_metacols], how="inner", left_on=["Metadata_Plate", "Metadata_Well"], right_on=platemap_metacols)

# Drop Redundant columns from merge
probadf.drop(columns=platemap_metacols, inplace=True)


# ## Define phenotype and columns to group by

# In[7]:


phenotype_cols = probadf.loc[:, "ADCCM":"SmallIrregular"].columns.tolist()

filt_cols = ['Metadata_Plate', 'Reagent Identifier', 'Metadata_Model_Type', 'Characteristics [Cell Line]', 'Metadata_Well']


# ## Defining tests and aggregation metric names

# In[8]:


# Create a dictionary where the keys represent the name of the comparison or test, and the values are dictionaries
# the subdictionaries refer to the wrapper function for creating the comparison, and the metric name of the comparison being made
comp_functions = {"ks_test":  # Name of the test to perform
                  {"statistical_test_function": perform_ks_test,  # The function for making comparisons
                   "comparison_metric": "ks_statistic"}  # The name of the comparison metric
                  }


# ## Compare treatments and negative controls

# In[9]:


treatments = sig_test.get_treatment_comparison(comp_functions,
                                               probadf.loc[~probadf["Control Type"].isin(["negative", "no reagent"])],
                                               probadf.loc[probadf["Control Type"] == "negative"],
                                               phenotype_cols,
                                               filt_cols
                                               )


# ## Save the output of the treatment

# In[10]:


treatments = pd.DataFrame(treatments)
treatments.to_parquet(output_path / comparison_results_output_filename)

