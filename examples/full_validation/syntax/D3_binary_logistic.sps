OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/D3_binary_logistic.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/D3_binary_logistic.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/D3_binary_logistic.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/firm_panel.sav'.
LOGISTIC REGRESSION VARIABLES HighTQ
  /METHOD=ENTER DTI IP Lev ROA Size
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
OMSEND.
