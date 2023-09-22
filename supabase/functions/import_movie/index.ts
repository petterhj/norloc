import { serve } from 'deno-server';
import { createClient } from 'supabase-js';
import { corsHeaders, createResponse } from '../_shared/util.ts';
import * as tmdb from '../_shared/tmdb.ts';
import { productionSlug } from '../_shared/slug.ts';

serve(async (req) => {
  // Needed when invoking the function from a browser.
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization') }
        }
      }
    );

    const { type, tmdbid } = await req.json();

    if (!type || !tmdbid) {
      return createResponse({
        error: 'Type or TMDb ID not provided',
      }, 400);
    }

    const { data: { user } } = await supabase.auth.getUser();
    
    if (!user) {
      return createResponse({ error: 'Unauthorized' }, 401);
    }

    const { data: { permissions }, error } = await supabase
      .from('user_permissions')
      .select('role, permissions')
      .eq('id', user.id)
      .limit(1)
      .single();

    if (error) throw error;

    if (!permissions.includes('productions.insert')) {
      return createResponse({ error: 'Unauthorized' }, 401);
    }

    console.warn('import', type, tmdbid);
    const detailsResponse = await tmdb.details(type, tmdbid);
    console.log(detailsResponse);

    console.log('-----------------------------');

    const productionTitle = 
      detailsResponse.original_title || detailsResponse.title;
   
    const { data: production, error: insertError } = await supabase
      .from('productions')
      .insert({
        type: type.toUpperCase(),
        slug: productionSlug(productionTitle),
        title: productionTitle,
        release_date: detailsResponse.release_date,
        tmdb_id: detailsResponse.id,
        imdb_id: detailsResponse.imdb_id,
      })
      .select();

    console.log('-----------------------------');
    console.log(production);
    console.log('-----------------------------');

    if (insertError) throw insertError;

    return createResponse({
      type: production.type.toLowerCase(),
      slug: production.slug,
    }, 200);
  } catch (error) {
    console.log(error);
    return createResponse({ error: error.message }, 500);
  }
});
