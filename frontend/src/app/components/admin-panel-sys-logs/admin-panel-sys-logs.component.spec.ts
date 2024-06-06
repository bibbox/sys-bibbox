import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminPanelSysLogsComponent } from './admin-panel-sys-logs.component';

describe('SysLogsComponent', () => {
  let component: AdminPanelSysLogsComponent;
  let fixture: ComponentFixture<AdminPanelSysLogsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminPanelSysLogsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminPanelSysLogsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
