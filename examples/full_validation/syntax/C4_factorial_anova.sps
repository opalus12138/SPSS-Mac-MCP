OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/C4_factorial_anova.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/C4_factorial_anova.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/C4_factorial_anova.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/experiment.sav'.
UNIANOVA t4_week8 BY treatment intensity
  /METHOD=SSTYPE(3) /INTERCEPT=INCLUDE
  /POSTHOC=treatment(BONFERRONI)
  /EMMEANS=TABLES(treatment*intensity)
  /PRINT=DESCRIPTIVE HOMOGENEITY ETASQ.
OMSEND.
