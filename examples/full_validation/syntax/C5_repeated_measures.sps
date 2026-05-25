OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/C5_repeated_measures.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/C5_repeated_measures.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/C5_repeated_measures.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/experiment.sav'.
GLM t1_baseline t2_week2 t3_week4 t4_week8 BY treatment
  /WSFACTOR=time 4 Polynomial
  /MEASURE=score
  /METHOD=SSTYPE(3)
  /PRINT=DESCRIPTIVE ETASQ
  /WSDESIGN=time
  /DESIGN=treatment.
OMSEND.
