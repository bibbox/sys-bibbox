let BASEURL: string = 'localhost';

export const environment = {
  production: true,
  BASEURL: BASEURL,


  KEYCLOAK_CONFIG: {
    url: 'http://'+ BASEURL +':5014/auth',
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
