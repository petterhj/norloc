create type production_type as enum(
    'FILM',
    'TV'
);

alter table "public"."productions" add column "type" production_type not null;

alter table "public"."productions" add unique (type, slug);
