CREATE OR REPLACE FUNCTION public.add_default_user_data()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
begin
  insert into public.user_roles (id, role, updated_at)
  values (new.id, 'USER', now());

  insert into public.user_profiles (id, first_name, last_name, updated_at)
  values (
    new.id,
    new.raw_user_meta_data->>'first_name',
    new.raw_user_meta_data->>'last_name',
    now()
  );
  return new;
end;
$function$
;

CREATE TRIGGER on_user_created
  after insert on auth.users
  for each row execute procedure public.add_default_user_data();
