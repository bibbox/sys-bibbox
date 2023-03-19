// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  BASEURL: 'localhost',
  KEYCLOAK_URL: `http://localhost:5014`,
  KEYCLOAK_CLIENT_ID: 'sys-bibbox-frontend',
  KEYCLOAK_REALM: 'sys-bibbox',

  KEYCLOAK_NON_PROTECTED_PATHS: [
    '/logout',
    'https://raw.githubusercontent.com/',
  ],

};

// TODO replace Keycloak env params dynamically

// baseurl bibbox.local

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
