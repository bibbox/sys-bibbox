import { KeycloakService } from 'keycloak-angular';
import {environment} from '../environments/environment';

export function initializeKeycloak(keycloak: KeycloakService) {
  return () =>
    keycloak.init({
      config: {
        url: environment.KEYCLOAK_CONFIG.url,
        realm: environment.KEYCLOAK_CONFIG.realm,
        clientId: environment.KEYCLOAK_CONFIG.clientId,
      },
      initOptions: {
        checkLoginIframe: false,
      },
      enableBearerInterceptor: true,
      bearerPrefix: 'Bearer',
      shouldAddToken: (request) => {
        const {method, url} = request;
        const isGetRequest = 'GET' === method.toUpperCase();
        const isAcceptablePathMatch = environment.KEYCLOAK_CONFIG.non_protected_paths.some((path) => url.includes(path));
        return !(isGetRequest && isAcceptablePathMatch);
      }
    });
}
