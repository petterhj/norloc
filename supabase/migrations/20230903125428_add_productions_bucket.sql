insert into
    storage.buckets (id, name, public, avif_autodetection)
    values('productions', 'productions', TRUE, FALSE);

create policy "Public access for production files"
    on storage.objects
    for select                              -- Allow read access
    to anon, authenticated                  -- Allow access to anonymous and authenticated users
    using ( bucket_id = 'productions' );    -- Identify the bucket
