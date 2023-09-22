import { supabase } from '@/lib/supabase';

export default async (to, from, next) => {
  try {
    const { type, tmdbid } = to.params;
    console.warn(type, tmdbid);
    const { data, error } = await supabase
      .from('productions')
      .select('type, slug')
      .eq('type', type.toUpperCase())
      .eq('tmdb_id', tmdbid.toString())
      .limit(1);
    
    if (error) throw error;

    if (data.length) {
      const { type, slug } = data[0];
      next({
        name: 'production',
        params: { type: type.toLowerCase(), slug },
      });
      return;
    } else {
      console.warn('IMPORT');
      const { data, error } = await supabase.functions.invoke(
        'import_movie',
        { body: { type, tmdbid } },
      );

      console.warn(data);

      if (error) throw error;

      // next({
      //   name: 'production',
      //   params: { type, slug },
      // });
    }
  } catch (error) {
    console.error('import error', error);
    next(false);
  }
};
