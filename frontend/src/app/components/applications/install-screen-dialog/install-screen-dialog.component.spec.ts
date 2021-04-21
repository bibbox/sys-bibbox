import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstallScreenDialogComponent } from './install-screen-dialog.component';

describe('InstallScreenDialogComponent', () => {
  let component: InstallScreenDialogComponent;
  let fixture: ComponentFixture<InstallScreenDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstallScreenDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstallScreenDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
