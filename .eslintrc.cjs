module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
  },
  'extends': [
    'eslint:recommended',
    'plugin:vue/vue3-essential',
    'plugin:vue/vue3-strongly-recommended',
  ],
  'overrides': [
  ],
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module',
  },
  'plugins': [
    'vue',
  ],
  'rules': {
    'comma-dangle': ['error', 'only-multiline'],
    'indent': ['error', 2],
    'linebreak-style': ['error', 'unix'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    // https://eslint.org/docs/latest/rules/object-curly-spacing
    // https://eslint.org/docs/latest/rules/array-bracket-spacing
    'object-curly-spacing': ['error', 'always'],
    'array-bracket-spacing': ['error', 'never'],

    // https://eslint.vuejs.org/rules/max-len.html
    'vue/max-len': ['error', {
      'code': 80,
      'template': 80,
    }],
    // https://eslint.vuejs.org/rules/max-attributes-per-line.html
    'vue/max-attributes-per-line': ['error', {
      'singleline': { 'max': 5 },
      'multiline': { 'max': 1 },
    }],
  },
};
