create view user_permissions with (security_invoker) as
    select
        user_profiles.id,
        user_roles.role,
        ARRAY_AGG (role_permissions.permission) permissions
    from
        public.user_profiles
        left join user_roles on user_profiles.id = user_roles.id
        left join role_permissions on user_roles.role = role_permissions.role
        group by user_profiles.id, user_roles.role;
