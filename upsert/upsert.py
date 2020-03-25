# load the data
df_staging.write.format("jdbc").option("url", jdbcurl).option("dbtable", "staging_table").mode("append").save()

# write something to the "audit table" to kick off the trigger
df_audit.write.format("jdbc").option("url", jdbcurl).option("dbtable", "audit_table").mode("append").save()
