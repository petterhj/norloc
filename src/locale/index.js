import { createI18n } from 'vue-i18n';

const messages = {
  no: {
    app: {
      title: 'Norske opptakssteder'
    },
    general: {
      loading: 'Laster',
      search: 'Søk',
      save: 'Lagre',
      unpublished: 'Upublisert',
    },
    form: {
      save: 'Lagre',
    },
    auth: {
      signin: 'Logg inn',
      signout: 'Logg ut',
      signup: 'Bli medlem',
      id: 'Identifikator',
      role: 'Rolle',
      permissions: 'Tilganger',
      states: {
        invalidCredentials: 'Feil brukernavn eller passord',
      },
      roles: {
        admin: 'Administrator',
        contributor: 'Bidragsyter',
        user: 'Medlem',
      },
      fields: {
        email: 'Epost-adresse',
        password: 'Passord',
      },
    },
    productions: {
      productions: 'Produksjoner',
      types: {
        film: 'Film',
        tv: 'TV',
      },
      errors: {
        fetch: 'Kunne ikke hente produksjoner ({type}).'
      }
    },
    production: {
      production: 'Produksjon',
      fields: {
        runtime: 'Spilletid',
        published: 'Publisert',
      },
      actions: {
        publish: 'Publiser',
        unpublish: 'Avpubliser',
      },
    },
    people: {
      people: 'Folk',
    },
    member: {
      member: 'Medlem',
      members: 'Medlemmer',
      fields: {
        firstName: 'Fornavn',
        lastName: 'Etternavn',
      }
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: 'no',
  messages,
});

export default i18n;
