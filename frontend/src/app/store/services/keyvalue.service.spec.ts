import { TestBed } from '@angular/core/testing';

import { KeyValueService } from './keyvalue.service';

describe('KeyValueService', () => {
  let service: KeyValueService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(KeyValueService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
