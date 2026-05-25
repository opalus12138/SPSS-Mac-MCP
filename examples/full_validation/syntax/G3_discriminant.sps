OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/G3_discriminant.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/G3_discriminant.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/G3_discriminant.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/cluster_survival.sav'.
DISCRIMINANT /GROUPS=true_segment(0 2)
  /VARIABLES=x1_spend x2_freq x3_recency
  /ANALYSIS ALL
  /PRIORS EQUAL
  /STATISTICS=COEFF RAW BOXM TABLE
  /CLASSIFY=NONMISSING POOLED.
OMSEND.
