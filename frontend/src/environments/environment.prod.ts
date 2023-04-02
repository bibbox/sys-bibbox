export const environment = {
  production: true,
  BASEURL: 'bibbox.local',


  KEYCLOAK_URL: `http://localhost:5014`,
  KEYCLOAK_CLIENT_ID: 'sys-bibbox-frontend',
  KEYCLOAK_REALM: 'sys-bibbox',
  KEYCLOAK_NON_PROTECTED_PATHS: [
    '/logout',
    'https://raw.githubusercontent.com/',
  ],

  KEYCLOAK_ROLES : {
    admin: 'admin',
    demo_user: 'demo-user',
    standard_user: 'standard-user',
  },

  KEYCLOAK_CONFIG : {
    max_instances_per_demo_user: 3,
    resource_name: 'sys-bibbox-frontend',
  }
};
