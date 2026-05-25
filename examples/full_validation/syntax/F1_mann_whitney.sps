OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/F1_mann_whitney.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/F1_mann_whitney.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/F1_mann_whitney.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/nonparametric.sav'.
SELECT IF region < 3.
NPAR TESTS /M-W= income BY region(1 2)
  /MISSING ANALYSIS.
EXECUTE.
OMSEND.
