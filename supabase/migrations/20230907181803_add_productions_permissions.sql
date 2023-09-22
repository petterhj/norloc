create policy "Allow SELECT on published productions for all users"
    on public.productions
    as permissive
    for select
    to public
    using ( published is true );

create policy "Allow SELECT on all productions for authorized users" 
    on public.productions
    for select using ( authorize('productions.update', auth.uid()) );

create policy "Allow INSERT on productions for authorized users" 
    on public.productions
    with check ( authorize('productions.insert', auth.uid()) );

create policy "Allow UPDATE on productions for authorized users" 
    on public.productions
    for update using ( authorize('productions.update', auth.uid()) );

create policy "Allow DELETE on productions for authorized users"
    on public.productions
    for delete using ( authorize('productions.delete', auth.uid()) );
