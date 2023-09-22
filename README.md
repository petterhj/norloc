# norloc

## Development

```sh
# .env
VITE_SUPABASE_URL=http://localhost:54321
VITE_SUPABASE_ANON_KEY=

# supabase/functions/.env
TMDB_API_KEY=
```

```sh
# Install dependencies
$ npm install

# Start Supabase and development server
$ npm run dev

# Serve Supabase functions
$ npx supabase functions serve --env-file ./supabase/.env.local
```

```sh
# Supabase commands
$ npx supabase [start|stop]    # Start/stop Supabase services 
$ npx supabase status          # Show status of local Supabase containers
```

#### Functions

* [Supabase: Functions - Local development](https://supabase.com/docs/guides/functions/local-development)
* [Supabase: Functions - Secrets](https://supabase.com/docs/guides/functions/secrets)

```sh
# Invoke function
$ curl -i --location --request POST 'http://localhost:54321/functions/v1/<function_name>' \
  --header 'Authorization: Bearer <ANON_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{foo: "bar"}'
```

#### Database migrations

* [Supabase: Database migrations](https://supabase.com/docs/guides/getting-started/local-development#database-migrations)

```sh
# Create new migration file
$ npx supabase migration new <migration_name>

# Update the created sql file (supabase/migrations/
# <timestamp>_migration_name.sql) with changes, e.g.
# by using the diff tool or pg_dump:
$ npx supabase db diff --schema public [--debug]
$ pg_dump postgresql://postgres:postgres@localhost:54322/postgres \
    --data-only \
    --inserts \
    --column-inserts \
    -n public \
    -n auth > backup.sql

# Apply the migration by resetting the database to
# current migrations
$ npx supabase db reset
```

### Deploy

```sh

```

## References

* [Supabase: Build a User Management App with Vue 3](https://supabase.com/docs/guides/getting-started/tutorials/with-vue-3)
* [supabase/examples/slack-clone](https://github.com/supabase/supabase/blob/master/examples/slack-clone/nextjs-slack-clone/)
