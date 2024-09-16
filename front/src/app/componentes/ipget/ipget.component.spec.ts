import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IpGetSComponent } from './ipget.component';

describe('IpgetComponent', () => {
  let component: IpGetSComponent;
  let fixture: ComponentFixture<IpGetSComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IpGetSComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IpGetSComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
