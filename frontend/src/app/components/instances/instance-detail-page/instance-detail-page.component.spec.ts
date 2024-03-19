import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstanceDetailPageComponent } from './instance-detail-page.component';

describe('InstanceDetailPageComponent', () => {
  let component: InstanceDetailPageComponent;
  let fixture: ComponentFixture<InstanceDetailPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstanceDetailPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstanceDetailPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
