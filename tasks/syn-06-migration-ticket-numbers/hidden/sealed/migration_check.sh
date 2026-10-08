#!/usr/bin/env bash
# migration_check.sh <workspace> : roll forward on legacy data, app behaviour, rollback, roll forward again.
# Uses its own SQLite file. Exits non-zero on the first failed assertion.
set -euo pipefail
WS="$1"; cd "$WS"
DB="$(mktemp -d)/migration.db"; export TRACKLINE_DB="$DB"
BASE_VERSION=20260929090005
q() { sqlite3 -batch -noheader "$DB" "$1"; }
fail() { echo "MIGRATION CHECK FAILED: $*" >&2; exit 1; }
expect() { [ "$2" = "$3" ] || fail "$1: expected [$3] got [$2]"; }

mix ecto.create --quiet
mix ecto.migrate --quiet --to "$BASE_VERSION"

TS() { echo "'2026-01-$1T$2Z'"; }
sqlite3 "$DB" <<SQL
INSERT INTO users (id,email,inserted_at,updated_at) VALUES (1,'legacy@example.com','2026-01-01T00:00:00Z','2026-01-01T00:00:00Z');
INSERT INTO organizations (id,name,slug,inserted_at,updated_at) VALUES
 (1,'Legacy A','legacy-a','2026-01-01T00:00:00Z','2026-01-01T00:00:00Z'),
 (2,'Legacy B','legacy-b','2026-01-01T00:00:00Z','2026-01-01T00:00:00Z'),
 (3,'Legacy Empty','legacy-empty','2026-01-01T00:00:00Z','2026-01-01T00:00:00Z');
-- org 1: ids 1..5, created out of id order, with a tie between 3 and 4
INSERT INTO tickets (id,organization_id,author_id,title,status,priority,inserted_at,updated_at) VALUES
 (1,1,1,'t1','open','normal','2026-01-03T10:00:00Z','2026-01-03T10:00:00Z'),
 (2,1,1,'t2','closed','high','2026-01-01T10:00:00Z','2026-01-04T10:00:00Z'),
 (3,1,1,'t3','open','low','2026-01-02T10:00:00Z','2026-01-02T10:00:00Z'),
 (4,1,1,'t4','pending','normal','2026-01-02T10:00:00Z','2026-01-02T10:00:00Z'),
 (5,1,1,'t5','open','urgent','2026-01-05T10:00:00Z','2026-01-05T10:00:00Z'),
 (6,2,1,'b1','open','normal','2026-01-01T09:00:00Z','2026-01-01T09:00:00Z'),
 (7,2,1,'b2','open','normal','2026-01-01T09:00:01Z','2026-01-01T09:00:01Z');
SQL
BEFORE=$(q "select id||':'||title||':'||status||':'||priority||':'||inserted_at from tickets order by id")

mix ecto.migrate --quiet
EXPECTED="1:4|2:1|3:2|4:3|5:5|6:1|7:2"
numbers() { q "select group_concat(id||':'||number, '|') from (select id, number from tickets order by id)"; }
expect "numbers after roll forward" "$(numbers)" "$EXPECTED"
expect "no ticket left without a number" "$(q 'select count(*) from tickets where number is null')" "0"
expect "row count" "$(q 'select count(*) from tickets')" "7"
AFTER=$(q "select id||':'||title||':'||status||':'||priority||':'||inserted_at from tickets order by id")
expect "other ticket data untouched" "$AFTER" "$BEFORE"
# uniqueness is enforced by the database
if sqlite3 "$DB" "INSERT INTO tickets (organization_id,author_id,title,number,inserted_at,updated_at) VALUES (1,1,'dup',1,'2026-02-01T00:00:00Z','2026-02-01T00:00:00Z');" 2>/dev/null; then
  fail "duplicate (organization, number) was accepted"
fi
# the same number in another organization is fine
sqlite3 "$DB" "INSERT INTO tickets (organization_id,author_id,title,number,inserted_at,updated_at) VALUES (3,1,'ok',1,'2026-02-01T00:00:00Z','2026-02-01T00:00:00Z'); DELETE FROM tickets WHERE title='ok';"

# application behaviour on the migrated legacy data
OUT=$(mix run --no-start -e '
  {:ok, _} = Application.ensure_all_started(:trackline)
  alias Trackline.{Repo, Support}
  u = Repo.get!(Trackline.Accounts.User, 1)
  for {label, org_id} <- [{"A1", 1}, {"A2", 1}, {"B1", 2}, {"E1", 3}, {"E2", 3}] do
    org = Repo.get!(Support.Organization, org_id)
    {:ok, t} = Support.create_ticket(org, u, %{title: "new " <> label})
    IO.puts("NEW #{label}=#{t.number}")
  end
' 2>&1 | grep '^NEW ' | tr '\n' ' ')
expect "numbers for new tickets" "$OUT" "NEW A1=6 NEW A2=7 NEW B1=3 NEW E1=1 NEW E2=2 "
sqlite3 "$DB" "DELETE FROM tickets WHERE title LIKE 'new %'"

# roll back every migration newer than the base, on a database that has tickets
NEW_COUNT=$(ls priv/repo/migrations | awk -F_ -v b="$BASE_VERSION" '$1 > b' | wc -l | tr -d ' ')
[ "$NEW_COUNT" -ge 1 ] || fail "no new migration found"
mix ecto.rollback --quiet --step "$NEW_COUNT"
expect "version after rollback" "$(q 'select max(version) from schema_migrations')" "$BASE_VERSION"
expect "row count after rollback" "$(q 'select count(*) from tickets')" "7"
expect "ticket data after rollback" "$(q "select id||':'||title||':'||status||':'||priority||':'||inserted_at from tickets order by id")" "$BEFORE"
expect "number column removed by rollback" "$(q "select count(*) from pragma_table_info('tickets') where name='number'")" "0"

# and forward again
mix ecto.migrate --quiet
expect "numbers after second roll forward" "$(numbers)" "$EXPECTED"
echo "migration check ok"
