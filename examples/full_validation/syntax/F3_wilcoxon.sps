OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/F3_wilcoxon.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/F3_wilcoxon.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/F3_wilcoxon.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/experiment.sav'.
NPAR TESTS /WILCOXON=pre_test WITH post_test (PAIRED).
OMSEND.
