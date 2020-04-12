create table audit(
    load_time datetime,
    load_message varchar(50)
);

create trigger trigger_name
    on audit_table
    after insert as
begin
    -- upsert
    MERGE prod_table AS [Target]
    USING (SELECT * from staging_table) AS [Source]
    ON [Target].some_key = [Source].some_key
    WHEN MATCHED THEN
        UPDATE SET [Target].some_column = [Source].some_column
    WHEN NOT MATCHED THEN
        INSERT (some_column, some_column) VALUES ([Source].some_column, [Source].some_column);
    
    -- clean up
    truncate table staging_table;
end
