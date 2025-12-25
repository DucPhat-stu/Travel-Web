-- Logical backup helper for PostgreSQL
-- This file is NOT an actual dump, but contains recommended commands
-- to take full/schema-only/data-only backups for the Travel-Web project.
-- Run these from your terminal (adjust user/host/db/name as needed).

-- Full backup (schema + data):
--   pg_dump -U <db_user> -h <db_host> -p <db_port> -Fc -d <db_name> -f full_backup.dump

-- Schema-only:
--   pg_dump -U <db_user> -h <db_host> -p <db_port> -s -d <db_name> -f schema_only.sql

-- Data-only:
--   pg_dump -U <db_user> -h <db_host> -p <db_port> -a -d <db_name> -f data_only.sql

-- Restore (custom format):
--   pg_restore -U <db_user> -h <db_host> -p <db_port> -d <db_name> full_backup.dump

-- Tips:
-- 1) Use a dedicated DB user with minimum privileges for dump/restore.
-- 2) Run "VACUUM (ANALYZE);" after restore for best performance.
-- 3) Keep .env credentials safe; never commit real dumps to VCS.

