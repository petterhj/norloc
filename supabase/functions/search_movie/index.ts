// Follow this setup guide to integrate the Deno language server with your
// editor:
//  https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

import { serve } from 'deno-server';
// import { createError } from 'deno-http-errors';
import { createClient } from 'supabase-js';
import { corsHeaders, createResponse } from '../_shared/util.ts';
import * as tmdb from '../_shared/tmdb.ts';


serve(async (req) => {
  // Needed when invoking the function from a browser.
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Create a Supabase client with the Auth context of the user that called
    // the function to ensure that row-level-security (RLS) policies are
    // applied.
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization') }
        }
      }
    );

    // Get the session or user object
    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
      return createResponse({ error: 'Unauthorized' }, 401);
    }

    const { type, query } = await req.json();

    if (!type || !query) {
      return createResponse({
        error: 'Type or query string not provided',
      }, 400);
    }

    const { error, data } = await supabase
      .from('productions')
      .select('tmdb_id')
      .not('tmdb_id', 'is', null);

    if (error) throw error;
    
    const tmdbIds = data.map((production) => production.tmdb_id);

    const searchResponse = await tmdb.search(type, query);

    return createResponse(
      searchResponse
        .map((result) => ({
          ...result,
          exists: tmdbIds.includes(result.id.toString()),
        })), 200);
  } catch (error) {
    console.log(error);
    return createResponse({ error: error.message }, 500);
  }
});
