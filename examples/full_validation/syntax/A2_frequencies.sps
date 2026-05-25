OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/A2_frequencies.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/A2_frequencies.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/A2_frequencies.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/survey_likert.sav'.
FREQUENCIES VARIABLES=Q1 Q2 Q3 gender age_group
  /STATISTICS=MEAN MEDIAN MODE STDDEV
  /ORDER=ANALYSIS.
OMSEND.
