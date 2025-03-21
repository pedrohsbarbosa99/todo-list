CREATE TABLE IF NOT EXISTS fluxdb_migration (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    applied BOOLEAN DEFAULT FALSE,
    file TEXT UNIQUE NOT NULL
);

CREATE INDEX idx_migration_file ON fluxdb_migration(file);
