create view users as
  select
    users.id,
    user_profiles.first_name,
    user_profiles.last_name,
    user_roles.role
  from
    auth.users
    left join user_profiles on users.id = user_profiles.id
    left join user_roles on users.id = user_roles.id;
