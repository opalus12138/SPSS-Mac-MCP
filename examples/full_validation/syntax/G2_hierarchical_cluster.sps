OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/output/G2_hierarchical_cluster.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/spv/G2_hierarchical_cluster.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/html/G2_hierarchical_cluster.html' VIEWER=NO.
GET FILE='/Users/opalus/Projects/SPSS-Mac-MCP/examples/full_validation/datasets/cluster_survival.sav'.
SAMPLE 100 FROM 500.
CLUSTER x1_spend x2_freq x3_recency
  /METHOD WARD
  /MEASURE=SEUCLID
  /PRINT SCHEDULE
  /PRINT CLUSTER(3,3)
  /PLOT NONE.
OMSEND.
