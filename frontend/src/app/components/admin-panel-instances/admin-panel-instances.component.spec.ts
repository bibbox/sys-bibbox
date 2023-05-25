import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminPanelInstancesComponent } from './admin-panel-instances.component';

describe('AdminPanelComponent', () => {
  let component: AdminPanelInstancesComponent;
  let fixture: ComponentFixture<AdminPanelInstancesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminPanelInstancesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminPanelInstancesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
