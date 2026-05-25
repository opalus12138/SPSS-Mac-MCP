OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/D2_hierarchical_reg.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/D2_hierarchical_reg.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/D2_hierarchical_reg.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/firm_panel.sav'.
REGRESSION /STATISTICS COEFF OUTS R ANOVA CHANGE
  /DEPENDENT TQ
  /METHOD=ENTER Lev ROA Size
  /METHOD=ENTER DTI
  /METHOD=ENTER IP.
OMSEND.
