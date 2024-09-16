import { TestBed } from '@angular/core/testing';

import { IpGetServiceService } from './ip-get-service.service';

describe('IpGetServiceService', () => {
  let service: IpGetServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IpGetServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
