#!/usr/bin/env bash
set -euo pipefail

# Braslina DB restore script
# Downloads backup from MinIO and restores to PostgreSQL

BACKUP_FILE=${1:?"Usage: $0 <backup_filename>"}
BUCKET="braslina-backups"

DB_USER=${POSTGRES_USER:-braslina}
DB_NAME=${POSTGRES_DB:-braslina}

MINIO_ALIAS=${MINIO_ALIAS:-local}

echo "[$(date)] Downloading ${BACKUP_FILE} from MinIO..."
mc cp "${MINIO_ALIAS}/${BUCKET}/${BACKUP_FILE}" "/tmp/${BACKUP_FILE}"

echo "[$(date)] Restoring to database ${DB_NAME}..."
gunzip -c "/tmp/${BACKUP_FILE}" | docker exec -i braslina-db psql -U "${DB_USER}" "${DB_NAME}"

rm -f "/tmp/${BACKUP_FILE}"
echo "[$(date)] Restore complete."
