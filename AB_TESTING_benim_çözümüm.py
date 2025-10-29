#####################################################
# Comparison of Conversion Rates Between Bidding Methods Using A/B Testing
#####################################################

#####################################################
# Business Problem
#####################################################

# Facebook recently introduced a new bidding type called “average bidding” as an alternative to the existing “maximum bidding” method.
# One of our clients decided to test this new feature and wants to determine whether average bidding generates more conversions than maximum bidding.
# An A/B test has been running for one month, and our client now expects you to analyze the results of this test.
# For our client, the ultimate success metric is Purchase. Therefore, the statistical analysis should focus on the Purchase metric.


#####################################################
# Dataset Story
#####################################################

# This dataset contains information about a company’s website performance,
# including the number of ads users see and click on, as well as the revenue generated from those clicks.
# There are two separate datasets: one for the Control Group and one for the Test Group.
# These datasets are located on separate sheets in the Excel file named ab_testing.xlsx.
# The Control Group used the Maximum Bidding method, while the Test Group used the Average Bidding method.

# Variables:

# Impression: Number of times an ad is displayed
# Click: Number of times the displayed ad is clicked
# Purchase: Number of products purchased after clicking the ads
# Earning: Revenue generated from the purchased products

#####################################################
# Task 1: Data Preparation and Analysis
#####################################################

import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option("display.max_columns", None)
#pd.set_option("display.max_rows", None)
pd.set_option('display.width', 200)

#  Step 1: Read the dataset consisting of control and test groups from the file named "ab_testing.xlsx".
#  Assign the control and test data to separate variables.

df = pd.read_excel(r"ab_testing.xlsx")
df.head()

control_df = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

print(control_df.head())
print(test_df.head())

# Step 2: Analyze the control and test group datasets.

control_df.describe().T
test_df.describe().T

# Step 3: Combine the control and test group datasets using the concat method.

control_df["Group"] = "Control"
test_df["Group"] = "Test"

df = pd.concat([control_df, test_df], axis=0, ignore_index=True)
print(df.head(50))

print(df["Group"].value_counts())

#####################################################
# Task 2: Defining the A/B Test Hypothesis
#####################################################

# Step 1: Define the hypotheses.

H0: M1 = M2 (There is no statistically significant difference in the mean purchase value between the Maximum Bidding and Average Bidding methods.)
H1: M1 ≠ M2(There is a statistically significant difference in the mean purchase value between the two methods.)

# Step 2: Analyze the mean purchase values for the control and test groups.

control_df["Purchase"].mean()
test_df["Purchase"].mean()

#####################################################
# Task 3: Performing the Hypothesis Test
#####################################################

######################################################
# A/B Testing (Independent Two-Sample T-Test)
######################################################

# Step 1: Check the assumptions before running the hypothesis test.
# These assumptions are Normality and Homogeneity of Variance.

# 1. Normality Test (Shapiro-Wilk Test)

from scipy.stats import shapiro

# H0: The data is normally distributed.
# H1: The data is not normally distributed.

test_stat, pvalue = shapiro(control_df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

## Test Stat = 0.9773, p-value = 0.5891
### p-value = 0.5891 > 0.05 → Fail to reject H0 → Control group is normally distributed.

test_stat, pvalue = shapiro(test_df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

## Test Stat = 0.9589, p-value = 0.1541
## p-value = 0.1541 > 0.05 → Fail to reject H0 → Test group is normally distributed.

# Both groups are normally distributed, so the normality assumption holds.


# 2. Homogeneity of Variance (Levene’s Test)

from scipy.stats import levene

# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.

test_stat, pvalue = levene(control_df["Purchase"], test_df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

## Test Stat = 2.6393, p-value = 0.1083
### p-value = 0.1083 > 0.05 → Fail to reject H0 → Variances are homogeneous.

# Step 2: Select the appropriate test based on the assumptions.

#Since both assumptions are satisfied, use the parametric t-test.

from scipy.stats import ttest_ind

test_stat, pvalue = ttest_ind(control_df["Purchase"], test_df["Purchase"], equal_var = True)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# If assumptions were not met, the Mann–Whitney U test would have been used instead (not applicable here).

##Varsayımlar sağlandı. Bu kullanılmaz!

##from scipy.stats import mannwhitneyu

##test_stat, pvalue = mannwhitneyu(control_df["Purchase"], test_df["Purchase"], equal_var = True)
##print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


# Step 3: Interpret the results.

Test Stat = -0.9416, p-value = 0.3493
p-value = 0.3493 > 0.05. H0 reddedilemez.

#There is no statistically significant difference in the mean purchase values between the Maximum Bidding and Average Bidding methods.

##############################################################
# Task 4: Analysis of Results
##############################################################

# Step 1: Which test did you use and why?

## I used the parametric independent two-sample t-test, as I was comparing the mean purchase values between two groups.
## Both groups were normally distributed and had equal variances, meaning the assumptions of the t-test were satisfied.

# Step 2: Provide a recommendation to the client based on the results.

## There is no statistically significant difference in the average purchase (conversion) between the Maximum Bidding and Average Bidding methods.
## Therefore, switching to the new Average Bidding strategy is not expected to yield higher conversions compared to the existing Maximum Bidding approach.