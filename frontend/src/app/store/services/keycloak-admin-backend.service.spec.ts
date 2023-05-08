import { TestBed } from '@angular/core/testing';

import { KeycloakAdminBackendService } from './keycloak-admin-backend.service';

describe('KeycloakAdminBackendService', () => {
  let service: KeycloakAdminBackendService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(KeycloakAdminBackendService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
