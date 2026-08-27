# Storage access guide

Every request resolves the tenant from the signed session before touching storage.
Row-level policies enforce tenant scope on every table that carries a tenant_id column.
Background jobs receive the tenant explicitly; they never infer it from the queue name.

Connection pooling is configured per environment and documented in the runbook.
