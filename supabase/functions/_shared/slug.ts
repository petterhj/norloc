// https://github.com/simov/slugify

import slugify from 'slugify';

export function productionSlug(title) {
  return slugify(title, {
    replacement: '-',
    lower: true,
    strict: true,
    locale: 'nb',
  });
}
