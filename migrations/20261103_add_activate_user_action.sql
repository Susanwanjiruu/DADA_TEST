-- Apply this migration to an existing PostgreSQL database before
-- deploying code that writes ActionType.activate_user.
ALTER TYPE actiontype ADD VALUE IF NOT EXISTS 'activate_user';
