create type role_permission as enum(
    'productions.insert',
    'productions.update',
    'productions.delete'
);

create table public.role_permissions (
  id           bigint generated by default as identity primary key,
  role         user_role not null,
  permission   role_permission not null,
  unique (role, permission)
);

comment on table public.role_permissions is 'Permissions for each role.';

alter table "public"."role_permissions" enable row level security;

create policy "Enable read access for all users"
    on "public"."role_permissions"
    as permissive
    for select
    to public
    using (true);

-- authorize with role-based access control (RBAC)
create function public.authorize(
  requested_permission role_permission,
  user_id uuid
)
returns boolean as $$
declare
  bind_permissions int;
begin
  select count(*)
  from public.role_permissions
  inner join public.user_roles on role_permissions.role = user_roles.role
  where role_permissions.permission = authorize.requested_permission
    and user_roles.id = authorize.user_id
  into bind_permissions;
  
  return bind_permissions > 0;
end;
$$ language plpgsql security definer;