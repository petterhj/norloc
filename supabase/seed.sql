-- users
CREATE OR REPLACE FUNCTION public.create_user(
    email text,
    password text,
    first_name text,
    last_name text,
    user_role user_role
) RETURNS void AS $$
  declare
  user_id uuid;
  encrypted_pw text;
BEGIN
  user_id := gen_random_uuid();
  encrypted_pw := crypt(password, gen_salt('bf'));
  
  INSERT INTO auth.users
    (instance_id, id, aud, role, email, encrypted_password, email_confirmed_at, recovery_sent_at, last_sign_in_at, raw_app_meta_data, raw_user_meta_data, created_at, updated_at, confirmation_token, email_change, email_change_token_new, recovery_token)
  VALUES
    ('00000000-0000-0000-0000-000000000000', user_id, 'authenticated', 'authenticated', email, encrypted_pw, now(), now(), now(), '{"provider":"email","providers":["email"]}', format('{"first_name":"%s", "last_name":"%s"}', first_name::text, last_name::text)::jsonb, now(), now(), '', '', '', '');
  
  INSERT INTO auth.identities (id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at)
  VALUES
    (gen_random_uuid(), user_id, format('{"sub":"%s","email":"%s"}', user_id::text, email)::jsonb, 'email', now(), now(), now());

  UPDATE public.user_roles
    SET role = user_role
    WHERE id = user_id;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    PERFORM public.create_user(
        'admin@example.com',
        'admin-password',
        'Mario',
        'Mario',
        'ADMIN'::user_role 
    );
    
    PERFORM public.create_user(
        'contributor@example.com',
        'contributor-password',
        'Luigi',
        'Mario',
        'CONTRIBUTOR'::user_role
    );

    PERFORM public.create_user(
        'user@example.com',
        'user-password',
        'Wario',
        'Wario',
        'USER'::user_role
    );
END $$;


-- role permissions
INSERT INTO public.role_permissions (
  role,
  permission
) values 
('ADMIN'::user_role, 'productions.insert'::role_permission),
('ADMIN'::user_role, 'productions.update'::role_permission),
('ADMIN'::user_role, 'productions.delete'::role_permission),
('CONTRIBUTOR'::user_role, 'productions.insert'::role_permission),
('CONTRIBUTOR'::user_role, 'productions.update'::role_permission);


-- productions
INSERT INTO public.productions (
  type,
  title,
  plot,
  release_date,
  runtime,
  tmdb_id,
  imdb_id,
  nbdb_id,
  slug,
  poster_path,
  blur_hash,
  created_at,
  created_by,
  updated_at,
  published
) values (
  'FILM'::production_type,
  'Den brysomme mannen',
  'Den perfekte fasaden. Det totale mareritt. På overflaten har Andreas et perfekt liv. Kone, venner og bolig er som klipt ut av en livsstilskatalog. Men under overflaten er livet underlig: Andreas vet ikke hvorfor han er havnet i byen han bor i. Han trenger desperat å finne det ut. Men det kan bli farlig.',
  '2006-05-26',
  91,
  '13318',
  'tt0808185',
  '4561234',
  'den-brysomme-mannen',
  'posters/den-brysomme-mannen.jpg',
  'LiOfGXX8}7s:D4aywIfk.8aeJBj@',
  now(),
  (SELECT id from auth.users WHERE email = 'admin@example.com'),
  now(),
  true
),
(
  'FILM'::production_type,
  'Budbringeren',
  'Roy er et sjabert og kjærlighetssultent postbud som styres av nysgjerrighet, faenskap og en helt egen evne til å befinne seg på feil sted til feil tid. Han har ingen respekt for andres privatliv eller eiendom, lider av akutt mangel på yrkesetikk, rapper andres post og bor i et skikkelig høl av en hybel. Så en dag skjer det noe på postruta til Roy. Line, ei ung, døv jente glemmer husnøklene sine i postkassa. Roy knabber nøklene, nøler ett sekund og låser seg inn i leiligheten hennes. Fra nå av tar livet til Roy en annen vending. Jo mer han oppdager, jo mer vikler han seg inn i noe langt farligere enn å åpne andres brev, fortære kald spaghetti på boks, vaske seg med Zalo og hanskes med narkomane overfallsmenn.',
  '1997-02-21',
  83,
  '34582',
  NULL,
  '12344557',
  'budbringeren',
  'posters/budbringeren.jpg',
  'L7IV.BKP4Txsl:wcY6xa}uxa5%rD',
  now(),
  (SELECT id from auth.users WHERE email = 'admin@example.com'),
  now(),
  true
),
(
  'FILM'::production_type,
  'Sønner av Norge',
  'Opprør, pønkrock, drabantbyhelvete, og den evige kampen mellom hippier og pønkere. Et uvanlig far-sønn-forhold, og styrken i de båndene vi av og til gjør vårt beste for å rive over.',
  '2011-09-09',
  87,
  '81834',
  NULL,
  '901216',
  'sonner-av-norge',
  NULL,
  NULL,
  now(),
  (SELECT id from auth.users WHERE email = 'admin@example.com'),
  now(),
  false
),
(
  'TV'::production_type,
  'Kampen for tilværelsen',
  'Tomasz har aldri møtt faren. På sin leting etter ham havner han i Ullevål Hageby, der de perfekte fasadene har dypere sprekker enn man skulle tro.',
  '2014-09-10',
  45,
  '68390',
  'tt3773240',
  NULL,
  'kampen-for-tilvaerelsen',
  'posters/kampen-for-tilvaerelsen.jpg',
  NULL,
  now(),
  (SELECT id from auth.users WHERE email = 'contributor@example.com'),
  now(),
  true
);