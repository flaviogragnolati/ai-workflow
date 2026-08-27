# Tenant isolation rules

Every request resolves the tenant from the signed session before touching storage.
Row-level policies enforce tenant scope on every table that carries a tenant_id column.
Background jobs receive the tenant explicitly; they never infer it from the queue name.

## Notes

This section was written before the policy migration and no longer reflects the schema.
