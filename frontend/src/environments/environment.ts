// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

let BASEURL: string = 'localhost';

export const environment = {
  production: false,
  BASEURL: BASEURL,


  KEYCLOAK_CONFIG: {
    url: 'https://keycloak.'+ BASEURL +'/auth',
    realm: 'sys-bibbox',
    clientId: 'sys-bibbox-frontend',

    non_protected_paths: [
      '/logout',
      'https://raw.githubusercontent.com/',
    ],

    roles : {
      admin: 'bibbox-admin',
      demo_user: 'bibbox-demo',
      standard_user: 'bibbox-standard',
    },

    max_instances_per_demo_user: 0,
  },
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
