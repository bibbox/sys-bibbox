import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstanceGroupComponent } from './instance-group.component';

describe('InstanceGroupComponent', () => {
  let component: InstanceGroupComponent;
  let fixture: ComponentFixture<InstanceGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstanceGroupComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstanceGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
