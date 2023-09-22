const TMDB_API_BASE_URL = 'https://api.themoviedb.org/3';

async function tmdbRequest(path, params) {
  const queryParams = new URLSearchParams({
    ...params,
    language: 'no-NB',
  });

  const requestUrl = `${TMDB_API_BASE_URL}${path}?${queryParams}`;

  console.debug(`TMDb request: ${requestUrl}`);

  const resp = await fetch(requestUrl, { headers: {
    'Authorization': `Bearer ${Deno.env.get('TMDB_API_KEY')}`,
  } });
  
  const data = await resp.json();

  if (data?.status === false) {
    throw new Error(data.status_message);
  }

  return data;
}

export async function search(type, query) {
  const tmdbConfig = await tmdbRequest('/configuration');
  const searchType = type === 'tv' ? 'tv' : 'movie';
  const data = await tmdbRequest(`/search/${searchType}`, {
    query,
    include_adult: false,
    language: 'no',
    page: 1,
  });

  if (!data.results.length) {
    return [];
  }

  if (searchType === 'tv') {
    return data.results
      .filter(({ origin_country }) => origin_country.includes('NO'))
      .map(({
        id,
        name,
        original_name,
        original_language,
        overview,
        first_air_date,
        poster_path,
      }) => ({
        type: 'tv',
        id,
        title: name,
        original_title: original_name,
        original_language,
        overview,
        release_date: first_air_date,
        poster_url: poster_path ? 
          `${tmdbConfig.images.secure_base_url}w185${poster_path}` : 
          null,
      }));  
  }

  return data.results
    .filter(
      ({ original_language }) => ['no', 'nb'].includes(original_language)
    )
    .map(({
      id,
      title,
      original_title,
      original_language,
      overview,
      release_date,
      poster_path,
    }) => ({
      type: 'film',
      id,
      title,
      original_title,
      original_language,
      overview,
      release_date,
      poster_url: poster_path ? 
        `${tmdbConfig.images.secure_base_url}w185${poster_path}` : 
        null,
    }));
}

export async function details(type, tmdbid) {
  const tmdbConfig = await tmdbRequest('/configuration');
  const searchType = type === 'tv' ? 'tv' : 'movie';
  const details = await tmdbRequest(`/${searchType}/${tmdbid}`, {
    append_to_response: 'external_ids',
  });

  console.log('details', details);
  
  const response = {
    id: details.id,
    overview: details.overview,
    genres: details.genres.map((genre) => genre.name),
    production_countries: details.production_countries.map(({
      iso_3166_1,
      name,
    }) => ({
      name,
      code: iso_3166_1,
    })),
    spoken_languages: details.spoken_languages.map(({
      iso_639_1,
      name,
    }) => ({
      name,
      code: iso_639_1,
    })),
    production_companies: details.production_companies.map(({
      id,
      name,
      origin_country,
    }) => ({
      id,
      name,
      country: origin_country,
    })),
    poster_url: details.poster_path ? 
      `${tmdbConfig.images.secure_base_url}w185${details.poster_path}` : 
      null,
    imdb_id: details.external_ids?.imdb_id,
    status: details.status,
  };

  return searchType === 'tv' ? {
    ...response,
    title: details.name,
    original_title: details.original_name,
    release_date: details.first_air_date,
    runtime: details.episode_run_time,
  } : {
    ...response,
    title: details.title,
    original_title: details.original_title,
    release_date: details.release_date,
    runtime: details.runtime,
  };
}