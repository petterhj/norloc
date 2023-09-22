create type user_role as enum('USER', 'CONTRIBUTOR', 'ADMIN');

create table "public"."user_roles" (
    "id" uuid not null,
    "role" user_role NOT NULL,
    "updated_at" timestamp with time zone
);

alter table "public"."user_roles" enable row level security;

CREATE UNIQUE INDEX user_roles_pkey ON public.user_roles USING btree (id);

alter table "public"."user_roles" add constraint "user_roles_pkey" PRIMARY KEY using index "user_roles_pkey";

alter table "public"."user_roles" add constraint "user_roles_id_fkey" FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."user_roles" validate constraint "user_roles_id_fkey";

set check_function_bodies = off;

create policy "Users can view their own role"
    on "public"."user_roles"
    as permissive
    for select
    to public
    using ((auth.uid() = id));
