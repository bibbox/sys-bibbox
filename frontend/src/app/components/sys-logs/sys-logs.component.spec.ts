import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SysLogsComponent } from './sys-logs.component';

describe('SysLogsComponent', () => {
  let component: SysLogsComponent;
  let fixture: ComponentFixture<SysLogsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SysLogsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SysLogsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
