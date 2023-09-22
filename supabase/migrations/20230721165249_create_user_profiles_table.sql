create table "public"."user_profiles" (
    "id" uuid not null,
    "first_name" text not null,
    "last_name" text not null,
    "updated_at" timestamp with time zone
);


alter table "public"."user_profiles" enable row level security;

CREATE UNIQUE INDEX user_profiles_pkey ON public.user_profiles USING btree (id);

alter table "public"."user_profiles" add constraint "user_profiles_pkey" PRIMARY KEY using index "user_profiles_pkey";

alter table "public"."user_profiles" add constraint "user_profiles_id_fkey" FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."user_profiles" validate constraint "user_profiles_id_fkey";

alter table "public"."user_profiles" add constraint "first_name_length" CHECK ((char_length(first_name) >= 2)) not valid;

alter table "public"."user_profiles" validate constraint "first_name_length";

alter table "public"."user_profiles" add constraint "last_name_length" CHECK ((char_length(last_name) >= 2)) not valid;

alter table "public"."user_profiles" validate constraint "last_name_length";

set check_function_bodies = off;


create policy "Users can view their own profile"
    on "public"."user_profiles"
    as permissive
    for select
    to public
    using ((auth.uid() = id));


create policy "Users can insert their own profile"
    on "public"."user_profiles"
    as permissive
    for insert
    to public
    with check ((auth.uid() = id));


create policy "Users can update own profile"
    on "public"."user_profiles"
    as permissive
    for update
    to public
    using ((auth.uid() = id));
