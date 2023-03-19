import { KeycloakService } from 'keycloak-angular';
import {environment} from '../environments/environment';

export function initializeKeycloak(keycloak: KeycloakService) {
  return () =>
    keycloak.init({
      config: {
        url: environment.KEYCLOAK_URL + '/auth',
        realm: environment.KEYCLOAK_REALM,
        clientId: environment.KEYCLOAK_CLIENT_ID,
      },
      initOptions: {
        checkLoginIframe: false
      },
      shouldAddToken: (request) => {
        const {method, url} = request;
        const isGetRequest = 'GET' === method.toUpperCase();
        const isAcceptablePathMatch = environment.KEYCLOAK_NON_PROTECTED_PATHS.some((path) => url.includes(path));
        return !(isGetRequest && isAcceptablePathMatch);
      }
    });
}
