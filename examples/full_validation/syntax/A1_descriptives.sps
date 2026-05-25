OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/A1_descriptives.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/A1_descriptives.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/A1_descriptives.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/firm_panel.sav'.
DESCRIPTIVES VARIABLES=TQ DTI IP Lev ROA Size
  /STATISTICS=MEAN STDDEV MIN MAX KURTOSIS SKEWNESS.
OMSEND.
