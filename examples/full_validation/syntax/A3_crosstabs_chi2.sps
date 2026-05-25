OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/A3_crosstabs_chi2.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/A3_crosstabs_chi2.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/A3_crosstabs_chi2.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/categorical.sav'.
CROSSTABS /TABLES=industry BY digital_level
  /STATISTICS=CHISQ PHI LAMBDA
  /CELLS=COUNT ROW COLUMN
  /COUNT ROUND CELL.
OMSEND.
