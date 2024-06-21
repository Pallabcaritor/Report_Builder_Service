REALTION_MASTER_QUERY ="""SELECT
                        tc.constraint_name, tc.table_name, kcu.column_name, 
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name,
                        cf.data_type AS child_data_type, 
                        cp.data_type AS parent_data_type
                        FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        JOIN information_schema.tables as t
                            on t.table_name = tc.table_name and t.table_catalog  = tc.table_catalog and t.table_schema = tc.table_schema 
                        JOIN information_schema.columns as cf
                            on cf.table_name = tc.table_name and cf.column_name = kcu.column_name and cf.table_catalog = tc.table_catalog and cf.table_schema = tc.table_schema 
                        JOIN information_schema.columns as cp
                            on cp.table_name = ccu.table_name and cp.column_name = ccu.column_name and cp.table_catalog = ccu.table_catalog and cp.table_schema = ccu.table_schema 
                        WHERE constraint_type = 'FOREIGN KEY';"""